# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-13 06:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0003_creditaccount_closed_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creditaccount',
            name='closed_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
