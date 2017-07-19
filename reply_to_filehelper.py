#coding=utf8
import requests
import itchat

# 带对象参数注册，对应消息对象将调用该方法
@itchat.msg_register(itchat.content.TEXT, isFriendChat=True, isGroupChat=True, isMpChat=True)
def text_reply(msg):
	# 注意实验楼环境的中文输入切换
    itchat.send('%s: %s' % (msg['FromUserName'], msg['Text']), 'filehelper')   

# 为了让实验过程更加方便（修改程序不用多次扫码），我们使用热启动
itchat.auto_login(hotReload=True)
itchat.run()