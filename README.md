# ftp_server_client
多线程多用户FTP服务器端与客户端程序
功能介绍：
        本套程序可以同时实现多用户进行登陆操作，实现文件上传下载、删除、目录创建及目录进入与退出等功能，同时对用户密码实现SHA512进行加密
        认证，实现文件下载及上传进度条可见。
文件介绍：
        FTP服务器端：
                    bin 文件夹下 server.py 为服务器端启动程序
                    conf 文件夹下 setting.py为系统配置文件
                    core 文件夹 为主程序核心模块
                    db 文件夹为用户数据存放
                    文件介绍：
                            main.py 为服务器端主程序调用多线程及身份验证功能
                            db_handler.py 为服务器端数据处理模块
                            file_handler.py 为服务器端FTP实例操作处理模块
                            conf文件夹下 admin.py 为临时用户数据增加模块
        FTP 客户端：
                  bin 文件夹下 ftp_client.py 为客户器端启动程序
                  conf 文件夹下 setting.py为系统配置文件
                  core 文件夹 为主程序核心模块
                  db 文件夹为用户数据存放
                  文件介绍：
                          client.py 为客户端主程序用于建立与服务器端的认证连接
                          file_handler.py 为客户端文件上传与下载功能实例模块
开源地址为：https://github.com/jianbosky/ftp_server_client
博客地址为：
                          
