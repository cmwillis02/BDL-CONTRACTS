# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-18 01:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0008_auto_20171017_2138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='franchise_fact',
            name='opponent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Franchise', to='contracts.Franchise'),
        ),
        migrations.AlterField(
            model_name='player_fact',
            name='franchise',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contracts.Franchise'),
        ),
    ]
