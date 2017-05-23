# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-23 13:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('iaa', '__first__'),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='iaa_agreement',
        ),
        migrations.AddField(
            model_name='project',
            name='iaa',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='iaa.IAA'),
        ),
    ]
