#!/usr/bin/env python3.5
# -*-coding:utf8-*-
import sys,os,re
import socket
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASEDIR)
class ftpc(object):
    def __init__(self,sk,username,cmd_action,home):
        self.sk = sk
        self.username = username
        self.cmd_action = cmd_action
        self.home = home
    def put(self):
        '''
        上传文件

        :return:
        '''
        try:
            os.chdir(self.home)
        except:
            os.makedirs(self.home)
            os.chdir(self.home)
        # 判断命令是否含有空格
        fg = re.search("\s","%s"%self.cmd_action)
        if fg:
            self.cmd,self.cmd_file = str(self.cmd_action).split(" ")
            if os.path.isfile(os.getcwd()+"\\"+self.cmd_file):
                self.sk.send(bytes(self.cmd_action,"utf8"))  # 发送动作命令
                rec_msg = self.sk.recv(8000)
                if rec_msg.decode() == "f_ack":
                    f = open(self.cmd_file, 'rb')
                    self.fsize = os.path.getsize(self.cmd_file) # 获取要发送文件的大小
                    self.sk.send(bytes("fsize|%s"%self.fsize,"utf8")) # 发送文件大小
                    self.ack = self.sk.recv(1000)
                    if self.ack.decode() =="f_ack_ready":
                        self.fsize = int(self.fsize)
                        self.size = 0
                        ack =""
                        while self.size < self.fsize and ack !="ok":
                            data = f.read(4095)  # 一次读取分片大小4095
                            self.sk.send(data)
                            self.size += len(data)
                            count = int(self.size/self.fsize*100)
                            print('#'*count,"->",(count),"%")
                        ack = self.sk.recv(1000).decode()
                        if ack =="ok":
                            print("上传成功")
                        else:
                            print("上传失败")
                    else:
                        print(self.ack.decode())
                else:
                    print("上传文件失败：%s"%rec_msg.decode())
            else:
                print("上传文件失败,请输入正确的文件名!")
        else:
            print("上传文件失败,请输入正确的文件名!")

    def get(self):
        '''
        下载文件
        :return:
        '''
        try:
            os.chdir(self.home)
        except:
            os.makedirs(self.home)
            os.chdir(self.home)
        # 判断命令是否含有空格
        fg = re.search("\s","%s"%self.cmd_action)
        if fg:
            self.cmd,self.cmd_file = str(self.cmd_action).split(" ")
        else:
            self.cmd_file =None
        self.sk.send(bytes(self.cmd_action,"utf8"))
        rec_msg = self.sk.recv(8000)
        if rec_msg.decode() == "f_ack_read":
            self.rec = self.sk.send(bytes("ok","utf8"))
            self.rec_size = self.sk.recv(2048)
            self.ack_rec= str(self.rec_size.decode()).split("|")
            self.sk.send(bytes("f_ack","utf8"))
            self.ack_s =int(self.ack_rec[1])
            print(self.ack_s)
            self.re_s = 0
            f = open(self.cmd_file,"wb")

            while self.re_s < self.ack_s:
                xx = self.re_s/self.ack_s*100
                data = self.sk.recv(4096)
                self.re_s += len(data)
                # print(data.decode("gbk"))
                f.write(data)
                count = int(xx)
                print('#'*count,"->",(count+1),"%")
            self.sk.send(bytes("ok","utf8"))
            print(self.re_s)
            self.ack_ok = self.sk.recv(1024)
            print("接收文件：%s"%self.ack_ok.decode())
        else:
            print("接收文件失败：%s"%rec_msg.decode())
