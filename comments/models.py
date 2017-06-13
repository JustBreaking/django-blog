# -*- coding: utf-8 -*-
from django.db import models
# from django.utils.six import python_2_unicode_compatible
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Comment(models.Model):
    user = models.ForeignKey('focus.NewUser')
    content = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey('focus.Article')

    def __str__(self):
        return self.content[:20]
