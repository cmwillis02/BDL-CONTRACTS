# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-18 18:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('contract_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('current_ind', models.BooleanField()),
                ('date_assigned', models.DateField()),
                ('date_terminated', models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Franchise',
            fields=[
                ('franchise_id', models.IntegerField(primary_key=True, serialize=False)),
                ('team_name', models.CharField(max_length=50)),
                ('owner_name', models.CharField(max_length=50)),
                ('owner_email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('player_id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('position', models.CharField(choices=[('q', 'QB'), ('r', 'RB'), ('w', 'WR'), ('t', 'TE'), ('k', 'PK'), ('d', 'DEF')], max_length=1)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='contract',
            name='franchise_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contracts.Franchise'),
        ),
        migrations.AddField(
            model_name='contract',
            name='player_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contracts.Player'),
        ),
    ]