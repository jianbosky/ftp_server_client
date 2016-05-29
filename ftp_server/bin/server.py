#!/usr/bin/env python3.5
# -*-coding:utf8-*-
import os,sys
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASEDIR)
from core import main

'''
FTPserver用户名 jjb  密码 123456
                alex 密码 123456


'''
if __name__ == "__main__":
    main.run()
