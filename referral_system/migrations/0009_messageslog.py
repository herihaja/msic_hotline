# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('referral_system', '0008_occupation'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessagesLog',
            fields=[
                ('id_message', models.AutoField(serialize=False, primary_key=True)),
                ('date_sent', models.DateTimeField(default=datetime.datetime.now, null=True, blank=True)),
                ('status', models.CharField(max_length=250, null=True, blank=True)),
                ('content_sms', models.TextField(null=True, blank=True)),
                ('from_number', models.CharField(max_length=100, null=True, blank=True)),
                ('to_number', models.CharField(max_length=100, null=True, blank=True)),
                ('id_actor', models.IntegerField(null=True, blank=True)),
                ('id_recipient', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'messages_log',
                'managed': False,
            },
        ),
    ]
