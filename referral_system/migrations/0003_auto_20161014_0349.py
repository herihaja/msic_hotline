# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referral_system', '0002_authuser_fcm_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='occupation',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occupation',
            name='id',
            field=models.AutoField(serialize=False, primary_key=True),
        ),
    ]
