# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referral_system', '0003_otherservices'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'managed': True},
        ),
    ]
