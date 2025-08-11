from datetime import datetime
from . import db

class Department(db.Model):
    """部门模型"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.Text)
    parent_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    parent = db.relationship('Department', backref=db.backref('children', lazy=True), remote_side=[id])
    head_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    head = db.relationship('User', foreign_keys=[head_id], backref=db.backref('managed_departments', lazy=True))
    status = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Department {self.name}>'