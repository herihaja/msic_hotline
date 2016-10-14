# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referral_system', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='authuser',
            name='fcm_token',
            field=models.CharField(max_length=512, null=True),
        ),
    ]
