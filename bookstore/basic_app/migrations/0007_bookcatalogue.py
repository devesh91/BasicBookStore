# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-29 04:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app', '0006_remove_userprofileinfo_portfolio_site'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookCatalogue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_id', models.PositiveIntegerField(unique=True)),
                ('book_name', models.CharField(max_length=256)),
            ],
        ),
    ]
