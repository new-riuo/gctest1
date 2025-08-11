from app import app, db
from models import User, Role
from werkzeug.security import generate_password_hash

with app.app_context():
    # 检查是否存在admin角色
    admin_role = Role.query.filter_by(name='admin').first()
    if not admin_role:
        admin_role = Role(name='admin', description='管理员角色')
        db.session.add(admin_role)
        db.session.commit()
    
    # 检查是否存在admin用户
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        # 创建admin用户
        admin_user = User(
            username='admin',
            email='admin@example.com',
            password_hash=generate_password_hash('Admin123'),  # 符合密码强度要求的密码
            full_name='管理员',
            role_id=admin_role.id,
            status='active'
        )
        db.session.add(admin_user)
        db.session.commit()
    else:
        # 确保admin用户状态为active
        if admin_user.status != 'active':
            admin_user.status = 'active'
            db.session.commit()
    
    print('管理员账户已创建或激活成功')