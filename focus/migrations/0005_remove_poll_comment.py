# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-06 02:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('focus', '0004_auto_20170606_0219'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poll',
            name='comment',
        ),
    ]