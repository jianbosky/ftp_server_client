# -*- coding:utf-8 -*-
import pickle
# 增加用户
testDict ={"name":"test","password":"123456","file_dir":"E:\\python\\2","file_size":500}
file = 'alex' # 以用户名命名文件
fp = open(file,'wb')
pickle.dump(testDict,fp)
fp.close()

# f = open("jjb.pkl","rb")
# data = pickle.loads(f.read())
# f.close()
# print(data)
# """