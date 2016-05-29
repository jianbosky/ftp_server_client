#!/usr/bin/env python3.5
# -*-coding:utf8-*-


def db_handler(conn_params,file_name):
    '''
    处理数据库路径
    :param conn_params:
    :param file_name:
    :return:
    '''
    db_path="{}\{}".format(conn_params["dbpath"],file_name)
    return db_path

def handler(conn_params,file_name):
    '''
    处理数据库引擎
    :param conn_params:
    :param file_name:
    :return:
    '''
    if conn_params["engine"]=="file_storage":
        return db_handler(conn_params,file_name)
