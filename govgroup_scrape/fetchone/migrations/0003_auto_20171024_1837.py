# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-24 18:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fetchone', '0002_detaillink_listinlink'),
    ]

    operations = [
        migrations.AddField(
            model_name='detaillink',
            name='crawled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='listinlink',
            name='crawled',
            field=models.BooleanField(default=False),
        ),
    ]