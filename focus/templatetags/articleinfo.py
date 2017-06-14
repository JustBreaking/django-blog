#encoding:utf-8
from django import template
from ..models import Article,Category,Tag
from django.db.models.aggregates import Count
register = template.Library()

# @register.filter
# def get_key(d, key_name):
#     return d.get(key_name)
#
# @register.filter
# def get_attr(d, m):
#     if hasattr(d, m):
#         return getattr(d, m)

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
    #模板中可以获取类名和分类下的文章数num_articles
    return Category.objects.annotate(num_articles=Count('article')).filter(num_articles__gt=0)  #注意此处有两个_

#获取文章归档下的文章数量
@register.filter
def get_articlenums(date):
    return Article.objects.filter(create_time__year=date.year, create_time__month=date.month).count()

@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_articles=Count('article')).filter(num_articles__gt=0)
