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
                    self.fsize = int(self.fsize)
                    self.size = 0
                    ack =""
                    if self.ack.decode() =="f_ack_ready":
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
                    elif self.ack.decode() == "f_ok":
                        print("上传的文件已经存在，无需上传！")
                    elif self.ack.decode() == "f_continue":
                        # 开启断点续传
                        self.sk.send(bytes("continue_ok","utf8"))
                        print("正在断点续传中，请稍候！")
                        self.str_size =int(self.sk.recv(1024).decode())
                        # 定位到上次文件中断的位置
                        f.seek(self.str_size)
                        while self.str_size < self.fsize:
                            data = f.read(4094)
                            self.sk.send(data)
                            self.str_size+= len(data)
                            count = int(self.str_size/self.fsize*100)
                            print('#'*count,"->",(count),"%","当前已上传%s字节，总大小是:%s字节"%(self.str_size,self.fsize))
                        ack = self.sk.recv(1000).decode()
                        if ack =="ok":
                            print("上传成功")
                        else:
                            print("上传失败")
                        
                    else:
                        # 打印错误信息
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
            self.sk.send(bytes(self.cmd_action,"utf8"))  # 发送get命令及文件名
            rec_msg = self.sk.recv(8000)
            if rec_msg.decode() == "f_ack_read":
                self.sk.send(bytes("f_read_ok","utf8"))
                self.rec_size = self.sk.recv(2048)
                self.ack_rec= str(self.rec_size.decode()).split("|")
                self.ack_s =int(self.ack_rec[1])
                print(self.ack_s)
                # 判断当前要下载的文件本地是否存在
                if os.path.isfile(self.cmd_file):
                    # 获取当前目录已存在的文件大小
                    self.bsize = os.path.getsize(self.cmd_file)
                    if self.bsize == self.ack_s:
                        self.sk.send(bytes("本地已存在此文件：%s,无需下载！"%self.cmd_file,"utf8"))
                        print("本地已存在此文件：%s,无需下载！"%self.cmd_file)

                    else:
                        # 文件下载断点续传
                        self.sk.send(bytes("f_ack_continue","utf8"))
                        self.fack = self.sk.recv(1024).decode()
                        if self.fack == "file_continue":
                            # 发送上次下载的文件大小
                            print("文件正在以断点续传功能下载，请稍侯！")
                            self.sk.send(bytes("%s"%self.bsize,"utf8"))
                            f = open(self.cmd_file,"ab")
                            while self.bsize < self.ack_s:
                                xx =self.bsize/self.ack_s*100
                                data = self.sk.recv(4096)
                                self.bsize += len(data)
                                f.write(data)
                                f.flush()
                                count = int(xx)
                                print('#'*count,"->",(count+1),"%","当前已下载%s字节，总大小是:%s字节"%(self.bsize,self.ack_s))
                            self.sk.send(bytes("ok","utf8"))
                            self.ack_ok = self.sk.recv(1024)
                            print("接收文件：%s"%self.ack_ok.decode())
                else:
                    # 文件正常下载
                    self.sk.send(bytes("f_ack","utf8"))
                    self.re_s = 0
                    f = open(self.cmd_file,"wb")
                    while self.re_s < self.ack_s:
                        xx = self.re_s/self.ack_s*100
                        data = self.sk.recv(4096)
                        self.re_s += len(data)
                        # print(data.decode("gbk"))
                        f.write(data)
                        f.flush()
                        count = int(xx)
                        print('#'*count,"->",(count+1),"%")
                    self.sk.send(bytes("ok","utf8"))
                    print(self.re_s)
                    self.ack_ok = self.sk.recv(1024)
                    print("接收文件：%s"%self.ack_ok.decode())
            else:
                print("接收文件失败：%s"%rec_msg.decode())
        else:
            print("请输入要下载的文件名！")

