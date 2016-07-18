# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referral_system', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DwProjet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_parent', models.IntegerField()),
                ('id_type_niveau', models.IntegerField()),
                ('short_code_calculated', models.CharField(max_length=40, null=True, blank=True)),
                ('code_questionnaire', models.CharField(max_length=20)),
                ('nom_table', models.CharField(max_length=25, null=True, blank=True)),
                ('type_projet', models.CharField(max_length=2)),
                ('commentaire', models.TextField(null=True, blank=True)),
                ('affiche', models.IntegerField(null=True, blank=True)),
                ('url', models.CharField(max_length=80, null=True, blank=True)),
                ('url_xform', models.CharField(max_length=80, null=True, blank=True)),
                ('credential', models.TextField(null=True, blank=True)),
                ('code_sujet', models.CharField(max_length=20, null=True, blank=True)),
                ('doublon', models.CharField(max_length=80, null=True, blank=True)),
                ('need_total', models.IntegerField(null=True, blank=True)),
                ('xls_form', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'dw_projet',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DwQuestionnaire',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_projet', models.IntegerField()),
                ('questionnaire', models.TextField()),
                ('nom_colonne', models.CharField(max_length=80)),
                ('path', models.CharField(max_length=80, null=True, blank=True)),
                ('libelle_fr', models.CharField(max_length=254)),
                ('libelle_us', models.CharField(max_length=254, null=True, blank=True)),
                ('data_type', models.CharField(max_length=40, null=True, blank=True)),
                ('date_format', models.CharField(max_length=10, null=True, blank=True)),
                ('rang', models.IntegerField(null=True, blank=True)),
                ('sel', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'dw_questionnaire',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Sms',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_niveau', models.IntegerField()),
                ('id_soumission', models.CharField(max_length=35)),
                ('status', models.CharField(max_length=10)),
                ('code_questionnaire', models.CharField(max_length=20)),
                ('date_soumission', models.DateField()),
                ('date_soumission_u', models.CharField(max_length=6)),
                ('date_modification', models.DateField()),
                ('date_modification_u', models.CharField(max_length=6)),
                ('imported', models.IntegerField()),
                ('short_code_calculated', models.IntegerField()),
                ('phone_number', models.CharField(max_length=15)),
                ('datasender_id', models.CharField(max_length=20)),
                ('datasender_name', models.CharField(max_length=254)),
            ],
            options={
                'db_table': 'sms',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SmsApi',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_niveau', models.IntegerField()),
                ('status', models.CharField(max_length=10)),
                ('code_questionnaire', models.CharField(max_length=20)),
                ('date_soumission', models.DateField()),
                ('date_soumission_u', models.CharField(max_length=6)),
                ('imported', models.IntegerField()),
                ('short_code_calculated', models.IntegerField()),
                ('phone_number', models.CharField(max_length=15)),
            ],
            options={
                'db_table': 'sms_api',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SmsFac',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('id_niveau', models.IntegerField(null=True, blank=True)),
                ('status', models.CharField(max_length=10, null=True, blank=True)),
                ('code_questionnaire', models.CharField(max_length=20, null=True, blank=True)),
                ('date_soumission', models.DateField(null=True, blank=True)),
                ('date_soumission_u', models.CharField(max_length=6, null=True, blank=True)),
                ('imported', models.IntegerField(null=True, blank=True)),
                ('short_code_calculated', models.IntegerField(null=True, blank=True)),
                ('phone_number', models.CharField(max_length=15, null=True, blank=True)),
                ('quest_2', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_3', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_4', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_5', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_6', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_7', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_8', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_9', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_10', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_11', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_12', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_13', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_14', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_15', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_16', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_17', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_18', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_19', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_20', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_21', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_22', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_23', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_24', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_25', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_26', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_27', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_28', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_29', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_30', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_31', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_32', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_33', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_34', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_35', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_36', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_37', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_38', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_39', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_40', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_41', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_42', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_43', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_44', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_45', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_46', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_47', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_48', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_49', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_1', models.CharField(max_length=250, null=True, blank=True)),
            ],
            options={
                'db_table': 'sms_fac',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SmsFacTmp',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('id_niveau', models.IntegerField(null=True, blank=True)),
                ('status', models.CharField(max_length=10, null=True, blank=True)),
                ('code_questionnaire', models.CharField(max_length=20, null=True, blank=True)),
                ('date_soumission', models.DateField(null=True, blank=True)),
                ('date_soumission_u', models.CharField(max_length=6, null=True, blank=True)),
                ('imported', models.IntegerField(null=True, blank=True)),
                ('short_code_calculated', models.IntegerField(null=True, blank=True)),
                ('phone_number', models.CharField(max_length=15, null=True, blank=True)),
                ('quest_2', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_3', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_4', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_5', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_6', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_7', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_8', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_9', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_10', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_11', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_12', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_13', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_14', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_15', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_16', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_17', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_18', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_19', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_20', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_21', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_22', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_23', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_24', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_25', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_26', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_27', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_28', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_29', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_30', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_31', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_32', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_33', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_34', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_35', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_36', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_37', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_38', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_39', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_40', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_41', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_42', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_43', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_44', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_45', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_46', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_47', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_48', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_49', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_1', models.CharField(max_length=250, null=True, blank=True)),
            ],
            options={
                'db_table': 'sms_fac_tmp',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SmsReg',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('id_niveau', models.IntegerField(null=True, blank=True)),
                ('status', models.CharField(max_length=10, null=True, blank=True)),
                ('code_questionnaire', models.CharField(max_length=20, null=True, blank=True)),
                ('date_soumission', models.DateField(null=True, blank=True)),
                ('date_soumission_u', models.CharField(max_length=6, null=True, blank=True)),
                ('imported', models.IntegerField(null=True, blank=True)),
                ('short_code_calculated', models.IntegerField(null=True, blank=True)),
                ('phone_number', models.CharField(max_length=15, null=True, blank=True)),
                ('quest_1', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_2', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_3', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_4', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_5', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_6', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_7', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_8', models.CharField(max_length=250, null=True, blank=True)),
            ],
            options={
                'db_table': 'sms_reg',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SmsRegTmp',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('id_niveau', models.IntegerField(null=True, blank=True)),
                ('status', models.CharField(max_length=10, null=True, blank=True)),
                ('code_questionnaire', models.CharField(max_length=20, null=True, blank=True)),
                ('date_soumission', models.DateField(null=True, blank=True)),
                ('date_soumission_u', models.CharField(max_length=6, null=True, blank=True)),
                ('imported', models.IntegerField(null=True, blank=True)),
                ('short_code_calculated', models.IntegerField(null=True, blank=True)),
                ('phone_number', models.CharField(max_length=15, null=True, blank=True)),
                ('quest_1', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_2', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_3', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_4', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_5', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_6', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_7', models.CharField(max_length=250, null=True, blank=True)),
                ('quest_8', models.CharField(max_length=250, null=True, blank=True)),
            ],
            options={
                'db_table': 'sms_reg_tmp',
                'managed': False,
            },
        ),
    ]
