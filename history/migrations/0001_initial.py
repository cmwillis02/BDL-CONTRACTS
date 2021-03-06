# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-02-06 22:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contracts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='franchise_fact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matchup_type', models.CharField(choices=[('p', 'Playoffs'), ('r', 'Regular Season'), ('b', 'Bye')], max_length=1)),
                ('result', models.CharField(choices=[('w', 'Win'), ('l', 'Loss'), ('t', 'Tie')], max_length=1, null=True)),
                ('total_score', models.FloatField()),
                ('opponent_score', models.FloatField(null=True)),
                ('franchise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contracts.Franchise')),
                ('opponent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Franchise', to='contracts.Franchise')),
                ('week', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contracts.Week')),
            ],
        ),
        migrations.CreateModel(
            name='player_awards',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
                ('year', models.IntegerField()),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contracts.Player')),
            ],
        ),
        migrations.CreateModel(
            name='player_fact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roster_status', models.CharField(choices=[('s', 'Starter'), ('b', 'Bench'), ('i', 'IR'), ('f', 'Free Agent')], max_length=50)),
                ('score', models.FloatField(null=True)),
                ('franchise', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contracts.Franchise')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contracts.Player')),
                ('week', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contracts.Week')),
            ],
        ),
        migrations.CreateModel(
            name='player_milestones',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contracts.Player')),
                ('week', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contracts.Week')),
            ],
        ),
    ]
