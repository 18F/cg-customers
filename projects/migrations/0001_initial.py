# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-22 16:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('packages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agency', models.CharField(max_length=16, verbose_name='Agency')),
                ('project_name', models.CharField(max_length=128, verbose_name='Project Name')),
                ('org_manager', models.CharField(max_length=64, verbose_name='Org Manager')),
                ('iaa_agreement', models.CharField(max_length=64, verbose_name='IAA Agreement')),
                ('system_owner', models.CharField(max_length=64, verbose_name='System Owner')),
                ('quota_memory_limit', models.PositiveIntegerField(verbose_name='Quota Memory Limit (in GB)')),
                ('is_free', models.BooleanField(default=False)),
                ('package_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='packages.Package')),
            ],
        ),
    ]