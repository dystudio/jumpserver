# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-06 10:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20180125_1218'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['username'], 'verbose_name': 'User'},
        ),
        migrations.AlterModelOptions(
            name='usergroup',
            options={'ordering': ['name'], 'verbose_name': 'User group'},
        ),
    ]