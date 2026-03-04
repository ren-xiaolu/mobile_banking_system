"""
    数据的增删改查
"""
from config.setting import USER_DATA_PATH
import json
import os


# 保存用户信息
def save_data(user_info):
    phone_number = user_info['phone_number']  # phone_number为关键字
    with open(f'{USER_DATA_PATH}\{phone_number}.json', 'w', encoding='utf-8') as f:
        json.dump(user_info, f)


# 查找用户信息，查找成功返回用户数据
def select_data(phone_number):
    user = f'{USER_DATA_PATH}/{phone_number}.json'
    if os.path.exists(user):
        with open(user, 'r', encoding='utf-8') as f:
            user_data = json.load(f)  # 将json格式转换成python格式
            return user_data
    return None


# 删除用户信息
def delete_data(phone_number):
    user = f'{USER_DATA_PATH}/{phone_number}.json'
    if os.path.exists(user):
        os.remove(user)
        return True
    return False
