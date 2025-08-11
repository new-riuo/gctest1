import re  # 添加re模块导入
from datetime import datetime

from flask import Flask, render_template, redirect, url_for, flash, session, Blueprint
from flask import jsonify, request
from flask_wtf import FlaskForm, CSRFProtect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate  # 添加此行导入Flask-Migrate
from sqlalchemy.orm import joinedload
from werkzeug.security import generate_password_hash, check_password_hash

from dashboard.views import dashboard
from models import db, ProductionPlan, User, Role, Department, ProcessingMaterial, MaterialTransaction, \
    ProcessingRecord, RawMaterialInventory, RawMaterial, ProcessedProduct
from blueprints.auth import auth_bp
from blueprints.user import user_bp
from blueprints.department import dept_bp
from blueprints.role import role_bp
from blueprints.production import production_bp
from blueprints.material import material_bp  # 保留这一行导入
from blueprints.system import system_bp
# 删除这一行导入
# from blueprints import material_routes
from decorators import validate_content_type, api_login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
csrf = CSRFProtect(app)

# 为API路由添加CSRF例外
csrf.exempt(auth_bp)


# 初始化Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'  # 指定登录路由

# Add user loader callback
@login_manager.user_loader
def load_user(user_id): 
    # Assuming User model has an id field that matches user_id
    return db.session.get(User, int(user_id))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///production_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
# 添加此行初始化迁移
migrate = Migrate(app, db)

app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(role_bp)
app.register_blueprint(dept_bp)
app.register_blueprint(material_bp)  # 保留这一行注册
app.register_blueprint(production_bp)
# 删除以下两行重复代码
# 创建物料管理蓝图
# material_bp = Blueprint('material', __name__)

# 导入路由（确保路由定义在蓝图创建之后）
# from blueprints import material_routes

# app.register_blueprint(material_bp)

# 注册系统管理蓝图
app.register_blueprint(system_bp)
@app.route('/create-user', endpoint='create_user_page')
def create_user():
    return render_template('user-management-pages/register.html')  # 渲染用户创建页面模板



# 获取当前用户信息API
@app.route('/api/user/info', methods=['GET'])
@login_required
def api_get_user_info():
    try:
        user_data = {
            'id': current_user.id,
            'username': current_user.username,
            'email': current_user.email,
            'role': {'name': current_user.role.name} if current_user.role else None,
            'department': {'name': current_user.department.name} if current_user.department else None
        }
        return jsonify({'success': True, 'user': user_data})
    except Exception as e:
        app.logger.error(f"获取用户信息失败: {str(e)}")
        return jsonify({'success': False, 'message': '获取用户信息失败'}), 500

# 恢复index路由定义
@app.route('/index')
def index():
    return render_template('index.html')

# 应用入口
if __name__ == '__main__':
    # 打印所有注册的路由
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint}: {rule.rule}")
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)

# 原材料库存页面路由
@app.route('/raw-material-inventory')
@login_required
def raw_material_inventory():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        pagination = RawMaterialInventory.query.join(RawMaterial).paginate(page=page, per_page=per_page)
        inventories = pagination.items
        return render_template('raw-material-pages/raw-material-inventory.html', 
                             inventories=inventories, pagination=pagination)
    except Exception as e:
        app.logger.error(f"原材料库存页面错误: {str(e)}")
        flash('获取库存列表失败，请稍后重试', 'danger')
        return render_template('raw-material-pages/raw-material-inventory.html', 
                             inventories=[], pagination=None)

# 原材料加工记录页面路由
@app.route('/processing-records')
@login_required
def processing_records():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        pagination = ProcessingRecord.query.paginate(page=page, per_page=per_page)
        records = pagination.items
        return render_template('processing-pages/processing-records.html', 
                             records=records, pagination=pagination)
    except Exception as e:
        app.logger.error(f"加工记录页面错误: {str(e)}")
        flash('获取加工记录失败，请稍后重试', 'danger')
        return render_template('processing-pages/processing-records.html', 
                             records=[], pagination=None)

# 新增加工单页面路由
@app.route('/new-processing-record')
@login_required
def new_processing_record():
    materials = RawMaterial.query.filter_by(status=True).all()
    plans = ProductionPlan.query.filter(
        ProductionPlan.end_date >= datetime.now().date()
    ).all()
    return render_template('processing-pages/new-processing-record.html',
                         materials=materials, plans=plans)


# 加工记录API
@app.route('/api/processing-records', methods=['GET'])
@login_required
def get_processing_records():
    records = ProcessingRecord.query.all()
    result = []
    for record in records:
        result.append({
            'id': record.id,
            'processing_no': record.processing_no,
            'production_plan': record.production_plan.plan_number if record.production_plan else None,
            'processing_date': record.processing_date.strftime('%Y-%m-%d %H:%M:%S'),
            'completion_date': record.completion_date.strftime('%Y-%m-%d %H:%M:%S') if record.completion_date else None,
            'status': record.status,
            'operator': record.operator.username if record.operator else None,
            'department': record.department.name if record.department else None
        })
    return jsonify(result)

@app.route('/api/processing-records', methods=['POST'])
@login_required
@validate_content_type
def create_processing_record():
    data = request.get_json()
    
    # 参数校验
    if not data or 'materials' not in data or 'products' not in data:
        return jsonify({'message': '请求参数不完整，缺少materials或products'}), 400
    
    if not isinstance(data['materials'], list) or len(data['materials']) == 0:
        return jsonify({'message': 'materials必须是非空数组'}), 400
    
    if not isinstance(data['products'], list) or len(data['products']) == 0:
        return jsonify({'message': 'products必须是非空数组'}), 400
    
    # 生成加工单号
    processing_no = f"PROC-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # 创建加工记录
    record = ProcessingRecord(
        processing_no=processing_no,
        production_plan_id=data.get('production_plan_id'),
        operator_id=current_user.id,
        department_id=data.get('department_id'),
        notes=data.get('notes', '')
    )
    
    # 添加原材料明细并检查库存
    for material in data['materials']:
        if 'id' not in material or 'quantity' not in material:
            return jsonify({'message': '原材料信息不完整，缺少id或quantity'}), 400
        
        try:
            quantity = float(material['quantity'])
            if quantity <= 0:
                return jsonify({'message': '原材料数量必须大于0'}), 400
        except ValueError:
            return jsonify({'message': '原材料数量必须是有效的数字'}), 400
    
        mat = RawMaterial.query.get_or_404(material['id'])
        quantity = float(material['quantity'])
        
        # 检查库存
        inventory = RawMaterialInventory.query.filter_by(material_id=mat.id).first()
        if not inventory or inventory.quantity < quantity:
            db.session.rollback()
            return jsonify({
                'message': f'原材料 "{mat.name}" 库存不足，无法创建加工单'
            }), 400
        
        # 创建加工原材料记录
        processing_mat = ProcessingMaterial(
            processing=record,
            material=mat,
            quantity=quantity,
            unit=mat.unit
        )
        db.session.add(processing_mat)
        
        # 自动创建出库记录
        outbound = MaterialTransaction(
            transaction_type='outbound',
            material=mat,
            quantity=quantity,
            batch_number=data.get('batch_number', ''),
            operator_id=current_user.id,
            notes=f'用于加工: {processing_no}'
        )
        db.session.add(outbound)
        
        # 减少库存
        inventory.quantity -= quantity
    
    # 添加成品记录
    for product in data['products']:
        if 'model' not in product or 'quantity' not in product:
            return jsonify({'message': '成品信息不完整，缺少model或quantity'}), 400
        
        try:
            quantity = float(product['quantity'])
            if quantity <= 0:
                return jsonify({'message': '成品数量必须大于0'}), 400
        except ValueError:
            return jsonify({'message': '成品数量必须是有效的数字'}), 400
    
        processed_product = ProcessedProduct(
            processing=record,
            product_model=product['model'],
            quantity=float(product['quantity']),
            unit=product.get('unit', ''),
            qualified_quantity=float(product.get('qualified_quantity', 0)),
            unqualified_quantity=float(product.get('unqualified_quantity', 0))
        )
        db.session.add(processed_product)
    
    try:
        db.session.add(record)
        db.session.commit()
        return jsonify({
            'message': '加工单创建成功',
            'processing_id': record.id,
            'processing_no': processing_no
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'创建失败: {str(e)}'}), 500

# 更新加工记录状态（完成加工）
@app.route('/api/processing-records/<int:record_id>/complete', methods=['POST'])
@login_required
@validate_content_type
def complete_processing(record_id):
    record = ProcessingRecord.query.get_or_404(record_id)
    
    if record.status == 'completed':
        return jsonify({'message': '该加工单已完成'}), 400
    
    data = request.get_json()
    
    # 更新成品合格/不合格数量
    for product_data in data.get('products', []):
        product = ProcessedProduct.query.filter_by(
            processing_id=record_id,
            product_model=product_data['model']
        ).first()
        
        if product:
            product.qualified_quantity = float(product_data.get('qualified_quantity', 0))
            product.unqualified_quantity = float(product_data.get('unqualified_quantity', 0))
    
    # 更新加工记录状态和完成时间
    record.status = 'completed'
    record.completion_date = datetime.utcnow()
    record.notes = data.get('notes', record.notes)
    
    try:
        db.session.commit()
        return jsonify({'message': '加工单已标记为完成'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'更新失败: {str(e)}'}), 500

@app.route('/material-management/raw-material')
def raw_material_management():
    return render_template('material-management-pages/raw-material-management.html')

@app.route('/create-new-user', endpoint='create_new_user')
def create_new_user():
    return render_template('user-management-pages/create-user.html')

@app.route('/edit-user/<username>', endpoint='edit_user_by_username')
def edit_user(username):
    return render_template('user-management-pages/edit-user.html', username=username)

@app.route('/api/departments/check-code', methods=['GET'])
@api_login_required
def check_department_code():
    from models import Department
    code = request.args.get('code')
    exclude_id = request.args.get('exclude_id', type=int)
    
    query = Department.query.filter_by(code=code)
    if exclude_id:
        query = query.filter(Department.id != exclude_id)
        
    exists = query.first() is not None
    return jsonify({'is_unique': not exists})