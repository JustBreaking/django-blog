## 一个简易的django博客

------

### 环境
> * Django 1.11.1
> * python 2.7.13
> * sqlite(django自带)

### 创建django项目
创建一个名为mysite的项目,创建成功会自动生成一个名为mysite的文件夹
```
django-admin startproject mysite(若创建失败可能需要使用 django-admin.py)
```
进入mysite，目录结构为
```
.
├── manage.py
└── mysite
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```
文件说明：
* manage.py：与Django进行交互的命令行工具，比如后面根据model生成数据库表结构、供开发使用的server等都是使用该工具，在manage.py的同级目录使用python manage.py 可以看到可以使用的命令列表。
* mysite：该django工程的包名。
* mysite/__init__.py：表明mysite是一个包。
* setting.py：Django的配置文件，包括工程的app配置、数据库配置、语言配置等。
* urls.py：Django的dispatcher，根据不同的url映射到不同的视图。
* wsgi.py：WSGI是web server gateway interface，这个文件是使project符合这种协议的入口点（entry-point）

启动服务
```
python manage.py runserver
```
然后打开浏览器 输入 http://127.0.0.1:8000 就可以看到服务启动了！

在mysite下创建一个名为users的app
首先进入到mysite，然后
```
django-admin startapp users
```
users创建成功后，django在myysite下创建一个user文件夹
至此mysite的文件目录结构为：
```
.
├── manage.py
├── mysite
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── users
    ├── admin.py
    ├── apps.py
    ├── __init__.py
    ├── migrations
    │   └── __init__.py
    ├── models.py
    ├── tests.py
    └── views.py
```
文件说明
* users：app的根目录

* admin.py：Django自带了一个管理界面，这个文件可以注册model在界面中管理

* __init__.py：表明polls也是一个包

* migrations：用来初始化数据库，在执行python manage.py makemigrations 的时候会自动生成一个文件在这里

* __init__.py：表明migrations也是一个包

* models.py：在这个文件里面定义model类

* tests.py：写测试代码

* views.py：视图，Django映射urls.py里面的url的时候，在views.py里面查找对应的处理方法

### 快速启动该项目
1. 克隆项目
```
git init
git clone https://github.com/JustBreaking/django-blog.git
```
2. 安装依赖包
```
pip install requirements.txt
```
3. 同步数据库
```
python manage.py makemigrations
python manage.py migrate
```
