# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-28 02:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='fact_franchise',
            new_name='franchise_fact',
        ),
        migrations.RenameModel(
            old_name='fact_player',
            new_name='player_fact',
        ),
    ]