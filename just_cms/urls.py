#encoding:utf-8
"""just_cms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from focus import urls as focus_urls
from comments import urls as comments_urls
from focus import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^focus/', include(focus_urls)),
    url(r'^comments/', include(comments_urls)),
    # url(r'^$', views.index, name='index'),
    url(r'^$', views.IndexView.as_view(), name='index'),  #通过类视图实现
    url(r'', include('ckeditor_uploader.urls')),
]   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
