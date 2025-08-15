from datetime import datetime
from . import db

class Equipment(db.Model):
    """设备管理模型"""
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50))
    specification = db.Column(db.String(100))
    status = db.Column(db.String(20), default='active')
    location = db.Column(db.String(100))
    purchase_date = db.Column(db.Date)
    last_maintenance_date = db.Column(db.Date)
    next_maintenance_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.String(50))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = db.Column(db.String(50))

    def __repr__(self):
        return f'<Equipment {self.name}>'