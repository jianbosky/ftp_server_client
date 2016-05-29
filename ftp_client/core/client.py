#!/usr/bin/env python3.5
# -*-coding:utf8-*-
import sys,os,re
import socket,hashlib
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASEDIR)
from core import file_handler
from conf import setting
def login():
    hash = hashlib.sha512()
    while True:
        user_input = input("请输入用户名：").strip()
        pass_input = input("请输入密码：").strip()
        if len(user_input) !=0 and len(pass_input) != 0:
            hash.update(bytes(pass_input,"utf8"))
            sha_pwd = hash.hexdigest()
            user = "%s|%s"% (user_input,sha_pwd)
            return user
            break
def ftp_client():
    sk = socket.socket()
    sk.connect((setting.IP_PORT["host"],setting.IP_PORT["port"]))
    while True:
        flage = False
        sk.send(bytes("connect","utf8"))
        msg = sk.recv(100)
        print("欢迎访问FTP服务器,请根据提示进行操作")
        if msg.decode() == "login":
            while flage == False:
                login_user =login()
                username,password = str(login_user).split("|")
                sk.send(bytes(login_user,"utf8"))
                user_info = sk.recv(1000)
                if user_info.decode() == "login_ack":
                    print("登陆成功！")
                    flage = True
                    break
                print(user_info.decode())
            while flage:
                cmd_action = input("请输入操作命令如：get fy.py or help ：").strip()
                if len(cmd_action) == 0:continue
                if cmd_action == "q":
                    sys.exit()
                # 判断命令是否含有空格
                fg = re.search("\s","%s"%cmd_action)
                if fg:
                    cmd,cmd_file = str(cmd_action).split(" ")
                    ftp = file_handler.ftpc(sk,username,cmd_action,setting.DATABASE["local"])
                    if hasattr(ftp,cmd):
                        func = getattr(ftp,cmd)
                        func()
                        continue
                else:
                    cmd_file =None
                sk.send(bytes(cmd_action,"utf8"))
                rec_msg = sk.recv(8000)
                print(rec_msg.decode())
            if flage == "False":
                sk.send(bytes("connect","utf8"))
    sk.close()
def run():
    ftp_client()
if __name__ == "__main__":
    run()
