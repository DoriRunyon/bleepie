# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-24 22:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meepo', '0002_auto_20170620_0153'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='on_watch',
            field=models.BooleanField(default=False),
        ),
    ]
