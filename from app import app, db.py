from app import app, db
from models import User

with app.app_context():
    # 添加字段
    db.session.execute('ALTER TABLE user ADD COLUMN department_id INTEGER')
    # 添加外键约束
    db.session.execute('ALTER TABLE user ADD CONSTRAINT fk_user_department FOREIGN KEY (department_id) REFERENCES department (id)')
    db.session.commit()

department_id = db.Column(db.Integer, db.ForeignKey('department.id'))