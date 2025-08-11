from datetime import datetime
from . import db

class ProductionPlan(db.Model):
    """生产计划模型"""
    id = db.Column(db.Integer, primary_key=True)
    plan_number = db.Column(db.String(20), unique=True)
    product_model = db.Column(db.String(20))
    quantity = db.Column(db.Integer)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    responsible_person = db.Column(db.String(20))

    def __repr__(self):
        return f'<ProductionPlan {self.plan_number}>'


class ProcessingRecord(db.Model):
    """原材料加工记录模型"""
    id = db.Column(db.Integer, primary_key=True)
    production_plan_id = db.Column(db.Integer, db.ForeignKey('production_plan.id'))
    production_plan = db.relationship('ProductionPlan', backref=db.backref('processing_records', lazy=True))
    processing_no = db.Column(db.String(50), unique=True, nullable=False)
    processing_date = db.Column(db.DateTime, default=datetime.utcnow)
    completion_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='pending')
    operator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    operator = db.relationship('User', backref=db.backref('processing_records', lazy=True))
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    department = db.relationship('Department', backref=db.backref('processing_records', lazy=True))
    notes = db.Column(db.Text)

    def __repr__(self):
        return f'<ProcessingRecord {self.processing_no}>'


class ProcessingMaterial(db.Model):
    """加工所用原材料明细模型"""
    id = db.Column(db.Integer, primary_key=True)
    processing_id = db.Column(db.Integer, db.ForeignKey('processing_record.id'), nullable=False)
    processing = db.relationship('ProcessingRecord', backref=db.backref('materials', lazy=True))
    material_id = db.Column(db.Integer, db.ForeignKey('raw_material.id'), nullable=False)
    material = db.relationship('RawMaterial')
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20))

    def __repr__(self):
        return f'<ProcessingMaterial {self.material.name}: {self.quantity}{self.unit}>'


class ProcessedProduct(db.Model):
    """加工后成品模型"""
    id = db.Column(db.Integer, primary_key=True)
    processing_id = db.Column(db.Integer, db.ForeignKey('processing_record.id'), nullable=False)
    processing = db.relationship('ProcessingRecord', backref=db.backref('products', lazy=True))
    product_model = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20))
    qualified_quantity = db.Column(db.Float)
    unqualified_quantity = db.Column(db.Float)

    def __repr__(self):
        return f'<ProcessedProduct {self.product_model}: {self.quantity}{self.unit}>'