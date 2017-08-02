#coding=utf8
import itchat
from itchat.content import *
import requests
import time;  # 引入time模块

KEY = '4019b0eb4728489e9f537872ab18f00c'
userDict = {}
userList = []
userFirstChatDateList = []

def get_response(msg):
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key'    : KEY,
        'info'   : msg,
        'userid' : 'wechat-robot',
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        return r.get('text')
    except:
        return

@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    msg['Text'](msg['FileName'])
    return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])

@itchat.msg_register(TEXT,isFriendChat=False, isGroupChat=True)
def text_reply(msg):
    # 发送给文件助手，防止对方撤回
    itchat.send('%s: %s' % (msg['ActualNickName'], msg['Text']), 'filehelper')
    
    # 获取名字中含有特定字符的群聊，返回值为一个字典的列表
    # list = itchat.search_chatrooms(name=u'测试一下')
    # for index in list:
        # print index

    # 如果有人@我
    # if msg['isAt']:
        # 发送给文件助手，防止对方撤回
        # itchat.send('%s: %s' % (msg['ActualNickName'], msg['Text']), 'filehelper')
        # defaultReply = u'你好！'
        # reply = u'小小：'+get_response(msg['Text'])+'\n \n'+u'PS：我是智能机器人小小，主人在闭关学习了。有急事请拨打电话18826077893，或者发送电子邮件1214914477@qq.com。不@就不会自动回复。'
        # return reply or defaultReply

@itchat.msg_register(TEXT,isFriendChat=True,isGroupChat=False)
def text_reply(msg):
    # 发送给文件助手，防止对方撤回
    # itchat.send('%s: %s' % (msg['ActualNickName'], msg['Text']), 'filehelper')

    # 将时间戳转化为localtime
    x = time.localtime(msg['CreateTime'])
    createTime = time.strftime('%Y-%m-%d %H:%M:%S',x)
    itchat.send('FromUserName:%s\nToUserName:%s\n\nCreateTime: %s\nText:%s' % (msg['FromUserName'],msg['ToUserName'],createTime, msg['Text']), 'filehelper')

    defaultReply = u'你好，智能机器人小小为你服务！'
    defaultReply2 = u'你好，我是智能机器人小小！主人在闭关学习，一般很少查看一下微信的信息。由此带来不便，请谅解！如有急事，请致电或发短信至18826077893。谢谢！\n \n接下来由小小为你服务：小小会讲故事、讲笑话、成语接龙、做数学运算、新闻资讯、星座运势和聊天对话......'
    global userDict
    global userList
    global userFirstChatDateList

    # 获取当前时间
    ticks = time.time()
    # 取出最后一次聊天时的userList和userFirstChatDateList
    # currentUserList = userDict['userList']
    # currentUserFirstChatDateList = userDict['userFirstChatDateList']

    # 先把字典中上一次聊天时间与当前时间距离超过20分钟的去掉
    for index in range(len(userFirstChatDateList)):
        lastChatDate = userFirstChatDateList[index]
        print lastChatDate
        print ticks
        if (ticks - lastChatDate) >= 1200  :
            # 去掉与该时间
            del userFirstChatDateList[index]
            # 去掉与该时间对应的user
            del userList[index]

    # userList该列表维护的是第一次聊天了，但是时间还没超过20分钟的。简单来说，就是直接进行智能应答的列表
    # 如果在用户列表中，是同一个用户，而且不是第一次聊天，时间也还没超过20分钟的，就直接进行智能应答
    if msg['FromUserName'] in userList :   
        reply = get_response(msg['Text'])
        return reply or defaultReply 
    # 如果不在用户列表中
    else :
        # 添加用户
        userList.append(msg['FromUserName'])
        # 添加时间
        print ticks
        userFirstChatDateList.append(ticks)
        # 字典中更新用户和用户聊天时间
        userDict={'userList':userList,'userFirstChatDateList':userFirstChatDateList}
        # 返回默认的回复2
        return defaultReply2

itchat.auto_login(hotReload=True)
itchat.run()