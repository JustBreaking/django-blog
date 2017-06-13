#encoding:utf-8
from django import template
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

register = template.Library()

#装饰器表明这个函数是一个模板标签，takes_context=True 表示接受上下文对象，即 Context对象
@register.simple_tag(takes_context=True)
#object_list是要分页的对象，page_count表示每页的数量
def paginate(context, object_list, page_count):
    left = 3 #当前页码左边显示几个页码号 -1 ，比如3就显示2页
    right = 3 #当前页面右边显示几个页码号 -1

    paginator = Paginator(object_list, page_count)
    page = context['request'].GET.get('page') #从http请求中获取用户请求的页码号

    try:
        object_list = paginator.page(page)  #根据页码号获取当页数据
        context['current_page'] = int(page)
        #调用了两个辅助函数，根据当前页获得了左右的页码号，比如当前为第5页，num_pages 不小于7，那么pages = [3,4,5,6,7]
        pages = get_left(context['current_page'], left, paginator.num_pages) + get_right(context['current_page'], right, paginator.num_pages)
    except PageNotAnInteger:
        #异常处理  如果用户传递的page不是整数，则把第一页返回给他
        object_list = paginator.page(1)
        context['current_page'] = 1
        pages = get_right(context['current_page'], right, paginator.num_pages)
    except EmptyPage:
        #如果用户传递的值为空值，则把最后一页返回
        object_list = paginator.page(paginator.num_pages)
        context['current_page'] = paginator.num_pages
        pages = get_left(context['current_page'], left, paginator.num_pages)

    context['article_list'] = object_list   #封装获取到的分页数据
    context['pages'] = pages
    context['first_page'] = 1
    context['last_page'] = paginator.num_pages
    try:
        context['pages_first'] = pages[0]
        context['pages_last'] = pages[-1] +1 #  +1为了判断，在模板文件中体会
    except IndexError:
        context['pages_first'] = 1  #发生异常说明只有一页
        context['pages_last'] = 2 # 1+1 后的值

    return ''   #必须加这项，否则首页会显示None

#辅助函数，获取当前页码值左边的两个值，会处理一些细节
def get_left(current_page, left, num_pages):
    if current_page == 1:
        return []
    elif current_page == num_pages:
        l = [i-1 for i in range(current_page, current_page-left, -1) if i-1 > 1]
        l.sort()
        return l
    l = [i for i in range(current_page, current_page-left, -1) if i > 1]
    l.sort()
    return l

def get_right(current_page, right, num_pages):
    if current_page == num_pages:
        return []
    return [i+1 for i in range(current_page, current_page+right, 1) if i < num_pages-1 ]
