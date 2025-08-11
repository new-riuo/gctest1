from datetime import datetime
from . import db

class QualityRecord(db.Model):
    """质量管理记录模型"""
    id = db.Column(db.Integer, primary_key=True)
    record_number = db.Column(db.String(50), unique=True, nullable=False)
    product_model = db.Column(db.String(50))
    batch_number = db.Column(db.String(50))
    inspection_date = db.Column(db.DateTime, default=datetime.utcnow)
    inspector_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    inspector = db.relationship('User', backref=db.backref('quality_inspections', lazy=True))
    inspection_type = db.Column(db.String(50))
    results = db.Column(db.JSON)
    status = db.Column(db.String(20))
    comments = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<QualityRecord {self.record_number}>'