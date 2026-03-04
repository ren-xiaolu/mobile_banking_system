"""
    用户的业务逻辑
"""
from db import db_handle
from lib import common


def register_info(phone_number, name, password):
    """处理用户注册逻辑"""
    # 生成用户数据
    user_info = {
        "name": name,
        "phone_number": phone_number,
        "password": password,
        'balance': 0,
        'bill': [],
    }
    # 判断手机号是否已注册
    user_data = db_handle.select_data(phone_number)
    if user_data != None:
        return False, "该手机号已注册，请登录"
    db_handle.save_data(user_info)  # 不存在，则保存用户信息
    return True, f"{name}注册成功"


def login_info(phone_number, password):
    """处理用户登录逻辑"""
    # 查看用户是否存在
    user_data = db_handle.select_data(phone_number)
    if user_data:
        # 判断密码是否一致
        if password == user_data['password']:
            msg = common.nowtime()
            return 1, f'{msg}好，{user_data["name"]}'
        return 2, '密码错误，请重新输入'
    else:
        return 3, "用户不存在，请先注册"


def check_money_info(phone_number):
    """处理查看余额逻辑"""
    user_data = db_handle.select_data(phone_number)
    return user_data['name'], user_data['balance']


def change_password_info(phone_number, old_password, new_password):
    """处理更改密码逻辑"""
    # 原密码是否正确
    user_data = db_handle.select_data(phone_number)
    if old_password == user_data['password']:
        # 更改密码
        user_data['password'] = new_password
        # 保存更改数据
        db_handle.save_data(user_data)
        return True


def delete_user_info(phone_number):
    """处理注销用户逻辑"""
    flag = db_handle.delete_data(phone_number)
    return flag
