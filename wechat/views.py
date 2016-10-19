# coding: utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from wechat_sdk import WechatConf
from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import (TextMessage, VoiceMessage, ImageMessage, VideoMessage, LinkMessage, LocationMessage, EventMessage, ShortVideoMessage)
from wechat.models import MsgDB

from django.shortcuts import render
from django.utils import timezone
import datetime
import os
import random

conf = WechatConf(
    token='your_token', 
    appid='your_appid', 
    appsecret='your_appsecret', 
    encrypt_mode='safe',  # 可选项：normal/compatible/safe，分别对应于 明文/兼容/安全 模式
    encoding_aes_key='your_encoding_aes_key'  # 如果传入此值则必须保证同时传入 token, appid
)

help = ['help','h',u'帮助']
topic = ['topic','t','tree','hole','treehole','tree hole',u'树洞',u'秘密','secret','24']
about = ['about',u'关于','g2ex',u'我']
gif_msg = u'【收到不支持的消息类型，暂无法显示】'
content_min_length = 10

# 微信接口
@csrf_exempt
def WeChat(request):
    signature = request.GET.get('signature')
    timestamp = request.GET.get('timestamp')
    nonce = request.GET.get('nonce')
    wechat_instance = WechatBasic(conf=conf)
    if not wechat_instance.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
        return HttpResponseBadRequest('Verify Failed')
    else:
        if request.method == 'GET':
           response = request.GET.get('echostr', 'error')
        else:
            try:
                wechat_instance.parse_data(request.body)
                message = wechat_instance.get_message()
                if isinstance(message, TextMessage):
                    print(message.source, message.time, message.content)
                    # 显示最近 24 小时内的秘密
                    if message.content.lower() in topic:
                        reply_text = show_topic(10)
                        response = wechat_instance.response_text(reply_text, escape=True)
                    # 显示关于信息
                    elif message.content.lower() in about:
                        reply_text = show_about()
                        response = wechat_instance.response_news(reply_text)
                    # 显示帮助信息
                    elif message.content.lower() in help or len(message.content) <= content_min_length:
                        reply_text = show_help()
                        response = wechat_instance.response_news(reply_text)
                    # 过滤自定义表情
                    elif cmp(message.content, gif_msg)== 0:
                        response = wechat_instance.response_text(u'ʕ •ᴥ•ʔ 自定义表情是不会被记录的哎，写点文字吧~')
                    # 记录用户的消息
                    else:
                        save_message(message.source, message.content, timezone.now())
                        response = wechat_instance.response_text(u'嘘~~~ 树洞知道了~\n输入「树洞」可以看到大家最新的小秘密 ヾ(o◕∀◕)ﾉヾ', escape=True)
                elif isinstance(message, VoiceMessage):
                    response = wechat_instance.response_text(u'("▔□▔)/ 暂时还听不懂你在说什么唉，写点文字吧~')
                elif isinstance(message, ImageMessage):
                    response = wechat_instance.response_text(u'("▔□▔)/ 暂时还不能识别图片唉，写点文字吧~')
                elif isinstance(message, LinkMessage):
                    response = wechat_instance.response_text(u'("▔□▔)/ 链接我是不会记录的唉，写点文字吧~')
                elif isinstance(message, LocationMessage):
                    response = wechat_instance.response_text(u'("▔□▔)/ 位置信息我是不会记录的唉，写点文字吧~')
                elif isinstance(message, VideoMessage):
                    response = wechat_instance.response_text(u'("▔□▔)/ 视频我是不会记录的唉，写点文字吧~')
                elif isinstance(message, ShortVideoMessage):
                    response = wechat_instance.response_text(u'("▔□▔)/ 小视频我是不会记录的唉，写点文字吧~')
                else:
                    response = wechat_instance.response_text(u'恭喜你成为了 G2EX 前 60 亿个粉丝！随便写点什么试试吧~')
            except ParseError:
                return HttpResponseBadRequest('Invalid XML Data')
        return HttpResponse(response, content_type="application/xml")

# 把微信用户发来的消息保存到数据库中
def save_message(openid, content, time):
    msg = MsgDB.objects.filter(openid=openid)
    if msg.exists():
        # 该用户已经发过消息
        msg.update(content=content, time=time);
    else:
        # 该用户尚未发过消息
        msg = MsgDB(openid=openid, content=content, time=time)
        msg.save()

# 从数据库中读取 24 小时内的微信用户消息
def show_topic(numb):
    lastest_msg_list = MsgDB.objects.filter(
                                time__lte=timezone.now()
                            ).filter(
                                time__gte=timezone.now()-datetime.timedelta(days=1)
                            ).order_by('-time')[:numb]
    if lastest_msg_list.exists():
        name_list = get_names_from_file()
        topics = u'↓_↓ 来自树洞的秘密 ↓_↓'
        for msg in lastest_msg_list:
            topics += '\n';
            topics += name_list[random.randint(0, len(name_list)-1)]
            topics += '：'
            topics += msg.content;
    else:
        topics = u'看来最近没有人对树洞说出秘密，你不妨说一个吧~'
    return topics

# 从文件中读取武侠名字并随机分配给每条消息
def get_names_from_file():
    FILEDIR = os.path.dirname(__file__)
    try:
        with open(FILEDIR + '/resources/names','r') as f:
            names = f.read()
            name_list = names.split(' ')
    except IOError:
        name_list = ['匿名']
    finally:
        return name_list

# 显示关于信息
def show_about():
    about_desc = u'这是 G2EX 的公众号，点击「查看全文」你可以看到更多我的信息。\n\n公众号里实现了一个树洞的小应用，你可以把你心中的秘密以消息的形式发送给我，无需担心秘密泄露，树洞最多给你保留 24 小时，之后再也没有人知道咯~﻿\n同时你也可以看到别人最新的秘密，别担心，这些都是匿名的。\n\n输入「帮助」查看更多使用秘籍。'
    about_me = [{
            'title': u'关于',
            'description': about_desc,
            'url': u'https://g2ex.github.io/about',
        }]
    return about_me

# 显示帮助信息
def show_help():
    help_desc = u'''被你发现了！
你也许听说过树洞的故事。
在这里你能放心地说出心底的秘密，树洞帮你保留 24 小时，同时你也可以看到别人最新的秘密。忘了提醒你，至少 ''' + str(content_min_length) + u''' 个字才能算是秘密~

输入「树洞」或者「秘密」可以看到树洞中所有人最新的秘密
输入「关于」可以查看公众号信息
输入「帮助」可以查看帮助信息'''

    help = [{
            'title': u'树洞使用秘籍',
            'description': help_desc,
            'url': u'https://www.zybuluo.com/g2ex/note/511028',
        }]
    return help


''' 暂时不使用单独的页面显示树洞秘密
@csrf_exempt
def TreeHole(request):
    lastest_msg_list = MsgDB.objects.filter(
                                time__lte=timezone.now()
                            ).filter(
                                time__gte=timezone.now()-datetime.timedelta(days=1)
                            )
    context = {'lastest_msg_list': lastest_msg_list}
    return render(request, 'wechat/index.html', context)
'''