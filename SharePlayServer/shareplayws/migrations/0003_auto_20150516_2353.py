# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shareplayws', '0002_sp_address_street_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='sp_player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invite_reason', models.CharField(null=True, max_length=300)),
            ],
        ),
        migrations.AddField(
            model_name='sp_event',
            name='is_public',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='sp_event',
            name='owner',
            field=models.ForeignKey(related_name='created_by', to='shareplayws.sp_person'),
        ),
        migrations.AddField(
            model_name='sp_player',
            name='event',
            field=models.ForeignKey(to='shareplayws.sp_event'),
        ),
        migrations.AddField(
            model_name='sp_player',
            name='inviter',
            field=models.ForeignKey(related_name='invited_by', to='shareplayws.sp_person'),
        ),
        migrations.AddField(
            model_name='sp_player',
            name='player',
            field=models.ForeignKey(related_name='played_for', to='shareplayws.sp_person'),
        ),
        migrations.AddField(
            model_name='sp_event',
            name='player',
            field=models.ManyToManyField(to='shareplayws.sp_person', through='shareplayws.sp_player'),
        ),
    ]
