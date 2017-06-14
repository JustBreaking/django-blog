#encoding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from django.contrib.syndication.views import Feed
from .models import Article

class AllArticleRssFeed(Feed):
    #显示在聚合阅读器上的标题
    title = "Django blog tutorial"

    #通过聚合阅读器转到网站的地址
    link = "/"

    #显示在阅读器上的描述信息
    description = "django 博客项目测试文章"

    #需要显示的内容条目
    def items(self):
        return Article.objects.all()

    #聚合器中显示内容条目的标题
    def item_title(self, item):
        return '[%s] %s' % (item.category, item.title)

    #聚合器中显示内容条目的描述
    def item_description(self, item):
        return item.content
