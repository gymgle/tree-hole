## 微信公众平台「树洞」项目

> 童话故事「皇帝长了驴耳朵」里，理发匠知道皇帝长了一对驴耳朵，因秘密憋得太辛苦，终于对着山上一棵大树的洞里说出了这个秘密，因为这个童话故事，「树洞」一词逐渐有了「隐藏秘密」的隐喻。

关注公众号的用户给公众号发送消息，服务器会把多于 10 个字的消息当做用户的秘密保存。用户在公众号中输入 `树洞` 或 `秘密` 等关键字可以查看「树洞」中所有人 24 小时内的秘密。

## 把你的公众号变成「树洞」

「树洞」服务器后台基于 `Django` 框架开发，使用了 `wechat-python-sdk` 开发包。

开发和测试环境：

```
Ubuntu 14.04 LTS
wechat-python-sdk 0.6.4
Django 1.10.1
Python 2.7.6
```

在公众号中开启开发者模式，填写你的服务器信息。在的服务器上安装 `Django` 和 `wechat-python-sdk`。

进入项目目录，运行 `python manager.py runserver 0.0.0.0:80` 测试。

建议部署时搭配 Nginx 或 Apache。


微信公众平台开发过程请参考：
* 微信公众平台开发（一） https://g2ex.github.io/2016/09/25/WeChat-Media-Platform-Development-Intro/
* 微信公众平台开发（二） https://g2ex.github.io/2016/09/28/WeChat-Media-Platform-Development-with-SDK/

## 体验「树洞」

你可以在我的微信公众号「G2EX」里体验「树洞」，扫码即可。

![g2ex](https://g2ex.github.io/images/qrcode_for_g2ex.jpg)
