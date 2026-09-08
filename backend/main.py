"""HealthData-Valuator HTTP API. Run with uvicorn main:app."""
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
import json
import logging
import math
import secrets

from fastapi import FastAPI, Depends, Header, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import func, text, inspect
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import engine, SessionLocal, Base
from app.core.security import hash_password, verify_password, token_digest, PREFIX
from app.core.indicator_labels import INDICATOR_LABELS
from app.models.models import User as UserTable, Evaluation as EvaluationTable, LoginSession, WeightSetting
from app.schemas.schemas import (UserRegister, UserLogin, AdminUserCreate, AdminUserUpdate,
                                UserProfileUpdate, EvaluationCreate, EvaluationUpdate)
from app.crud.crud import owned_evaluation, serialize_indicators


@asynccontextmanager
async def lifespan(app):
    # Fail visibly on startup rather than serving a falsely healthy API.
    Base.metadata.create_all(bind=engine)
    inspector = inspect(engine)
    for model in (UserTable, EvaluationTable):
        actual = {c['name'] for c in inspector.get_columns(model.__tablename__)}
        missing = set(model.__table__.columns.keys()) - actual
        if missing:
            raise RuntimeError(f"数据库表 {model.__tablename__} 缺少字段 {sorted(missing)}；请先核对迁移说明，不要重建或删除旧表。")
    yield


app = FastAPI(title='HealthData-Valuator API', version='2.1.0', lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=settings.CORS_ORIGINS,
                   allow_credentials=False, allow_methods=['GET', 'POST', 'PUT', 'DELETE'],
                   allow_headers=['Authorization', 'Content-Type'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


@app.exception_handler(IntegrityError)
async def integrity_error(request, exc):
    return JSONResponse(status_code=409, content={'detail': '数据已存在或与已有记录冲突'})


@app.exception_handler(SQLAlchemyError)
async def database_error(request, exc):
    logging.getLogger(__name__).error('Database operation failed (%s)', type(exc).__name__)
    return JSONResponse(status_code=503, content={'detail': '数据库暂不可用，请稍后重试'})


def get_current_username(authorization: str | None = Header(None), db: Session = Depends(get_db)):
    if not authorization or not authorization.startswith('Bearer '):
        raise HTTPException(401, '请先登录')
    token = authorization[7:]
    session = db.get(LoginSession, token_digest(token))
    if not session or session.expires_at <= datetime.utcnow():
        raise HTTPException(401, '登录已过期，请重新登录')
    if not db.query(UserTable).filter(UserTable.username == session.username).first():
        raise HTTPException(401, '账号已失效')
    return session.username


def require_admin(username: str = Depends(get_current_username)):
    if username != 'admin':
        raise HTTPException(403, '需要管理员权限')
    return username


def user_info(user):
    return dict(id=user.id, username=user.username, hospital=user.hospital or '',
                phone=user.phone or '', email=user.email or '')


def revoke_sessions(db, username):
    db.query(LoginSession).filter(LoginSession.username == username).delete()


@app.get('/')
def root(db: Session = Depends(get_db)):
    db.execute(text('SELECT 1'))
    return {'status': 'online', 'message': '数据库连接正常'}


@app.post('/api/auth/register')
def register(body: UserRegister, db: Session = Depends(get_db)):
    if body.username.lower() == 'admin':
        raise HTTPException(403, '管理员账号不能通过公开注册创建')
    if db.query(UserTable).filter(UserTable.username == body.username).first():
        raise HTTPException(400, '用户名已存在')
    db.add(UserTable(**{**body.model_dump(), 'password': hash_password(body.password)}))
    db.commit()
    return {'code': 0, 'message': '注册成功，请登录'}


@app.post('/api/auth/login')
def login(body: UserLogin, db: Session = Depends(get_db)):
    user = db.query(UserTable).filter(UserTable.username == body.username).first()
    if not user or not verify_password(body.password, user.password):
        raise HTTPException(401, '用户名或密码错误')
    if not user.password.startswith(PREFIX):
        user.password = hash_password(body.password)
    # Store only token digests; all workers share sessions and expiry in the DB.
    db.query(LoginSession).filter(LoginSession.expires_at <= datetime.utcnow()).delete()
    token = secrets.token_urlsafe(32)
    db.add(LoginSession(token_hash=token_digest(token), username=user.username,
                        expires_at=datetime.utcnow() + timedelta(hours=settings.SESSION_HOURS)))
    db.commit()
    return {'code': 0, 'data': {'token': token, 'user_info': user_info(user)}}


@app.post('/api/auth/logout')
def logout(authorization: str | None = Header(None), db: Session = Depends(get_db)):
    if authorization and authorization.startswith('Bearer '):
        db.query(LoginSession).filter(LoginSession.token_hash == token_digest(authorization[7:])).delete()
        db.commit()
    return {'code': 0, 'message': '已退出登录'}


@app.get('/api/user/info')
def get_user_info(db: Session = Depends(get_db), username: str = Depends(get_current_username)):
    return {'code': 0, 'data': user_info(db.query(UserTable).filter(UserTable.username == username).one())}


@app.put('/api/user/info')
def update_user_info(body: UserProfileUpdate, db: Session = Depends(get_db), username: str = Depends(get_current_username)):
    user = db.query(UserTable).filter(UserTable.username == username).one()
    for key, value in body.model_dump(exclude_none=True).items():
        setattr(user, key, value)
    db.commit()
    return {'code': 0, 'data': user_info(user)}


INDICATOR_CATEGORY_NAMES = {
    1: '数据战略与治理成本', 2: '数据获取与采集成本', 3: '数据存储与备份成本',
    4: '数据处理与加工成本', 5: '数据应用与分析成本', 6: '数据流通与共享成本',
    7: '数据安全、隐私与合规成本', 8: '数据归档与销毁成本', 9: '数据全流程人力成本'
}


@app.get('/api/indicators')
def indicators():
    return {'code': 0, 'data': {'categories': [dict(id=i, name=n) for i, n in INDICATOR_CATEGORY_NAMES.items()]}}


@app.post('/api/evaluations')
def create_evaluation(body: EvaluationCreate, db: Session = Depends(get_db), username: str = Depends(get_current_username)):
    payload, total = serialize_indicators(body.indicators)
    record = EvaluationTable(name=body.name, description=body.description, indicators=payload,
                             total_value=total, username=username, status='completed',
                             created_at=datetime.now().isoformat())
    db.add(record)
    db.commit()
    return {'code': 0, 'data': {'id': record.id, 'total_value': record.total_value}}


@app.get('/api/evaluations/stats')
def evaluation_stats(db: Session = Depends(get_db), username: str = Depends(get_current_username)):
    q = db.query(EvaluationTable).filter(EvaluationTable.username == username)
    total = q.with_entities(func.sum(EvaluationTable.total_value)).scalar() or 0
    count = q.count()
    return {'code': 0, 'data': dict(total_count=count, total_value=round(total, 2),
                                   average_value=round(total / count, 2) if count else 0)}


@app.get('/api/evaluations')
def list_evaluations(page: int = Query(1, ge=1), pageSize: int = Query(10, ge=1, le=100),
                     status: str | None = None, keyword: str | None = None,
                     scope: str = Query('mine', pattern='^(mine|all)$'),
                     db: Session = Depends(get_db), username: str = Depends(get_current_username)):
    q = db.query(EvaluationTable)
    if scope == 'all':
        if username != 'admin':
            raise HTTPException(403, '需要管理员权限')
    else:
        q = q.filter(EvaluationTable.username == username)
    if keyword:
        q = q.filter(EvaluationTable.name.contains(keyword, autoescape=True))
    if status and status != 'all':
        q = q.filter(EvaluationTable.status == status)
    count = q.count()
    records = q.order_by(EvaluationTable.id.desc()).offset((page - 1) * pageSize).limit(pageSize).all()
    return {'code': 0, 'data': {'total': count, 'list': [dict(id=e.id, name=e.name,
            description=e.description, totalValue=e.total_value, createdAt=e.created_at, status=e.status)
            for e in records]}}


@app.get('/api/evaluations/{eval_id}')
def get_evaluation(eval_id: int, db: Session = Depends(get_db), username: str = Depends(get_current_username)):
    e = owned_evaluation(db, eval_id, username)
    return {'code': 0, 'data': dict(id=e.id, name=e.name, description=e.description,
            totalValue=e.total_value, createdAt=e.created_at, status=e.status, indicators=json.loads(e.indicators or '[]'))}


def _build_result_from_eval(e, hospital=''):
    raw = json.loads(e.indicators or '[]')
    total = float(e.total_value or 0)
    details = []
    for item in raw:
        cat = int(item.get('category', 1))
        amount = float(item.get('amount', 0))
        details.append(dict(categoryId=cat, categoryName=INDICATOR_CATEGORY_NAMES.get(cat, '其他'),
                            itemName=INDICATOR_LABELS.get(item.get('item_name'), item.get('item_name', '')),
                            amount=amount, percentage=round(amount / total * 100, 2) if total else 0,
                            description=''))
    categories = []
    for cat in sorted(set(d['categoryId'] for d in details)):
        rows = [d for d in details if d['categoryId'] == cat]
        categories.append(dict(id=cat, name=INDICATOR_CATEGORY_NAMES.get(cat, '其他'),
                               value=round(sum(d['amount'] for d in rows), 2), details=rows))
    return dict(id=e.id, reportId=f'REPORT-{e.id}', hospital=hospital, createdAt=e.created_at,
                name=e.name, status=e.status or 'completed', totalValue=total,
                categories=categories, details=details)


@app.get('/api/evaluations/{eval_id}/result')
def get_result(eval_id: int, db: Session = Depends(get_db), username: str = Depends(get_current_username)):
    e = owned_evaluation(db, eval_id, username)
    owner = db.query(UserTable).filter(UserTable.username == e.username).first()
    return {'code': 0, 'data': _build_result_from_eval(e, owner.hospital if owner else '')}


@app.put('/api/evaluations/{eval_id}')
def update_evaluation(eval_id: int, body: EvaluationUpdate, db: Session = Depends(get_db), username: str = Depends(get_current_username)):
    e = owned_evaluation(db, eval_id, username)
    if body.indicators is not None:
        e.indicators, e.total_value = serialize_indicators(body.indicators)
    if body.name is not None:
        e.name = body.name
    if body.description is not None:
        e.description = body.description
    db.commit()
    return {'code': 0, 'data': dict(id=e.id, total_value=e.total_value)}


@app.delete('/api/evaluations/{eval_id}')
def delete_evaluation(eval_id: int, db: Session = Depends(get_db), username: str = Depends(get_current_username)):
    db.delete(owned_evaluation(db, eval_id, username))
    db.commit()
    return {'code': 0, 'message': '删除成功'}


@app.post('/api/evaluations/{eval_id}/submit')
def submit_evaluation(eval_id: int, db: Session = Depends(get_db), username: str = Depends(get_current_username)):
    e = owned_evaluation(db, eval_id, username)
    e.status = 'completed'
    db.commit()
    return {'code': 0, 'data': {'id': e.id}}


@app.post('/api/evaluations/{eval_id}/duplicate')
def duplicate_evaluation(eval_id: int, db: Session = Depends(get_db), username: str = Depends(get_current_username)):
    e = owned_evaluation(db, eval_id, username)
    copy = EvaluationTable(name=e.name[:195] + ' (副本)', description=e.description,
                           total_value=e.total_value, indicators=e.indicators, username=username,
                           created_at=datetime.now().isoformat(), status=e.status)
    db.add(copy)
    db.commit()
    return {'code': 0, 'data': {'id': copy.id}}


@app.get('/api/admin/users')
def list_users(page: int = Query(1, ge=1), pageSize: int = Query(20, ge=1, le=100), keyword: str | None = None,
               db: Session = Depends(get_db), _: str = Depends(require_admin)):
    q = db.query(UserTable)
    if keyword:
        q = q.filter(UserTable.username.contains(keyword, autoescape=True) | UserTable.hospital.contains(keyword, autoescape=True))
    count = q.count()
    return {'code': 0, 'data': {'total': count, 'list': [user_info(u) for u in
            q.order_by(UserTable.id.desc()).offset((page - 1) * pageSize).limit(pageSize).all()]}}


@app.post('/api/admin/users')
def create_user(body: AdminUserCreate, db: Session = Depends(get_db), _: str = Depends(require_admin)):
    if db.query(UserTable).filter(UserTable.username == body.username).first():
        raise HTTPException(400, '用户名已存在')
    u = UserTable(**{**body.model_dump(), 'password': hash_password(body.password)})
    db.add(u)
    db.commit()
    return {'code': 0, 'data': user_info(u)}


def find_user(db, user_id):
    u = db.get(UserTable, user_id)
    if not u:
        raise HTTPException(404, '用户不存在')
    return u


@app.get('/api/admin/users/{user_id}')
def get_user(user_id: int, db: Session = Depends(get_db), _: str = Depends(require_admin)):
    return {'code': 0, 'data': user_info(find_user(db, user_id))}


@app.put('/api/admin/users/{user_id}')
def update_user(user_id: int, body: AdminUserUpdate, db: Session = Depends(get_db), _: str = Depends(require_admin)):
    u = find_user(db, user_id)
    for key, value in body.model_dump(exclude_none=True).items():
        if key == 'password':
            value = hash_password(value)
            revoke_sessions(db, u.username)
        setattr(u, key, value)
    db.commit()
    return {'code': 0, 'data': user_info(u)}


@app.delete('/api/admin/users/{user_id}')
def delete_user(user_id: int, db: Session = Depends(get_db), _: str = Depends(require_admin)):
    u = find_user(db, user_id)
    if u.username == 'admin':
        raise HTTPException(400, '不能删除管理员账号')
    if db.query(EvaluationTable).filter(EvaluationTable.username == u.username).first():
        raise HTTPException(409, '该用户仍有评估记录，请先处理评估记录再删除账号')
    revoke_sessions(db, u.username)
    db.delete(u)
    db.commit()
    return {'code': 0, 'message': '已删除'}


@app.get('/api/admin/stats')
def admin_stats(db: Session = Depends(get_db), _: str = Depends(require_admin)):
    count = db.query(EvaluationTable).count()
    total = db.query(func.sum(EvaluationTable.total_value)).scalar() or 0
    return {'code': 0, 'data': dict(total_evaluations=count, total_market_value=round(total, 2),
            total_value=round(total, 2), average_value=round(total / count, 2) if count else 0,
            total_users=db.query(UserTable).count())}


def read_weights(db):
    values = {str(i): 1.0 for i in range(1, 10)}
    values.update({str(w.category): w.value for w in db.query(WeightSetting).all()})
    return values


@app.get('/api/admin/weights')
def get_weights(db: Session = Depends(get_db), _: str = Depends(require_admin)):
    return {'code': 0, 'data': read_weights(db)}


@app.put('/api/admin/weights')
def update_weights(weights: dict, db: Session = Depends(get_db), _: str = Depends(require_admin)):
    for key, value in weights.items():
        if key not in {str(i) for i in range(1, 10)} or isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not 0 <= value <= 3:
            raise HTTPException(422, '权重类别必须为1至9，数值必须在0至3之间')
    for key, value in weights.items():
        record = db.get(WeightSetting, int(key))
        if record:
            record.value = value
        else:
            db.add(WeightSetting(category=int(key), value=value))
    db.commit()
    return {'code': 0, 'message': '参考权重已保存；当前报告仍采用直接相加法', 'data': read_weights(db)}


@app.post('/api/demo/init')
def init_demo(db: Session = Depends(get_db), username: str = Depends(require_admin)):
    if not settings.ENABLE_DEMO:
        raise HTTPException(403, '演示初始化未启用')
    name = '系统演示评估'
    if not db.query(EvaluationTable).filter_by(name=name, username=username, description='演示数据').first():
        db.add(EvaluationTable(name=name, username=username, description='演示数据', total_value=100,
                               indicators='[{"category":1,"item_name":"strategicPlanning","amount":100}]',
                               created_at=datetime.now().isoformat(), status='completed'))
        db.commit()
    return {'code': 0, 'message': '演示评估已就绪（不会创建默认密码账号）'}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)
