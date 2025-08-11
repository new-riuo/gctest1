from app import app, db
from models import User
from werkzeug.security import check_password_hash

with app.app_context():
    # 检查是否存在admin用户
    admin_user = User.query.filter_by(username='admin').first()
    
    if not admin_user:
        print('错误: 数据库中不存在admin用户')
    else:
        print('信息: admin用户存在')
        print(f'用户名: {admin_user.username}')
        print(f'邮箱: {admin_user.email}')
        print(f'状态: {admin_user.status}')
        print(f'角色: {admin_user.role.name if admin_user.role else None}')
        
        # 验证密码
        password_to_check = 'admin123'
        if check_password_hash(admin_user.password_hash, password_to_check):
            print(f'密码验证: 成功 (使用密码: {password_to_check})')
        else:
            print(f'密码验证: 失败 (尝试密码: {password_to_check})')
            print('提示: 可能密码已更改或使用了其他密码')
    
    # 检查是否存在其他管理员角色的用户
    admin_role_users = User.query.filter(User.role.has(name='admin')).all()
    if len(admin_role_users) > 1:
        print(f'信息: 发现{len(admin_role_users)}个具有管理员角色的用户')
        for user in admin_role_users:
            print(f'- {user.username} ({user.email})')