# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-12 10:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Process',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('process_name', models.CharField(max_length=128, unique=True, verbose_name='\u5de5\u5e8f\u540d')),
                ('process_code', models.CharField(max_length=16, verbose_name='\u5de5\u5e8f\u4ee3\u7801')),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('product_id', models.IntegerField(primary_key=True, serialize=False, verbose_name='\u4ea7\u54c1ID')),
                ('product_name', models.CharField(max_length=128, unique=True, verbose_name='\u4ea7\u54c1\u540d')),
                ('order_num', models.IntegerField(verbose_name='\u8ba2\u5355\u6570\u91cf')),
                ('deliver_date', models.DateField(max_length=8, verbose_name='\u4ea4\u8d27\u65e5\u671f')),
            ],
        ),
        migrations.AddField(
            model_name='process',
            name='product_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dailywork.Products'),
        ),
    ]
