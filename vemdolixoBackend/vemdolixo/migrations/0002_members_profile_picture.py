# -*- coding: utf-8 -*-
# Generated by Django 1.10.dev20160307181939 on 2016-09-06 14:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vemdolixo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='members',
            name='profile_picture',
            field=models.CharField(default='https://s3-sa-east-1.amazonaws.com/residoando/user.svg', max_length=400),
        ),
    ]
