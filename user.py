from flask_login import UserMixin
from datetime import datetime
from . import db

class User(UserMixin, db.Model):
    """用户模型"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    full_name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role', backref=db.backref('users', lazy=True))
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    department = db.relationship('Department', foreign_keys=[department_id], backref=db.backref('users', lazy=True))
    status = db.Column(db.String(20))
    last_login = db.Column(db.DateTime)

    def __repr__(self):
        return f'<User {self.username}>'

    def get_id(self):
        return str(self.id)

    @property
    def is_admin(self):
        """检查用户是否为管理员"""
        return self.role and self.role.name == 'admin'

    def has_permission(self, permission_name):
        """检查用户是否有指定权限"""
        if self.is_admin:
            return True
        if not self.role or not self.role.permissions:
            return False
        return permission_name in self.role.permissions