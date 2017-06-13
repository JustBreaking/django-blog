# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, Poll, NewUser,Keep, Tag, Category
from comments.forms import CommentForm
from .forms import LoginForm, RegisterForm, SetInfoForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.contrib.auth.hashers import make_password
from django.http  import  HttpResponseRedirect
from django.views.generic import ListView

import markdown, urlparse

def index(request):
    latest_article_list = Article.objects.query_by_time()
    articles_info = []
    dic = {}
    for article in latest_article_list:
        taginfo = Article.objects.get(id=article.id)
        dic['tag_list'] = taginfo.tags.all()
        dic['article'] = article;
        articles_info.append(dic)
        dic = {}

    loginform = LoginForm()
    context = {'articles_info':articles_info, 'loginform':loginform}
    return render(request, 'index.html', context)

def log_in(request):        #注意该处命名不能为login，会重名导致错误
    if request.user.is_authenticated:
        return redirect('/focus')
    if request.method == 'GET':
        form = LoginForm()
        # request.session['login_from'] = request.META.get('HTTP_REFERER', '/')   #记住原来的URL，如果没有则设置为首页('/')
        return render(request, 'login.html', {'form':form})
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['uid']
            password = form.cleaned_data['pwd']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # url = request.POST.get('source_url', '/focus')
                # return redirect(url)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))  #定向到登录之前的url
            else:
                return render(request, 'login.html', {'form':form, 'error':'password or username is not true!'})
        else:
            return render(request, 'login.html', {'form':form})

@login_required
def log_out(request):
    url = request.POST.get('source_url', '/focus')
    logout(request)
    return redirect(url)

# def article(request, article_id):
#     article = get_object_or_404(Article, id=article_id)
#     taginfo = Article.objects.get(id=article_id)  #多对多查询
#     tag_list = taginfo.tags.all()
#
#     #根据标签查询对应文章
#     # articleinfo = Tag.objects.get(id=3)
#     # article_list = articleinfo.article_set.all()
#
#     content = markdown2.markdown(article.content, extras=[
#         "code-friendly",
#         "fenced-code-blocks",
#         "header-ids",
#         "toc",
#         "metadata"
#     ])
#     commentform = CommmentForm()
#     loginform = LoginForm()
#     comments = article.comment_set.all
#
#     return render(request, 'detail.html', {
#         'article':article,
#         'tag_list':tag_list,
#         'loginform':loginform,
#         'commentform':commentform,
#         'content':content,
#         'comments':comments
#     })

def article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    taginfo = Article.objects.get(id=article_id)  #多对多查询
    tag_list = taginfo.tags.all()
    loginform = LoginForm()
    article.content = markdown.markdown(article.content, extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    form = CommentForm()
    #获取该article所有的comment
    comment_list = article.comment_set.all()
    context = {
        'article':article,
        'form':form,
        'loginform':loginform,
        'comment_list':comment_list,
        'tag_list':tag_list,
    }
    return render(request, 'detail.html', context)

# @login_required
# def comment(request, article_id):
#     form = CommmentForm(request.POST)
#     url = urlparse.urljoin('/focus/', article_id)
#     if form.is_valid():
#         user = request.user
#         article = Article.objects.get(id=article_id)
#         new_comment = form.cleaned_data['comment']
#         #构造一个评论的对象
#         c = Comment(content=new_comment, article_id=article_id)
#         #查询，此处应该为构造一个新的comment，而这个为从数据库查询，所以此处不合适
#         # c = Comment.objects.get(content=new_comment, article_id=article_id)
#         c.user = user
#         c.save()
#         article.comment_num += 1
#         article.save()
#     return redirect(url)

@login_required
def get_keep(request, article_id):  #收藏 keep
    logged_user = request.user
    article = Article.objects.get(id=article_id)
    is_keep = Keep.objects.filter(article_id=article_id, user_id=logged_user.id)
    if len(is_keep) == 0:  #未收藏，点击收藏
        article.keep_num += 1
        article.save()
        keep = Keep(article=article, user=logged_user)
        keep.save()
    else:           #已收藏，点击取消收藏
        article.keep_num -= 1
        article.save()
        Keep.objects.get(article_id=article_id, user_id=logged_user.id).delete()
    url = urlparse.urljoin('/focus/', article_id)
    return redirect(url)



@login_required
def get_poll(request, article_id):  #点赞 poll
    logged_user = request.user
    article = Article.objects.get(id=article_id)
    is_poll = Poll.objects.filter(article_id=article_id, user_id=logged_user.id)
    if len(is_poll) == 0:  #未收藏，点击收藏
        article.like_num += 1
        article.save()
        poll = Poll(article=article, user=logged_user)
        poll.save()
    else:           #已收藏，点击取消收藏
        article.like_num -= 1
        article.save()
        Poll.objects.get(article_id=article_id, user_id=logged_user.id).delete()
    url = urlparse.urljoin('/focus/', article_id)
    return redirect(url)

def register(request):
    error1 = "the name is already exist"
    valid = "this name is valid"
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'register.html', {'form':form})
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if request.POST.get('raw_username', 'erjgiqfv240hqp5668ej23foi') != 'erjgiqfv240hqp5668ej23foi':
            try:
                user = NewUser.objects.get(username=request.POST.get('raw_username', ''))
            except ObjectDoesNotExist:
                return render(request, 'register.html', {'form':form, 'msg':valid})
            else:
                return render(request, 'register.html', {'form':form, 'msg':error1})
        else:
            if form.is_valid():
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                password1 = form.cleaned_data['password1']
                password2 = form.cleaned_data['password2']
                if password1 != password2:
                    return render(request, 'register.html', {'form':form, 'msg':'Do not match the password input'})
                else:
                    password = make_password(password2, None, "pbkdf2_sha256")
                    user = NewUser(username=username, email=email, password=password)
                    user.save()
                    # return render(request, 'login.html', {'success':'you have successfully registered!'})
                    return redirect('/focus/login')
            else:
                return render(request, 'register.html', {'form':form, 'msg':'input msg is invalid!'})

class ArchivesView(ListView):   #文章归档
    model = Article
    template_name = 'index.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchivesView, self).get_queryset().filter(create_time__year=year,
                                                               create_time__month=month
                                                               )

class CategoryView(ListView):   #文章分类
    model = Article
    template_name = 'index.html'
    context_object_name = 'categories_list'

    def get_queryset(self):
        cate = get_object_or_404(Category, id=self.kwargs.get('category_id'))
        return super(CategoryView, self).get_queryset().filter(category=cate)

def archives(request, year, month):
    article_list = Article.objects.filter(create_time__year=year, create_time__month=month).order_by('-create_time')
    articles_info = []
    dic = {}
    for article in article_list:
        taginfo = Article.objects.get(id=article.id)
        dic['tag_list'] = taginfo.tags.all()
        dic['article'] = article;
        articles_info.append(dic)
        dic = {}

    loginform = LoginForm()
    context = {'articles_info':articles_info, 'loginform':loginform}
    return render(request, 'index.html', context)

def category(request, category_id):
    cate = get_object_or_404(Category, id=category_id)
    article_list = Article.objects.filter(category=cate).order_by('-create_time')
    articles_info = []
    dic = {}
    for article in article_list:
        taginfo = Article.objects.get(id=article.id)
        dic['tag_list'] = taginfo.tags.all()
        dic['article'] = article;
        articles_info.append(dic)
        dic = {}

    loginform = LoginForm()
    context = {'articles_info':articles_info, 'loginform':loginform}
    return render(request, 'index.html', context)
