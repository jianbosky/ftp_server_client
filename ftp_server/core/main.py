#!/usr/bin/env python3.5
# -*-coding:utf8-*-
import os,sys,socket,pickle
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASEDIR)
from conf import setting
from core import file_handler
from core import db_handler
import select,hashlib
import threading
def login(username,password):
    """
    FTP登陆验证函数
    :param username:
    :param password:
    :return:

    # testDict ={"username":"jjb","password":"123456","file_dir":"E:\python","file_size":500}
    # file = 'jjb.pkl'
    # fp = open(file,'wb')
    # pickle.dump(testDict,fp)
    # fp.close()
    f = open("jjb.pkl","rb")
    data = pickle.loads(f.read())
    f.close()
    print(data)
    """
    #实例化加密函数
    hash = hashlib.sha512()
    db= db_handler.handler(setting.DATABASE,username)
    if os.path.isfile(db):
        f = open(db,"rb")
        data = pickle.loads(f.read())
        f.close()
        if username == data["name"]:
            hash.update(bytes(data["password"],"utf8"))
            hash_pwd = hash.hexdigest()
            if hash_pwd == password:
                filedir = data["file_dir"]
                filesize = data["file_size"]
                return "True|%s|%s"%(filedir,filesize)
            else:
                return "False||"
        else:
            return "False||"
    else:
        return "False||"
def process(conn,addr):
    flage = "False"
    # 接收客户端连接请求信息
    info = conn.recv(1000)
    if info.decode() == "connect":
        conn.send(bytes("login","utf8"))
    # 接收用户及密码信息
    while flage =="False":
        user_check =conn.recv(8000)
        # 分割用户名及密码
        username,password = str(user_check.decode()).split("|")
        # 调用登陆验证函数
        login_ack = login(username,password)
        flage,home,size = str(login_ack).split("|")
        # print(flage,home,size)
        # print("user_input:",username,"user_pass:",password)
        if flage =="True":
            # 登陆成功发送登陆确认信息给客户端
            conn.send(bytes("login_ack","utf8"))
            # 实例化FTPserver
            ftp = file_handler.FTPs(username,conn,home,size) # 登陆用户，数据连接，工作目录,磁盘配额
            ftp.run()
            break
        else:
            # 登陆失败，发送给客户端重新验证
            conn.send(bytes("登陆失败！","utf8"))


def ftp_server():
    '''
    启动FTP服务器端，开启线程监听
    :return:
    '''
    server = socket.socket()
    server.bind((setting.IP_PORT["host"],setting.IP_PORT["port"]))
    server.listen(10)
    while True:
        r,w,e = select.select([server,], [], [], 1)
        for i,server in enumerate(r):
            conn,addr = server.accept()
            # 创建线程
            t = threading.Thread(target=process, args=(conn, addr))
            # 启动线程
            t.start()
    server.close()
def run():
    ftp_server()

if __name__ =="__main__":
    run()

