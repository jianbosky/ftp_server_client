#!/usr/bin/env python3.5
# -*-coding:utf8-*-
import os,sys
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASEDIR)
import re
from core import db_handler
from conf import setting
import pickle
class FTPs(object):
    '''
    ftp操作命令方法：
    '''
    def __init__(self,username,conn,home,total_size):
        '''
        初始化参数
        :param username: 操作用户名
        :param conn: sock连接
        :param home: 用户根目录
        :param total_size: 磁盘配额
        :return:
        '''
        self.username = username
        self.conn = conn
        self.root = home
        self.home = self.root
        self.total_size = int(total_size)
        self.cmd_file = None  # 文件指令
        self.psize = 4096 # 文件分片
    def getdirsize(self,space):
        '''
        计算磁盘空间大小
        :return:
        '''
        self.dirsize = 0
        for root,dirs,files in os.walk(space):
            self.dirsize += (sum([os.path.getsize(os.path.join(root,name))for name in files])/1024)
        return int(self.dirsize)
    def put(self):
        '''
        上传文件
        :return:
        '''
        if self.cmd_file:
            self.user_space = int(self.getdirsize(self.root)/1024)
            # 组合接收字符串
            self.file_root = '%s\\%s'% (self.home,self.cmd_file)
            # # 获取文件名
            self.f =os.path.basename(self.file_root)
            if os.path.isdir(self.home):
                os.chdir(self.home)
            else:
                os.makedirs(self.home)
                os.chdir(self.home)
            try:
                self.conn.send(bytes("f_ack","utf8"))
                self.size = str(self.conn.recv(1024).decode()).split("|")
                if self.size[0]== "fsize":
                    self.fss = int(self.size[1])
                    self.f_total_size = int(self.user_space + (self.fss/1024/1024))
                    if self.f_total_size < self.total_size:  # 判断空间是否超额
                        self.conn.send(bytes("f_ack_ready","utf8"))
                        self.bsize = 0
                        print("需要上传文件大小：",self.fss)
                        # 打开文件
                        f=open(self.f,'wb')
                        while self.bsize < self.fss:
                            data = self.conn.recv(self.psize)
                            self.bsize += len(data)
                            f.write(data)
                        self.conn.send(bytes("ok","utf8"))
                        print("实际已上传文件大小：",self.bsize)
                    else:
                        self.conn.send(bytes("上传空间不足！无法上传,你当前磁盘配额为%sM"%self.total_size,"utf8"))

            except Exception as ex:
                self.conn.send(bytes(ex,"utf8"))
        else:
            self.conn.send(bytes("请上传文件，文件不能为空","utf8"))
    def get(self):
        '''
        下载文件
        :return:
        '''
        if self.cmd_file:
            os.chdir(self.home) # 进入用户根目录
            self.file = os.getcwd()+"\\"+ self.cmd_file
            if os.path.isfile(self.file):
                f = open(self.file, 'rb')
                self.fsize = os.path.getsize(self.file) # 获取要发送文件的大小
                self.conn.send(bytes("f_ack_read","utf8"))
                self.conn.recv(1000)
                print("需发送文件大小：",self.fsize)
                self.conn.send(bytes("fsize|%s"%self.fsize,"utf8")) # 发送文件大小及要发送准备完毕指令
                if self.conn.recv(1000).decode() == "f_ack":  # 接收对方是否准备就绪
                    self.fsize = int(self.fsize)
                    self.size = 0
                    ack =""
                    while self.size < self.fsize and ack !="ok":
                        data = f.read(self.fsize)  # 一次读取分片大小4096
                        self.conn.send(data)
                        self.size += len(data)
                    print("实际发送文件大小：",self.size)
                    ack = self.conn.recv(1000).decode() # 接收客户端是否下载完指令
                    self.conn.send(bytes("成功","utf8"))
                else:
                    self.conn.send(bytes("接收失败","utf8"))
            else:
                self.conn.send(bytes("文件不存在","utf8"))
        else:
            self.conn.send(bytes("请输入文件名","utf8"))
    def dir(self):
        '''
        查看文件
        :return:
        '''
        self.current_space =int(self.getdirsize(self.home))
        # 文件列表
        self.li = ""
        # 目录列表
        self.dl = ""
        try:
            os.chdir(self.home)
        except:
            os.makedirs(self.home)
            os.chdir(self.home)
        try:
            if os.listdir(os.getcwd()):
                for self.i in os.listdir(os.getcwd()):
                    self.file = os.getcwd()+'\\'+self.i
                    if os.path.isfile(self.file):
                        # 获取文件大小
                        self.fsize = int(os.path.getsize(self.file)/1024)
                        if self.fsize < 1:
                            self.fsize = 4
                        else:
                            self.fsize +=4
                        self.li += '%s -rw-rw-rw- 占用大小：%skb\r\n'% (self.i,self.fsize)
                    else:
                        self.dl += '%s\r\n'%self.i
                self.conn.send(bytes("目录：\r\n\r\n%s 文件：\r\n%s\r\n \r\n当前目录空间大小：%skb"%(self.dl,self.li,self.current_space),"utf8"))
            else:
                self.conn.send(bytes("当前目录为:%s"%(self.home),"utf8"))
        except Exception as ex:
            self.conn.send(bytes(ex,"utf8"))
    def cd(self):
        '''
        进入目录
        :return:
        '''

        if self.cmd_file:
            os.chdir(self.home)  # 先进入到工作目录
            self.dir_change = os.path.abspath(os.path.join(self.home,"%s\%s"%(self.home,self.cmd_file)))
            if self.root in self.dir_change:
                try:
                    os.chdir(self.dir_change)
                    self.home = self.dir_change
                    self.conn.send(bytes("当前工作目录为：%s"%self.home,"utf8"))
                except:
                    os.makedirs(self.dir_change)
                    os.chdir(self.dir_change)
                    self.home = self.dir_change
                    self.conn.send(bytes("当前工作目录为：%s"%self.home,"utf8"))
            else:
                    self.conn.send(bytes("当前工作目录为：%s    更改失败！"%self.home,"utf8"))
        else:
            os.chdir(self.home)
            self.conn.send(bytes("当前工作目录为：%s"%self.home,"utf8"))
    def mkd(self):
        '''
        创建目录
        :return:
        '''
        if self.cmd_file:
            try:
                os.makedirs(self.cmd_file)
                self.conn.send(bytes("创建目录成功!","utf8"))
            except Exception as ex:
                self.conn.send(bytes("创建目录失败！原因:%s"%ex,"utf8"))
        else:
            self.conn.send(bytes("请输入文件夹名！","utf8"))
    def delete(self):
        '''
        删除文件
        :return:
        '''
        os.chdir(self.home) # 进入用户根目录
        try:
            self.file = self.home+'\\'+ self.cmd_file
            if os.path.isfile(self.file):
                os.remove(self.cmd_file)
                self.conn.send(bytes("文件:%s删除成功！"%self.cmd_file,"utf8"))
            else:
                os.removedirs(self.cmd_file)
                self.conn.send(bytes("目录删除成功！","utf8"))
                os.chdir(self.root)
        except Exception:
            if os.path.isdir(self.root):
                self.conn.send(bytes("删除失败！","utf8"))
            else:
                os.makedirs(self.root)
                self.conn.send(bytes("删除失败！","utf8"))

    def help(self):
        '''
        FTP帮助信息
        :return:
        '''
        self.conn.send(bytes("""
        FTP服务器操作方法有： put------>上传文件至服务器
                             get------>从服务器上下载文件
                             dir------>查看服务器文件列表
                             cd------->进入指定文件夹
                             delete--->删除文件
                             mkd ----->创建目录
                             help----->帮助信息
                             q ------->退出

        ""","utf8"))
    def run(self):

        while True:
            # try:
             # # 接收客户端发来的命令信息
            self.cmd = self.conn.recv(1000)
            self.cmd_action = str(self.cmd.decode())
            # 判断命令是否含有空格
            self.fg = re.search("\s","%s"%self.cmd_action)
            if self.fg:
                self.cmd_action,self.cmd_file = str(self.cmd_action).split(" ")
            else:
                self.cmd_file =None
            # print("cmd_action:",self.cmd_action,"cmd_file:",self.cmd_file)
            if hasattr(FTPs,self.cmd_action):
                func = getattr(self,self.cmd_action)
                func()
                continue
            else:
                self.conn.send(b'command is not found!')
                continue
            # except Exception as ex:
            #     print("系统异常:%s"%ex)