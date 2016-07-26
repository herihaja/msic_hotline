# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referral_system', '0005_auto_20160718_1249'),
    ]

    operations = [
        migrations.CreateModel(
            name='VoucherCode',
            fields=[
                ('unique_id', models.CharField(max_length=10, serialize=False, primary_key=True)),
            ],
            options={
                'db_table': 'VOUCHER_CODE',
                'managed': False,
            },
        ),
    ]
