#!/usr/bin/env python3.5
# -*-coding:utf8-*-
import os,sys
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASEDIR)
from core import client
if __name__ == "__main__":
    client.run()
