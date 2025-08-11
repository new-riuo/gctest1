from functools import wraps
from flask import request, jsonify
from flask_login import current_user

# Content type validation decorator
def validate_content_type(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        content_type = request.headers.get('Content-Type', '')
        if not content_type.startswith('application/json'):
            return jsonify({'message': '请求必须使用JSON格式'}), 400
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

# API login validation decorator
def api_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({'message': '请先登录'}), 401
        return f(*args, **kwargs)
    return decorated_function