# -*- coding: utf-8 -*-
from django.contrib import admin
from django.db import models
from django import forms
from .models import Article, Category, NewUser, Author, Tag

class ArticleAdmin(admin.ModelAdmin):
    # formfield_overrides = {     #修改article 中 TextField字段的显示区域大小
    #     models.TextField:{
    #         'widget':forms.Textarea(
    #             attrs={'rows':20, 'cols':50}
    #         )
    #     }
    # }
    list_display = ('title','create_time','like_num')

class NewUserAdmin(admin.ModelAdmin):
    list_display = ('username','date_joined','profile')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','intro')

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name','profile')
class TagAdmin(admin.ModelAdmin):
    list_display=('name', 'create_time')

admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(NewUser, NewUserAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Tag, TagAdmin)
