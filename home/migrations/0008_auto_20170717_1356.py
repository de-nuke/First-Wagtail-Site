# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-17 13:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_bloggalleryimage'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BlogGalleryImage',
            new_name='BlogPostGalleryImage',
        ),
    ]
