from django.conf.urls import url
from . import views
app_name = 'comments'
urlpatterns = [
    url(r'^(?P<article_id>[0-9]+)/comment/$', views.article_comment, name='article_comment'),
]
