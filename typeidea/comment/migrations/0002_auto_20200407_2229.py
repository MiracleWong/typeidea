# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-04-07 14:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='邮箱'),
        ),
    ]
