# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rps', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='matches',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='wins',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
