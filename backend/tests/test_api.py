"""Run: python -m unittest discover -s tests -v (from backend).
Uses a disposable SQLite database and a separate HTTP process, never .env data.
"""
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import time
import unittest
from urllib.request import Request, urlopen
from urllib.error import HTTPError

WORKSPACE = Path(__file__).resolve().parents[1]
TMP = tempfile.TemporaryDirectory(prefix='valuator-regression-')
os.environ['DATABASE_URL'] = 'sqlite:///' + str(Path(TMP.name) / 'test.sqlite')
os.environ['ENABLE_DEMO'] = 'false'
sys.path.insert(0, str(WORKSPACE))
from main import Base, engine, SessionLocal, UserTable, EvaluationTable, LoginSession, WeightSetting
from app.core.security import hash_password, token_digest, PREFIX
from datetime import datetime, timedelta


class ApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with socket.socket() as sock:
            sock.bind(('127.0.0.1', 0))
            cls.port = sock.getsockname()[1]
        cls.base = f'http://127.0.0.1:{cls.port}'
        cls.start_server()

    @classmethod
    def start_server(cls):
        cls.log = open(Path(TMP.name) / 'server.log', 'a', encoding='utf-8')
        cls.proc = subprocess.Popen([sys.executable, '-B', '-m', 'uvicorn', 'main:app',
                                     '--host', '127.0.0.1', '--port', str(cls.port)],
                                    cwd=WORKSPACE, env=os.environ.copy(), stdout=cls.log,
                                    stderr=subprocess.STDOUT)
        for _ in range(100):
            try:
                with urlopen(cls.base, timeout=1):
                    return
            except Exception:
                time.sleep(.1)
        raise RuntimeError('Test server failed to start')

    @classmethod
    def stop_server(cls):
        if os.name == 'nt':
            # Windows venv launchers may own a child Python process holding the log.
            subprocess.run(['taskkill', '/PID', str(cls.proc.pid), '/T', '/F'],
                           check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        else:
            cls.proc.terminate()
        cls.proc.wait(timeout=10)
        cls.log.close()

    @classmethod
    def tearDownClass(cls):
        cls.stop_server()
        engine.dispose()
        TMP.cleanup()

    def setUp(self):
        with engine.begin() as db:
            for table in reversed(Base.metadata.sorted_tables):
                db.execute(table.delete())
        with SessionLocal() as db:
            db.add(UserTable(username='admin', password=hash_password('admin-test-secret'), hospital='Admin hospital'))
            db.commit()
        self.alice = self.register_login('alice')
        self.bob = self.register_login('bob')
        self.admin = self.login('admin', 'admin-test-secret')

    def call(self, method, path, data=None, token=None):
        headers = {'Content-Type': 'application/json'}
        if token:
            headers['Authorization'] = 'Bearer ' + token
        req = Request(self.base + path, data=json.dumps(data).encode() if data is not None else None,
                      headers=headers, method=method)
        try:
            response = urlopen(req, timeout=10)
        except HTTPError as err:
            response = err
        with response:
            return response.status, json.load(response)

    def login(self, name, password='test-password'):
        status, body = self.call('POST', '/api/auth/login', dict(username=name, password=password))
        self.assertEqual(status, 200, body)
        return body['data']['token']

    def register_login(self, name):
        status, body = self.call('POST', '/api/auth/register', dict(username=name, password='test-password', hospital=name+' hospital'))
        self.assertEqual(status, 200, body)
        return self.login(name)

    def create(self, token=None):
        status, body = self.call('POST', '/api/evaluations', self.payload(), token or self.alice)
        self.assertEqual(status, 200, body)
        return body['data']['id']

    def payload(self):
        return dict(name='Regression evaluation', indicators=[dict(category=1, item_name='strategicPlanning', amount=.1),
                                                              dict(category=2, item_name='dataPurchase', amount=.2)])

    def test_ownership_all_operations(self):
        eid = self.create()
        for method, suffix, body in [('GET', '', None), ('GET', '/result', None),
                                     ('PUT', '', {'name':'other'}), ('DELETE', '', None),
                                     ('POST', '/submit', None), ('POST', '/duplicate', None)]:
            for token, expected in [(None, 401), (self.bob, 404)]:
                with self.subTest(method=method, suffix=suffix, token=expected):
                    self.assertEqual(self.call(method, f'/api/evaluations/{eid}{suffix}', body, token)[0], expected)
        self.assertEqual(self.call('GET', f'/api/evaluations/{eid}', token=self.admin)[0], 200)

    def test_admin_endpoints_private(self):
        for method,path,body in [('GET','/api/admin/stats',None),('GET','/api/admin/weights',None),
                                 ('PUT','/api/admin/weights',{'1':2}),('GET','/api/admin/users',None),
                                 ('POST','/api/demo/init',None)]:
            for token, expected in [(None,401),(self.alice,403)]:
                with self.subTest(path=path, token=expected):
                    self.assertEqual(self.call(method,path,body,token)[0],expected)
        self.assertEqual(self.call('POST','/api/demo/init',token=self.admin)[0],403)

    def test_registration_reserved_and_validation(self):
        for name in ['admin',' ADMIN ']:
            self.assertEqual(self.call('POST','/api/auth/register',dict(username=name,password='secret1',hospital='H'))[0],403)
        for body in [dict(username=' ',password='secret1',hospital='H'),dict(username='new',password='x',hospital='H'),dict(username='new',password='secret1',hospital=' ')]:
            self.assertEqual(self.call('POST','/api/auth/register',body)[0],422)
        self.assertEqual(self.call('POST','/api/auth/register',dict(username=' alice ',password='secret1',hospital='H'))[0],400)

    def test_password_hash_and_legacy_upgrade(self):
        with SessionLocal() as db:
            self.assertTrue(db.query(UserTable).filter_by(username='alice').one().password.startswith(PREFIX))
            db.add(UserTable(username='legacy',password='old-password',hospital='H'))
            db.commit()
        self.assertEqual(self.call('POST','/api/auth/login',dict(username='legacy',password='wrong'))[0],401)
        self.login('legacy','old-password')
        with SessionLocal() as db:
            self.assertTrue(db.query(UserTable).filter_by(username='legacy').one().password.startswith(PREFIX))

    def test_token_expiry_logout_reset_delete(self):
        with SessionLocal() as db:
            db.get(LoginSession,token_digest(self.bob)).expires_at=datetime.utcnow()-timedelta(seconds=1)
            alice_id=db.query(UserTable).filter_by(username='alice').one().id
            bob_id=db.query(UserTable).filter_by(username='bob').one().id
            db.commit()
        self.assertEqual(self.call('GET','/api/user/info',token=self.bob)[0],401)
        self.assertEqual(self.call('PUT',f'/api/admin/users/{alice_id}',{'password':'replacement'},self.admin)[0],200)
        self.assertEqual(self.call('GET','/api/user/info',token=self.alice)[0],401)
        token=self.login('alice','replacement')
        self.call('POST','/api/auth/logout',token=token)
        self.assertEqual(self.call('GET','/api/user/info',token=token)[0],401)
        token=self.login('bob')
        self.call('DELETE',f'/api/admin/users/{bob_id}',token=self.admin)
        self.assertEqual(self.call('GET','/api/user/info',token=token)[0],401)

    def test_statistics_and_admin_scope(self):
        self.create()
        self.assertEqual(self.call('GET','/api/evaluations/stats',token=self.bob)[1]['data']['total_count'],0)
        self.assertEqual(self.call('GET','/api/evaluations',token=self.bob)[1]['data']['total'],0)
        self.assertEqual(self.call('GET','/api/evaluations?scope=all',token=self.bob)[0],403)
        self.assertEqual(self.call('GET','/api/evaluations?scope=all',token=self.admin)[1]['data']['total'],1)
        self.assertEqual(self.call('GET','/api/evaluations',token=self.admin)[1]['data']['total'],0)

    def test_decimal_report_edit_copy_delete(self):
        eid=self.create()
        path=f'/api/evaluations/{eid}'
        result=self.call('GET',path+'/result',token=self.alice)[1]['data']
        self.assertEqual(result['totalValue'],.3)
        self.assertEqual(result['hospital'],'alice hospital')
        self.assertEqual(result['details'][0]['itemName'],'战略规划成本')
        self.assertEqual(len(result['categories'][0]['details']),1)
        self.assertEqual(result['reportId'],self.call('GET',path+'/result',token=self.alice)[1]['data']['reportId'])
        body=self.payload();body['name']='Edited';body['indicators'][0]['amount']=100
        self.assertEqual(self.call('PUT',path,body,self.alice)[1]['data']['total_value'],100.2)
        copy_id=self.call('POST',path+'/duplicate',token=self.alice)[1]['data']['id']
        self.assertEqual(self.call('GET',f'/api/evaluations/{copy_id}',token=self.alice)[0],200)
        self.call('DELETE',path,token=self.alice)
        self.assertEqual(self.call('GET',path,token=self.alice)[0],404)

    def test_invalid_amounts_and_duplicate_items(self):
        for amount in [-1,'NaN','Infinity',.001,1000000000001]:
            body=self.payload();body['indicators'][0]['amount']=amount
            with self.subTest(amount=amount):
                self.assertEqual(self.call('POST','/api/evaluations',body,self.alice)[0],422)
        body=self.payload();body['indicators']*=2
        self.assertEqual(self.call('POST','/api/evaluations',body,self.alice)[0],422)
        body=self.payload();body['indicators'][0]['category']=10
        self.assertEqual(self.call('POST','/api/evaluations',body,self.alice)[0],422)
        body=self.payload();body['indicators']=[]
        self.assertEqual(self.call('POST','/api/evaluations',body,self.alice)[0],422)

    def test_limits(self):
        for query in ['page=0','pageSize=0','pageSize=101']:
            self.assertEqual(self.call('GET','/api/evaluations?'+query,token=self.alice)[0],422)
        body=self.payload();body['name']='x'*201
        self.assertEqual(self.call('POST','/api/evaluations',body,self.alice)[0],422)
        body=self.payload();body['indicators']=[dict(category=1,item_name=str(i)+'x'*195,amount=1) for i in range(30)]
        self.assertEqual(self.call('POST','/api/evaluations',body,self.alice)[0],422)

    def test_user_deletion_does_not_orphan_evaluations(self):
        self.create()
        with SessionLocal() as db:
            user_id=db.query(UserTable).filter_by(username='alice').one().id
        self.assertEqual(self.call('DELETE',f'/api/admin/users/{user_id}',token=self.admin)[0],409)

    def test_restart_persists_sessions_and_weights(self):
        self.assertEqual(self.call('PUT','/api/admin/weights',{'1':1.75},self.admin)[0],200)
        self.stop_server();self.start_server()
        self.assertEqual(self.call('GET','/api/user/info',token=self.alice)[0],200)
        self.assertEqual(self.call('GET','/api/admin/weights',token=self.admin)[1]['data']['1'],1.75)
        eid=self.create()
        self.assertEqual(self.call('GET',f'/api/evaluations/{eid}',token=self.alice)[1]['data']['totalValue'],.3)

    def test_weight_validation_atomic(self):
        for weights in [{'1':2,'2':-1},{'10':1},{'1':'bad'},{'1':True},{'1':4}]:
            self.assertEqual(self.call('PUT','/api/admin/weights',weights,self.admin)[0],422)
            self.assertEqual(self.call('GET','/api/admin/weights',token=self.admin)[1]['data']['1'],1)

if __name__=='__main__':
    unittest.main()
