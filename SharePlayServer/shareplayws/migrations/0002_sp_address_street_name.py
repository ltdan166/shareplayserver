# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shareplayws', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sp_address',
            name='street_name',
            field=models.CharField(null=True, max_length=200),
        ),
    ]
