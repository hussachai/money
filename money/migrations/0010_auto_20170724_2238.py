# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-25 05:38
from __future__ import unicode_literals

import colorfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0009_auto_20170723_0025'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnnualGoal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.SmallIntegerField()),
                ('target_saving', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
            options={
                'verbose_name': 'Annual Goal',
                'verbose_name_plural': 'Annual Goals',
                'db_table': 'money_annual_goals',
                'ordering': ['-year'],
            },
        ),
        migrations.AlterModelOptions(
            name='incomestmt',
            options={'ordering': ['-tx_date', 'account'], 'verbose_name': 'Income Statement', 'verbose_name_plural': 'Income Statements'},
        ),
        migrations.AlterModelOptions(
            name='stmtdetail',
            options={'ordering': ['-balance__closing_date', '-tx_date'], 'verbose_name': 'Statement Detail', 'verbose_name_plural': 'Statements Detail'},
        ),
        migrations.AlterField(
            model_name='category',
            name='color',
            field=colorfield.fields.ColorField(default='#9370DB', max_length=18),
        ),
    ]
