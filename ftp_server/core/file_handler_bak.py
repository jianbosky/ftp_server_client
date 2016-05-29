#!/usr/bin/env python3.5
# -*-coding:utf8-*-
import os,sys
import subprocess
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASEDIR)
from core import db_handler
from conf import setting
class file_action(object):
    '''
    ftp操作命令方法：
    '''
    def __init__(self,username,cmd_action,cmd_file,total_size=300):
        self.username = username
        self.total_size = total_size
        self.cmd_action = cmd_action
        self.cmd_file = cmd_file
        self.root = db_handler.handler(setting.DATABASE,self.username,"2")
        self.home = self.root
    def put(self):
        if self.cmd_file:
            self.home = '%s\\%s'% (self.home,self.cmd_file)
            # 获取目录名
            d =os.path.dirname(self.home)
            # 获取文件名
            f =os.path.basename(self.home)
            try:
                os.chdir(self.home)
                return "d:%s,f:%s"%(d,f)
            except:
                os.makedirs(self.home)
                os.chdir(self.home)
                return "d:%s,f:%s"%(d,f)
        else:
            return "请上传文件，文件不能为空"

    def get(self):
        if self.cmd_file:
            try:
                os.chdir(self.home)
            except:
                os.makedirs(self.home)
                os.chdir(self.home)

        else:
            return "不存在"
        return self.cmd_file
    def dir(self):
        li = ""
        try:
            os.chdir(self.root)
        except:
            os.makedirs(self.root)
            os.chdir(self.root)
        if os.listdir(os.getcwd()):
            for i in os.listdir(os.getcwd()):

                file = os.getcwd()+'\\'+i
                if os.path.isfile(file):
                    # 获取文件大小
                    fsize = os.path.getsize(file)
                    li += '文件： %s 大小：%s\r\n'% (i,fsize)
                else:
                    li += '目录：%s\r\n'%i
        else:
            li ="."
        return li
    def cd(self):
        try:
            os.chdir(self.root)
        except:
            os.makedirs(self.root)
            os.chdir(self.root)
    def delete(self):
        try:
            os.chdir(self.root)
        except:
            os.makedirs(self.root)
            os.chdir(self.root)
        if self.cmd_file == None:
            self.cmd_file = "你没有输入文件名"
            return self.cmd_file
        else:
            return self.cmd_file
    def help(self):
        return ("""
        FTP服务器操作方法有：put--->上传文件至服务器
                             get--->从服务器上下载文件
                             dir--->查看服务器文件列表
                             cd---->进入指定文件夹
                             delete->删除文件

        """)