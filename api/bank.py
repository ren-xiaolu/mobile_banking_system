"""
银行的业务逻辑
"""
import time
from db import db_handle


def save_money_info(phone_number, money):
    """处理存钱逻辑"""
    # 查看现有余额
    user_data = db_handle.select_data(phone_number)
    balance = user_data['balance']
    # 存款操作
    user_data['balance'] = balance + money
    # 添加流水
    now_time = time.strftime("%Y-%m-%d %H:%M:%S")
    bill_info = f"{now_time} 存款金额:{money}元，账户余额:{user_data['balance']}元"
    user_data['bill'].append(bill_info)
    # 保存更改数据
    db_handle.save_data(user_data)
    # 返回取款结果
    return True, bill_info


def get_money_info(phone_number, money):
    """处理取钱逻辑"""
    # 查看现有余额
    user_data = db_handle.select_data(phone_number)
    balance = user_data['balance']
    # 判断余额是否足够
    if money <= balance:
        # 取款操作
        user_data['balance'] = balance - money
        # 添加流水
        now_time = time.strftime("%Y-%m-%d %H:%M:%S")
        bill_info = f"{now_time} 取款金额:{money}元，账户余额:{user_data['balance']}元"
        user_data['bill'].append(bill_info)
        # 保存更改数据
        db_handle.save_data(user_data)
        return True, bill_info
    else:
        return False, "您的账户余额不足，请重新输入"


def recipient_info(recipient_phone, recipient_name):
    """处理收款人信息逻辑"""
    # 查看收款人手机号和用户名是否符合
    recipient_data = db_handle.select_data(recipient_phone)
    if recipient_data:
        if recipient_name == recipient_data['name']:
            return True, f'请确认收款人姓名为{recipient_name}'
        return False, "收款人信息有误，请重新输入"
    return False, "用户不存在，请重新输入"


def transfer_account_info(recipient_phone, phone_number, password, money):
    """处理转账逻辑"""
    # 查看收款人余额
    recipient_data = db_handle.select_data(recipient_phone)
    recipient_balance = recipient_data['balance']
    # 查看现有余额
    user_data = db_handle.select_data(phone_number)
    user_balance = user_data['balance']
    # 判断余额是否足够
    if money <= user_balance:
        # 判断密码是否正确
        if password == user_data['password']:
            # 转账操作
            recipient_data['balance'] = recipient_balance + money
            user_data['balance'] = user_balance - money
            # 添加流水
            now_time = time.strftime("%Y-%m-%d %H:%M:%S")
            recipient_bill_info = f"{now_time} 转入金额:{money}元，账户余额:{recipient_data['balance']}元，汇款人{user_data['name']}"
            user_bill_info = f"{now_time} 转出金额:{money}元，账户余额:{user_data['balance']}元，收款人{recipient_data['name']}"
            recipient_data['bill'].append(recipient_bill_info)
            user_data['bill'].append(user_bill_info)
            # 保存更改数据
            db_handle.save_data(recipient_data)
            db_handle.save_data(user_data)
            return 0, user_bill_info
        else:
            return 1, "密码错误，请重新输入"
    return 2, "您的账户余额不足，请重新输入"


def check_bill_info(phone_number):
    """处理查看明细逻辑"""
    # 根据手机号返回账单
    user_data = db_handle.select_data(phone_number)
    return user_data['bill']
