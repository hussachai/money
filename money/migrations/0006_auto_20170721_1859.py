# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-22 01:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0005_auto_20170713_2008'),
    ]

    operations = [
        migrations.CreateModel(
            name='StmtBalanceSummary',
            fields=[
            ],
            options={
                'verbose_name': 'Statement Summary',
                'verbose_name_plural': 'Statements Summary',
                'proxy': True,
                'indexes': [],
            },
            bases=('money.stmtbalance',),
        ),
        migrations.AlterModelOptions(
            name='bankaccount',
            options={'verbose_name': 'Bank Account', 'verbose_name_plural': 'Bank Accounts'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='creditaccount',
            options={'ordering': ['closed_date', 'name', 'opened_date'], 'verbose_name': 'Credit Account', 'verbose_name_plural': 'Credit Accounts'},
        ),
        migrations.AlterModelOptions(
            name='incomestmt',
            options={'verbose_name': 'Income Statement', 'verbose_name_plural': 'Income Statements'},
        ),
        migrations.AlterModelOptions(
            name='stmtbalance',
            options={'ordering': ['-closing_date', 'account'], 'verbose_name': 'Statement Balance', 'verbose_name_plural': 'Statements Balance'},
        ),
        migrations.AlterModelOptions(
            name='stmtdetail',
            options={'ordering': ['balance__closing_date', 'tx_date'], 'verbose_name': 'Statement Detail', 'verbose_name_plural': 'Statements Detail'},
        ),
        migrations.AddField(
            model_name='incomestmt',
            name='linked_account',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='money.CreditAccount'),
            preserve_default=False,
        ),
    ]
