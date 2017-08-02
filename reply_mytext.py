#coding=utf8
import requests
import itchat

# 带对象参数注册，对应消息对象将调用该方法
@itchat.msg_register(itchat.content.TEXT, isFriendChat=True, isGroupChat=True, isMpChat=True)
def text_reply(msg):
    itchat.send(u'我是机器人小小，谢谢！',msg['FromUserName'])

# 为了让实验过程更加方便（修改程序不用多次扫码），我们使用热启动
itchat.auto_login(hotReload=True)
itchat.run()