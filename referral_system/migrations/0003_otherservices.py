# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referral_system', '0002_dwprojet_dwquestionnaire_sms_smsapi_smsfac_smsfactmp_smsreg_smsregtmp'),
    ]

    operations = [
        migrations.CreateModel(
            name='OtherServices',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('other_services_name', models.CharField(max_length=256, null=True, blank=True)),
            ],
            options={
                'db_table': 'OTHER_SERVICES',
                'managed': False,
            },
        ),
    ]
