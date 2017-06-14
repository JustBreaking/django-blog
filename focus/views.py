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

#通过添加了分页功能的类视图IndexView来实现
# def index(request):
#     latest_article_list = Article.objects.query_by_time()
#     articles_info = []
#     dic = {}
#     for article in latest_article_list:
#         taginfo = Article.objects.get(id=article.id)
#         dic['tag_list'] = taginfo.tags.all()
#         dic['article'] = article;
#         articles_info.append(dic)
#         dic = {}
#
#     loginform = LoginForm()
#     context = {'articles_info':articles_info, 'loginform':loginform}
#     return render(request, 'index.html', context)

'''
blog首页，通过调用as_view() 方法实现和视图函数index相同的功能,CategoryView和ArchivesView可以直接继承该类
该类未添加分页功能
'''
# class IndexView(ListView):
#     '''
#     model:将model指定为Article，告诉django要获取的模型是Article
#     template_name:指定这个视图的渲染模板
#     context_object_name:指定 获取的模型列表数据 保存的变量名，该变量会被传递给模板
#     '''
#     model = Article
#     template_name = 'index.html'
#     context_object_name = 'articles_info'
#     article_list = []
#     paginate_by = 1
#
#     def get_queryset(self):
#         self.article_list = Article.objects.query_by_time()
#     def get_context_data(self, **kwargs):
#         articles_info = []
#         dic = {}
#         for article in self.article_list:
#             taginfo = Article.objects.get(id=article.id)
#             dic['tag_list'] = taginfo.tags.all()
#             dic['article'] = article;
#             articles_info.append(dic)
#             dic = {}
#
#         loginform = LoginForm()
#         context = {'articles_info':articles_info, 'loginform':loginform}
#         return context

#添加分页功能
class IndexView(ListView):
    '''
    model:将model指定为Article，告诉django要获取的模型是Article
    template_name:指定这个视图的渲染模板
    context_object_name:指定 获取的模型列表数据 保存的变量名，该变量会被传递给模板
    '''
    model = Article
    template_name = 'index.html'
    context_object_name = 'article_list'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        '''
        在视图函数中将模板变量传递给模板是通过给 render 函数的 context 参数传递一个字典实现的，
        例如 render(request, 'blog/index.html', context={'post_list': post_list})，
        这里传递了一个 {'post_list': post_list} 字典给模板。
        在类视图中，这个需要传递的模板变量字典是通过 get_context_data 获得的，
        所以我们复写该方法，以便我们能够自己再插入一些我们自定义的模板变量进去。
        '''
        #首先获得父类生成的传递给模板的字典
        context = super(IndexView,self).get_context_data(**kwargs)
        '''
        父类生成的字典中已有 paginator、page_obj、is_paginated 这三个模板变量，
        paginator 是 Paginator 的一个实例，
        page_obj 是 Page 的一个实例，
        is_paginated 是一个布尔变量，用于指示是否已分页。
        例如如果规定每页 10 个数据，而本身只有 5 个数据，其实就用不着分页，此时 is_paginated=False
        由于 context 是一个字典，所以调用 get 方法从中取出某个键对应的值
        '''
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')
        article_list = context.get('article_list')

        #调用自己写的pagination_data 方法获得显示分页导航条需要的数据
        pagination_data = self.pagination_data(paginator, page, is_paginated)
        #将分页信息数据更新到context中，注意pagination_data方法返回的也是一个字典
        context.update(pagination_data)

        loginform = LoginForm()
        #将articles_info和loginform 加入到context中
        context.update({'loginform':loginform,})
        #将更新后的context返回，以便使用这个字典中的模板变量去渲染模板
        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            # 如果没有分页，则无需显示分页导航条，不用任何分页导航条的数据，因此返回一个空的字典
            return {}

        # 当前页左边连续的页码号，初始值为空
        left = []

        # 当前页右边连续的页码号，初始值为空
        right = []

        # 标示第 1 页页码后是否需要显示省略号
        left_has_more = False

        # 标示最后一页页码前是否需要显示省略号
        right_has_more = False

        # 标示是否需要显示第 1 页的页码号。
        # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
        # 其它情况下第一页的页码是始终需要显示的。
        # 初始值为 False
        first = False

        # 标示是否需要显示最后一页的页码号。
        # 需要此指示变量的理由和上面相同。
        last = False

        # 获得用户当前请求的页码号
        page_number = page.number

        # 获得分页后的总页数
        total_pages = paginator.num_pages

        # 获得整个分页页码列表，比如分了四页，那么就是 [1, 2, 3, 4]
        page_range = paginator.page_range
        print page_number,total_pages,page_range

        if page_number == 1:
            # 如果用户请求的是第一页的数据，那么当前页左边的不需要数据，因此 left=[]（已默认为空）。
            # 此时只要获取当前页右边的连续页码号，
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 right = [2, 3]。
            # 注意这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            right = list(page_range)[page_number:page_number + 2]

            # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
            # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
            if right[-1] < total_pages - 1:
                right_has_more = True

            # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
            # 所以需要显示最后一页的页码号，通过 last 来指示
            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:
            # 如果用户请求的是最后一页的数据，那么当前页右边就不需要数据，因此 right=[]（已默认为空），
            # 此时只要获取当前页左边的连续页码号。
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 left = [2, 3]
            # 这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            left = list(page_range)[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

            # 如果最左边的页码号比第 2 页页码号还大，
            # 说明最左边的页码号和第 1 页的页码号之间还有其它页码，因此需要显示省略号，通过 left_has_more 来指示。
            if left[0] > 2:
                left_has_more = True

            # 如果最左边的页码号比第 1 页的页码号大，说明当前页左边的连续页码号中不包含第一页的页码，
            # 所以需要显示第一页的页码号，通过 first 来指示
            if left[0] > 1:
                first = True
        else:
            # 用户请求的既不是最后一页，也不是第 1 页，则需要获取当前页左右两边的连续页码号，
            # 这里只获取了当前页码前后连续两个页码，你可以更改这个数字以获取更多页码。
            left = list(page_range)[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = list(page_range)[page_number:page_number + 2]

            # 是否需要显示最后一页和最后一页前的省略号
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            # 是否需要显示第 1 页和第 1 页后的省略号
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data

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

def detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    article.increase_views()
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

# 交给了单独的 comments app模块实现
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
'''
#文章归档，通过调用as_view() 方法实现和视图函数archives相同的功能
#参考http://zmrenwu.com/post/33/#c399
# ArchivesView 和 IndexView 类中的属性值完全一样，唯一不同的是文章列表，这里通过重写get_queryset方法找出归档下的文章列表
#最终实现归档页面的分页功能
'''
class ArchivesView(IndexView):
    #覆盖父类的get_queryset方法，该方法默认获取了指定模型的全部数据列表，为了获取特定时间的文章列表，这里通过filter进行筛选
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchivesView,self).get_queryset().filter(create_time__year=year, create_time__month=month)

# CategoryView 和 IndexView 类中的属性值完全一样，唯一不同的是文章列表，这里通过重写get_queryset方法找出归档下的文章列表
class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, id=self.kwargs.get('category_id'))
        return super(CategoryView,self).get_queryset().filter(category=cate)

class TagView(IndexView):
    def get_queryset(self):
        tag = get_object_or_404(Tag, id=self.kwargs.get('tag_id'))
        return super(TagView,self).get_queryset().filter(tags=tag)

# class CategoryView(IndexView):
#     def get_queryset(self):
#         cate = get_object_or_404(Category, id=self.kwargs.get('category_id'))
#         self.article_list = Article.objects.filter(category=cate)
#     def get_context_data(self, **kwargs):
#         context = super(IndexView,self).get_context_data(**kwargs)
#
#         paginator = context.get('paginator')
#         page = context.get('page_obj')
#         is_paginated = context.get('is_paginated')
#         article_list = context.get('article_list')
#
#         articles_info = []
#         dic = {}
#         for article in article_list:
#             taginfo = Article.objects.get(id=article.id)
#             dic['tag_list'] = taginfo.tags.all()
#             dic['article'] = article;
#             articles_info.append(dic)
#             dic = {}
#         loginform = LoginForm()
#         #将articles_info和loginform 加入到context中
#         context.update({
#             'articles_info':articles_info,
#             'loginform':loginform,
#         })
#         #将更新后的context返回，以便使用这个字典中的模板变量去渲染模板
#         return context

def archives(request, year, month): #文章归档
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
