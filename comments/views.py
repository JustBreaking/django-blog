# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from focus.models import Article
from .models import Comment
from .forms import CommentForm

def article_comment(request, article_id):
    article = get_object_or_404(Article, id=article_id) #获取评论对应的文章，该函数文章不存在时返回404
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)   #commit=False的作用是，仅仅利用表单的数据生成 Comment模型的实例，但还不保存到数据库
            comment.article = article   #将评论和文章关联起来
            comment.user = request.user
            comment.save()
            article.comment_num += 1
            article.save()
            #重定向 article的详情页，实际上当redirect函数接受一个模型的实例时，他会调用这个模型实例的get_absolute_url方法
            #然后重定向到get_absolute_url方法返回的url
            return redirect(article)
        else:
            #检测到表单数据不合法，重新渲染详情页，并且渲染表单的错误
            '''
            我们使用了 post.comment_set.all() 来获取 post 对应的全部评论。 Comment 和Post 是通过 ForeignKey 关联的，回顾一下我们当初获取某个分类 cate 下的全部文章时的代码：Post.objects.filter(category=cate)。这里 post.comment_set.all() 也等价于 Comment.objects.filter(post=post)，即根据 post 来过滤该 post 下的全部评论。但既然我们已经有了一个 Post 模型的实例 post（它对应的是 Post 在数据库中的一条记录），那么获取和 post 关联的评论列表有一个简单方法，即调用它的 xxx_set 属性来获取一个类似于 objects 的模型管理器，然后调用其 all 方法来返回这个 post 关联的全部评论。 其中 xxx_set 中的 xxx 为关联模型的类名（小写）。例如 Post.objects.filter(category=cate) 也可以等价写为 cate.post_set.all()。
            '''
            comment_list = article.comment_set.all()   #等价于 Comment.objects.filter(article=article)
            context = {'article':article, 'form':form, 'comment_list':comment_list}
            return render(request, 'detail.html', context)
    #不是post请求，说明用户没有提交数据，重定向到详情页
    return redirect(article)
