"""
    自定义的功能模块
"""
from core import src
from datetime import datetime


def is_login(func):
    def check(*args, **kwargs):
        if src.login_status:
            res = func()
            return res
        else:
            print("请先登录!")
            src.login()

    return check


def nowtime():
    hour = datetime.now().hour
    if 6 <= hour < 12:
        return "早上"
    if 12 <= hour < 18:
        return "下午"
    else:
        return "晚上"
