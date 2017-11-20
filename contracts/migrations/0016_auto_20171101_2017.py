# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-02 00:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0015_remove_week_run_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='current_years',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='contract',
            name='franchise',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contract', to='contracts.Franchise'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contract', to='contracts.Player'),
        ),
    ]