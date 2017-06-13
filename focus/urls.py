#encoding:utf-8
from django.conf.urls import include,url
from . import views

app_name = "focus"
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.log_in, name='login'),
    url(r'^logout/$', views.log_out, name='logout'),
    url(r'^register/$', views.register, name='register'),
    # url(r'^(?P<article_id>[0-9]+)/comment/$', views.comment, name='comment'),   #comments 独立模块下完成
    url(r'^(?P<article_id>[0-9]+)/poll/$', views.get_poll, name='poll'),
    url(r'^(?P<article_id>[0-9]+)/keep/$', views.get_keep, name='keep'),
    url(r'^(?P<article_id>[0-9]+)/$', views.article, name='detail'),
]

urlpatterns += [
    # url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.ArchivesView.as_view(), name='archives'),    #文章归档
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.archives, name='archives'),  #和上一行归档同样的效果
    # url(r'^category/(?P<category_id>[0-9]+)/$', views.CategoryView.as_view(), name='category'),  #文章分类
    url(r'^category/(?P<category_id>[0-9]+)/$', views.category, name='category'),
]
