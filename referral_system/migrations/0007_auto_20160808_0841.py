# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referral_system', '0006_vouchercode'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReferralOperation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('referral_id', models.CharField(max_length=20, null=True, blank=True)),
                ('actor_id', models.IntegerField(null=True, blank=True)),
                ('last_actor_id', models.IntegerField(null=True, blank=True)),
                ('referred_services', models.TextField(null=True, blank=True)),
                ('other_services', models.TextField(null=True, blank=True)),
                ('status', models.IntegerField(null=True, blank=True)),
                ('last_updated', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'db_table': 'referral_operation',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ReferredServices',
            fields=[
                ('service_name', models.CharField(max_length=250, serialize=False, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'db_table': 'referred_services',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SmsLoc',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('id_niveau', models.IntegerField()),
                ('status', models.CharField(max_length=10)),
                ('code_questionnaire', models.CharField(max_length=20)),
                ('date_soumission', models.DateField()),
                ('date_soumission_u', models.CharField(max_length=6)),
                ('imported', models.IntegerField()),
                ('short_code_calculated', models.IntegerField()),
                ('phone_number', models.CharField(max_length=15, null=True, blank=True)),
                ('quest_1', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_2', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_3', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_4', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_5', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_6', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_7', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_8', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_9', models.CharField(max_length=250, null=True, blank=True)),
            ],
            options={
                'db_table': 'sms_loc',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SmsLocTmp',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('id_niveau', models.IntegerField()),
                ('status', models.CharField(max_length=10)),
                ('code_questionnaire', models.CharField(max_length=20)),
                ('date_soumission', models.DateField()),
                ('date_soumission_u', models.CharField(max_length=6)),
                ('imported', models.IntegerField()),
                ('short_code_calculated', models.IntegerField()),
                ('phone_number', models.CharField(max_length=15, null=True, blank=True)),
                ('quest_1', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_2', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_3', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_4', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_5', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_6', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_7', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_8', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_9', models.CharField(max_length=250, null=True, blank=True)),
            ],
            options={
                'db_table': 'sms_loc_tmp',
                'managed': False,
            },
        ),
        migrations.AlterModelTable(
            name='appointment',
            table='appointment',
        ),
        migrations.AlterModelTable(
            name='client',
            table='client',
        ),
        migrations.AlterModelTable(
            name='vouchercode',
            table='voucher_code',
        ),
    ]
