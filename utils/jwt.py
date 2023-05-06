import time

import jwt

JWT_TOKEN_EXPIRE_TIME = 3600 * 2  # token有效时间 2小时
JWT_SECRET = 'abc'  # 加解密密钥
JWT_ALGORITHM = 'HS256'  # 加解密算法


def generate_jwt_token(user_id: int) -> str:
    """根据用户id生成token"""
    payload = {'user_id': user_id, 'exp': int(time.time()) + JWT_TOKEN_EXPIRE_TIME}
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def verify_jwt_token(user_id: int, token: str) -> bool:
    """验证用户token"""
    payload = {'user_id': user_id}
    try:
        _payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.PyJWTError:
        print('token解析失败')
        return False
    else:
        print(_payload)
        exp = int(_payload.pop('exp'))
        if time.time() > exp:
            print('已失效')
            return False
        return payload == _payload
