#coding=utf8
import itchat
from itchat.content import *
import requests
import time;  # 引入time模块

KEY = '4019b0eb4728489e9f537872ab18f00c'
userDict = {}
userList = []
userFirstChatDateList = []

@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    msg['Text'](msg['FileName'])
    return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])

@itchat.msg_register(TEXT,isFriendChat=False, isGroupChat=True)
def text_reply(msg):
    # 发送给文件助手，防止对方撤回
    itchat.send('%s: %s' % (msg['ActualNickName'], msg['Text']), 'filehelper')
    
@itchat.msg_register(TEXT,isFriendChat=True,isGroupChat=False)
def text_reply(msg):
    # 发送给文件助手，防止对方撤回
    # itchat.send('%s: %s' % (msg['ActualNickName'], msg['Text']), 'filehelper')
    # 将时间戳转化为localtime
    x = time.localtime(msg['CreateTime'])
    createTime = time.strftime('%Y-%m-%d %H:%M:%S',x)
    itchat.send('FromUserName:%s\nToUserName:%s\n\nCreateTime: %s\nText:%s' % (msg['FromUserName'],msg['ToUserName'],createTime, msg['Text']), 'filehelper')

itchat.auto_login(hotReload=True)
itchat.run()