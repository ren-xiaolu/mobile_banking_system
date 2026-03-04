import re
import sys
from api import user, bank
from lib import common

login_status = None  # 登录状态标识


def register():
    """注册"""
    print("-----------------请注册-----------------")
    while True:
        phone_number = input("请输入手机号：")
        # 手机号格式判断
        if re.match(r'^1[3-9]\d{9}', phone_number):
            name = input("请输入用户名：")
            password = input("请输入密码：")
            password1 = input("请再次输入密码：")
            if password == password1:
                flag, msg = user.register_info(phone_number, name, password)  # 用户数据处理
                print(msg)
                if flag:
                    break
                else:
                    login()
                    break
            else:
                print("输入密码不一致，请重新输入")
        else:
            print("手机号码格式有误，请输入正确的手机号")


def login():
    """登录"""
    print("-----------------请登录-----------------")
    count = 0
    while count < 3:
        phone_number = input("请输入手机号：")
        password = input("请输入密码：")
        flag, msg = user.login_info(phone_number, password)
        print(msg)
        if flag == 1:
            global login_status
            login_status = phone_number
            break
        elif flag == 2:
            count += 1
        else:
            register()
            break
    if count == 3:
        print("密码输入错误次数超限，请稍后再试")
        sys.exit()


@common.is_login
def save_money():
    """存钱"""
    while True:
        money = input("请输入存款金额：")
        if money.isdigit() and int(money) > 0:
            flag, msg = bank.save_money_info(login_status, int(money))
            print(msg)
            if flag:
                break
        else:
            print("请输入合法金额")


@common.is_login
def get_money():
    """取钱"""
    # 输入取款金额
    while True:
        money = input("请输入取款金额：")
        if money.isdigit() and int(money) > 0:
            flag, msg = bank.get_money_info(login_status, int(money))  # 进行取款的逻辑处理
            print(msg)  # 返回取款结果
            if flag:
                break
        else:
            print("请输入合法金额")


@common.is_login
def transfer_account():
    """转账"""
    flag = 0
    while True:
        # 输入收款人手机号
        recipient_phone = input("请输入收款人手机号：")
        # 手机号格式判断
        if re.match(r'^1[3-9]\d{9}', recipient_phone):
            # 输入收款人用户名
            recipient_name = input("请输入收款人用户名：")
            # 判断收款人信息是否正确
            flag0, msg0 = bank.recipient_info(recipient_phone, recipient_name)
            print(msg0)
            count = 0
            if flag0:
                while count < 3:
                    # 输入汇款金额
                    money = input("请输入汇款金额：")
                    # 金额合法性判断
                    if money.isdigit() and int(money) > 0:
                        # 输入密码
                        password = input("请输入密码：")
                        flag1, msg1 = bank.transfer_account_info(recipient_phone, login_status, password, int(money))
                        print(msg1)
                        if flag1 == 0:
                            flag = 1
                            break
                        elif flag1 == 1:
                            count += 1
                    else:
                        print("请输入合法金额")
                if count == 3:
                    print("密码输入错误次数超限，请稍后再试")
                    break
            if flag:
                break
        else:
            print("手机号码格式有误，请输入正确的手机号")


@common.is_login
def check_money():
    """查看余额"""
    name, balance = user.check_money_info(login_status)
    print(f'{name}账户余额为{balance}元')


@common.is_login
def check_bill():
    """查看明细"""
    bill_list = bank.check_bill_info(login_status)
    # 判断账单是否为空
    if bill_list:
        for bill_info in bill_list:
            print(bill_info)
    else:
        print("用户{login_status}暂无明细")


def change_password():
    """修改密码"""
    while True:
        # 输入原密码、新密码
        old_password = input("请输入原密码：")
        new_password = input("请输入新密码：")
        # 判断两次密码是否一致
        if old_password != new_password:
            flag = user.change_password_info(login_status, old_password, new_password)
            if flag:
                print("密码更改成功")
                break
        else:
            print("新密码不能和旧密码一致，请重新输入")


def login_out():
    """退出登录"""
    # 更改登录状态标识
    global login_status
    login_status = None


def delete_user():
    """注销用户"""
    global login_status
    flag = user.delete_user_info(login_status)
    if flag:
        login_status = None
        print("注销用户成功")


# 功能菜单
menu = {
    0: ("注册", register),
    1: ("登录", login),
    2: ("退出系统", sys.exit),
    3: ("存钱", save_money),
    4: ("取钱", get_money),
    5: ("转账", transfer_account),
    6: ("查看余额", check_money),
    7: ("查看明细", check_bill),
    8: ("修改密码", change_password),
    9: ("退出登录", login_out),
    10: ("注销用户", delete_user)
}


def main():
    print("\t\t\t欢迎来到手机银行系统")
    while True:
        if login_status:
            for select in list(menu)[2:11]:
                print(select, menu[select][0])
            select = int(input("请选择你要做操作："))
            if select in menu.keys():  # 输入合法性
                menu[select][1]()
            else:
                print("输入错误")
        else:
            for select in list(menu)[:3]:
                print(select, menu[select][0])
            select = int(input("请选择你要做操作："))
            if select in list(menu)[:3]:
                menu[select][1]()
            else:
                print("输入错误")
