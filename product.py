from datetime import datetime
from . import db

class Product(db.Model):
    """产品模型"""
    id = db.Column(db.Integer, primary_key=True)
    erp_product_id = db.Column(db.String(50), unique=True, nullable=False)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(50))
    category = db.Column(db.String(50))
    unit = db.Column(db.String(20))
    purchase_price = db.Column(db.Float)
    selling_price = db.Column(db.Float)
    stock_quantity = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Product {self.name} ({self.sku})>'

    def to_dict(self):
        return {
            'id': self.id,
            'erp_product_id': self.erp_product_id,
            'sku': self.sku,
            'name': self.name,
            'model': self.model,
            'category': self.category,
            'unit': self.unit,
            'purchase_price': self.purchase_price,
            'selling_price': self.selling_price,
            'stock_quantity': self.stock_quantity,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }