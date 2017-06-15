#encoding:utf-8
from django import forms
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from .models import NewUser

class LoginForm(forms.Form):
    uid = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'id':'uid', 'placeholder': 'Username'}))
    pwd = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'id':'pwd', 'placeholder':'Password'}))

# def email_validate(value):
#     email_re = re.compile(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$')
#     if not email_re.match(value):
#         raise ValidationError('邮箱格式错误')
#
# class RegisterForm(forms.Form):
#     username = forms.CharField(label='username', max_length=100,
#         widget=forms.TextInput(attrs={'id':'username', 'onblur':'authentication()','placeholder': 'Username',}),
#         error_messages = {'required':'bunennegewf'})
#     email = forms.EmailField(widget=forms.TextInput(attrs={'id':'email', 'placeholder': 'email'}))
#     password1 = forms.CharField(widget=forms.PasswordInput(attrs={'id':'password1', 'placeholder': 'password'}))
#     password2 = forms.CharField(widget=forms.PasswordInput(attrs={'id':'password2', 'placeholder': 'please comfirm password'}))

class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = NewUser
        fields = ("username", "email")

class SetInfoForm(forms.Form):
    username = forms.CharField()

# class CommmentForm(forms.Form):
#     comment = forms.CharField(label='', widget=forms.Textarea(attrs={'cols': '60', 'rows': '6'}))

class SearchForm(forms.Form):
    keyword = forms.CharField(widget=forms.TextInput)
