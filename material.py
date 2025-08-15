from datetime import datetime
from . import db

class RawMaterial(db.Model):
    """原材料信息模型"""
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50))
    specification = db.Column(db.String(100))
    unit = db.Column(db.String(20))
    supplier = db.Column(db.String(100))
    safety_stock = db.Column(db.Float, default=0)
    status = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<RawMaterial {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'type': self.type,
            'specification': self.specification,
            'unit': self.unit,
            'supplier': self.supplier,
            'safety_stock': self.safety_stock,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class RawMaterialInventory(db.Model):
    """原材料库存模型"""
    __tablename__ = 'raw_material_inventory'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    raw_material_id = db.Column(db.Integer, db.ForeignKey('raw_material.id', name='fk_raw_material_inventory_raw_material'), nullable=False)
    raw_material = db.relationship('RawMaterial', backref=db.backref('inventory', lazy=True))
    quantity = db.Column(db.Float, default=0)
    location = db.Column(db.String(100))
    minimum_stock = db.Column(db.Float, default=0)
    maximum_stock = db.Column(db.Float, default=0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_check_date = db.Column(db.Date)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<RawMaterialInventory {self.raw_material.name if self.raw_material else "Unknown"} - {self.quantity}>'

    def to_dict(self):
        return {
            'id': self.id,
            'raw_material_id': self.raw_material_id,
            'raw_material_name': self.raw_material.name if self.raw_material else "Unknown",
            'quantity': self.quantity,
            'location': self.location,
            'minimum_stock': self.minimum_stock,
            'maximum_stock': self.maximum_stock,
            'last_updated': self.last_updated.strftime('%Y-%m-%d %H:%M:%S') if self.last_updated else None,
            'last_check_date': self.last_check_date.strftime('%Y-%m-%d') if self.last_check_date else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }


class MaterialTransaction(db.Model):
    """原材料交易记录（入库/出库）"""
    id = db.Column(db.Integer, primary_key=True)
    transaction_type = db.Column(db.String(20), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('raw_material.id'), nullable=False)
    material = db.relationship('RawMaterial', backref=db.backref('transactions', lazy=True))
    quantity = db.Column(db.Float, nullable=False)
    batch_number = db.Column(db.String(50))
    transaction_date = db.Column(db.DateTime, default=datetime.utcnow)
    operator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    operator = db.relationship('User', backref=db.backref('material_transactions', lazy=True))
    notes = db.Column(db.Text)

    def __repr__(self):
        return f'<MaterialTransaction {self.transaction_type}: {self.material.name}>'