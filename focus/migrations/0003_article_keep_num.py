# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-05 18:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('focus', '0002_auto_20170606_0143'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='keep_num',
            field=models.BooleanField(default=False, verbose_name=b'\xe6\x94\xb6\xe8\x97\x8f'),
        ),
    ]
