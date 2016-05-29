#!/usr/bin/env python3.5
# -*-coding:utf8-*-
import os,sys
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASEDIR)

DATABASE = {
	'local': 'd:\\',   # 本地客户端目录
}

IP_PORT = {"host": "127.0.0.1",  # FTP服务器地址
          "port": 21,
}