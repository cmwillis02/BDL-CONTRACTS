# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-19 19:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0002_auto_20170919_1515'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='years',
            field=models.IntegerField(default=0),
        ),
    ]
