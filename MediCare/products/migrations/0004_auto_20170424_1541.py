# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-04-24 15:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20170321_1807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(upload_to='/home/anushka/MediCare/media/products/images/'),
        ),
    ]
