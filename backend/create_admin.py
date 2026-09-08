"""Create the initial administrator locally; never expose a bootstrap HTTP route."""
from getpass import getpass
from app.core.database import Base, engine, SessionLocal
from app.models.models import User
from app.core.security import hash_password

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    with SessionLocal() as db:
        if db.query(User).filter_by(username='admin').first():
            raise SystemExit('管理员已存在，未修改。')
        password = getpass('管理员密码（至少 12 位）：')
        if len(password) < 12 or password != getpass('再次输入密码：'):
            raise SystemExit('密码过短或两次输入不一致，未创建。')
        db.add(User(username='admin', password=hash_password(password), hospital='系统管理员'))
        db.commit()
        print('管理员创建成功。')
