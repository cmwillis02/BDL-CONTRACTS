# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-18 02:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0009_auto_20171017_2142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='week',
            name='run_status',
            field=models.IntegerField(),
        ),
    ]