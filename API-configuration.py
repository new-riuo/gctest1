import requests
import json
import time
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64

# API配置参数
APP_KEY = 'd6b8b86b02ca45ed'
SERVICE_ID = 'ECG61B'
APP_SECRET = 'b71e1d924f8c399a'
API_URL = 'http://openapi-web.eccang.com/openApi/api/unity'

# 可选配置参数（根据需要启用）
TOKEN = ''  # 应用的用户授权token
SUBJECT_CODE = ''  # 公司唯一编码

# 生成随机字符串
def generate_nonce_str(length=32):
    import random
    import string
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

# 生成时间戳
def generate_timestamp():
    return int(time.time() * 1000)

# 生成MD5签名
def generate_md5_sign(params, app_secret):
    # 按参数名排序
    sorted_params = sorted(params.items(), key=lambda x: x[0])
    # 拼接参数字符串
    sign_str = '&'.join([f"{k}={v}" for k, v in sorted_params if v and k != 'sign'])
    # 拼接应用密钥
    sign_str += app_secret
    # 计算MD5
    return hashlib.md5(sign_str.encode('utf-8')).hexdigest()

# 发送API请求
def send_api_request(interface_method, biz_content=None, sign_type='MD5'):
    # 准备请求参数
    params = {
        'app_key': APP_KEY,
        'service_id': SERVICE_ID,
        'nonce_str': generate_nonce_str(),
        'interface_method': interface_method,
        'charset': 'UTF-8',
        'timestamp': generate_timestamp(),
        'version': 'v1.0.0',
    }
    
    if biz_content:
        params['biz_content'] = json.dumps(biz_content, ensure_ascii=False)
    
    # 生成签名
    if sign_type == 'MD5':
        params['sign'] = generate_md5_sign(params, APP_SECRET)
    # AES签名生成逻辑省略
    
    params['sign_type'] = sign_type
    
    # 发送请求
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.post(API_URL, json=params, headers=headers)
    
    # 处理响应
    if response.status_code == 200:
        return response.json()
    else:
        return {
            'code': response.status_code,
            'message': f'HTTP错误: {response.status_code}',
            'data': response.text
        }
