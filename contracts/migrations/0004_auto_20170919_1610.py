# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-19 20:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0003_contract_years'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='contract_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]