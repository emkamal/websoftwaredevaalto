# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-09 19:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameapp', '0010_remove_taxonomy_games'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='state',
            field=models.CharField(default='error', max_length=50),
        ),
    ]
