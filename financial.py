from datetime import datetime
from . import db

class FinancialRecord(db.Model):
    """财务管理记录模型"""
    id = db.Column(db.Integer, primary_key=True)
    record_number = db.Column(db.String(50), unique=True, nullable=False)
    record_date = db.Column(db.DateTime, default=datetime.utcnow)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), default='CNY')
    record_type = db.Column(db.String(50))
    category = db.Column(db.String(50))
    description = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    creator = db.relationship('User', backref=db.backref('financial_records', lazy=True))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<FinancialRecord {self.record_number}>'