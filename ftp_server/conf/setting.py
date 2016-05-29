#!/usr/bin/env python3.5
# -*-coding:utf8-*-
import os,sys
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASEDIR)

DATABASE = {
	'engine': 'file_storage',   # support mysql,PostgreSQL in the future
	'dbpath': "{}\db".format(BASEDIR),
}

IP_PORT = {"host": "127.0.0.1",
          "port": 21,
}