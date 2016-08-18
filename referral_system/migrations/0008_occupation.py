# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referral_system', '0007_auto_20160808_0841'),
    ]

    operations = [
        migrations.CreateModel(
            name='Occupation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('occupation_name', models.CharField(max_length=100, null=True, blank=True)),
            ],
            options={
                'db_table': 'occupation',
                'managed': False,
            },
        ),
    ]
