# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-13 04:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emusic', '0008_favorite_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='fb_image',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='fb_name',
        ),
    ]
