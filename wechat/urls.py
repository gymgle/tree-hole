from django.conf.urls import url, include
from wechat import views

urlpatterns = [
    url(r'^$', views.WeChat),
    #url(r'^treehole/$', views.TreeHole),
]
