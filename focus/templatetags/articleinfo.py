#encoding:utf-8
from django import template
from ..models import Article,Category
register = template.Library()

@register.filter
def get_key(d, key_name):
    return d.get(key_name)

@register.filter
def get_attr(d, m):
    if hasattr(d, m):
        return getattr(d, m)

@register.simple_tag
def get_recent_articles(num=5):
    return Article.objects.all().order_by('-create_time')[:num]

#文章归档
@register.simple_tag
def archives():
    return Article.objects.dates('create_time', 'month', order='DESC')

#文章分类
@register.simple_tag
def get_categories():
    return Category.objects.all()
