# -*- coding: utf-8 -*-
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse

class ArticleManager(models.Manager):
    def query_by_column(self, category_id):
        query = self.get_queryset().filter(category_id=category_id)
    def query_by_user(self, user_id):
        user = User.objects.get(id=user_id)
        article_list = user.article_set.all()
        return article_list
    def query_by_polls(self):
        query = self.get_queryset().order_by('likes')
        return query
    def query_by_time(self):
        query = self.get_queryset().order_by('-create_time')
        return query
    def query_by_keyword(self, keyword):
        query = self.get_queryset().filter(title__contains=keyword)
        return query

@python_2_unicode_compatible
class NewUser(AbstractUser):
    profile = models.CharField('profile', default='', max_length=256)
    def __str__(self):
        return self.username

@python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField('类名', max_length=16)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    intro = models.TextField('introduction', default='')

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Author(models.Model):
    name = models.CharField('姓名', max_length=256)
    profile = models.CharField('简介', default='', max_length=256)
    register_time = models.DateTimeField(auto_now_add=True, editable=True)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Tag(models.Model):
    name = models.CharField('标签名',  max_length=16)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Article(models.Model):
    STATUS_CHOICES = (
        ('d', 'Draft'),
        ('p', 'Published'),
    )
    title = models.CharField('标题', max_length = 64)
    author = models.ForeignKey(Author, verbose_name='作者', null=True, on_delete=models.SET_NULL)
    # content = models.TextField('正文')
    content = RichTextUploadingField(verbose_name='正文')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)   #文章添加时自动添加创建时间
    last_modified_time = models.DateTimeField('最近编辑时间', auto_now=True)
    status = models.CharField('文章状态', max_length=1, choices=STATUS_CHOICES)
    #文章摘要 help_text 在该 field 被渲染成  form 时 显示帮助信息
    abstract = models.CharField('摘要', max_length=54, blank=True, null=True, help_text="可选，如若为空将摘取正文前54个字符")
    # PositiveIntegerField 存储非负整数
    views = models.PositiveIntegerField('浏览量', default=0)
    topped = models.BooleanField('置顶', default=False)
    #on_delete=models.SET_NULL 表示删除category分类后该分类下所有的Article的外键均设为null
    category = models.ForeignKey(Category, verbose_name='分类', null=True, on_delete=models.SET_NULL)
    comment_num = models.PositiveIntegerField('评论数', default=0)
    keep_num = models.PositiveIntegerField('收藏数', default=0)
    like_num = models.PositiveIntegerField('点赞数', default=0)
    tags = models.ManyToManyField(Tag, verbose_name='标签集合', blank=True)

    def __str__(self):
        #主要用于交互解释器显示表示该类的字符串
        return self.title
    def get_absolute_url(self):
        return reverse('focus:detail', kwargs={'article_id': self.id})		#在模板中可以直接调用,获取最新文章

    class Meta:
        # Meta包含一系列选项,此处ordering 表示排序， - 逆序
        ordering = ['-last_modified_time']
    objects = ArticleManager()
    
#comment 在 comments 单独的app下完成
# @python_2_unicode_compatible
# class Comment(models.Model):
#     user = models.ForeignKey(NewUser, null=True)
#     article = models.ForeignKey(Article, null=True)
#     content = models.TextField()
#     create_time = models.DateTimeField(auto_now_add=True, editable=True)
#     poll_num = models.IntegerField(default=0)
#
#     def __str__(self):
#         return self.content

class Poll(models.Model):   #点赞
    user = models.ForeignKey(NewUser, null=True)
    article = models.ForeignKey(Article, null=True)

class Keep(models.Model):   #收藏
    article = models.ForeignKey(Article, null=True)
    user = models.ForeignKey(NewUser, null=True)
