# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='sp_address',
            fields=[
                ('address_id', models.AutoField(serialize=False, primary_key=True)),
                ('street_number', models.IntegerField()),
                ('city', models.CharField(max_length=200)),
                ('postal_code', models.CharField(max_length=5)),
                ('country', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='sp_event',
            fields=[
                ('event_id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('event_date', models.DateTimeField(verbose_name='Event Date')),
            ],
        ),
        migrations.CreateModel(
            name='sp_location',
            fields=[
                ('location_id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=200, null=True)),
                ('telephone', models.CharField(max_length=50, null=True)),
                ('street_number', models.IntegerField(null=True)),
                ('street_name', models.CharField(max_length=200, null=True)),
                ('city', models.CharField(max_length=200, null=True)),
                ('postal_code', models.CharField(max_length=5, null=True)),
                ('country', models.CharField(max_length=100, null=True)),
                ('longitude', models.CharField(max_length=200)),
                ('latitude', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='sp_person',
            fields=[
                ('userid', models.CharField(primary_key=True, serialize=False, max_length=10)),
                ('firstname', models.CharField(max_length=200)),
                ('lastname', models.CharField(max_length=200)),
                ('telephone', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=200)),
                ('postal_address', models.ForeignKey(to='shareplayws.sp_address', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='sp_event',
            name='location',
            field=models.ForeignKey(to='shareplayws.sp_location'),
        ),
        migrations.AddField(
            model_name='sp_event',
            name='owner',
            field=models.ForeignKey(to='shareplayws.sp_person'),
        ),
    ]
