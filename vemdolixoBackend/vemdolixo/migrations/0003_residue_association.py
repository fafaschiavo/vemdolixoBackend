# -*- coding: utf-8 -*-
# Generated by Django 1.10.dev20160307181939 on 2016-09-21 22:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vemdolixo', '0002_members_profile_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='residue_association',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term', models.CharField(max_length=200)),
                ('residue_id', models.IntegerField(default=0)),
            ],
        ),
    ]
