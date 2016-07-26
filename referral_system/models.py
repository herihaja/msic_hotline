# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models
        


class Appointment(models.Model):
    referral_id = models.CharField(primary_key=True, max_length=30)
    referral_date = models.DateField(blank=True, null=True)
    language = models.CharField(max_length=20, blank=True, null=True)
    id_client = models.IntegerField(blank=True, null=True)
    id_facility = models.CharField(max_length=30, blank=True, null=True)
    notification_client_id = models.IntegerField(blank=True, null=True)
    notification_facility_id = models.IntegerField(blank=True, null=True)
    mode = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'APPOINTMENT'


class Client(models.Model):
    id_client = models.AutoField(primary_key=True)
    sex = models.CharField(max_length=1, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    occupation = models.CharField(max_length=250, blank=True, null=True)
    garment_id = models.CharField(max_length=100, blank=True, null=True)
    adr_street = models.CharField(max_length=255, blank=True, null=True)
    adr_village = models.CharField(max_length=255, blank=True, null=True)
    adr_commune = models.CharField(max_length=255, blank=True, null=True)
    adr_district = models.CharField(max_length=255, blank=True, null=True)
    adr_province = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'CLIENT'


class OtherServices(models.Model):
    other_services_name = models.CharField(max_length=256, blank=True, null=True)
    id_appointment = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'OTHER_SERVICES'


class Service(models.Model):
    id_services = models.IntegerField(primary_key=True)
    service_name = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'SERVICE'
        
class VoucherCode(models.Model):
    unique_id = models.CharField(primary_key=True, max_length=10)
    
    class Meta:
        managed = False
        db_table = 'VOUCHER_CODE'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup)
    permission = models.ForeignKey('AuthPermission')

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType')
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser)
    group = models.ForeignKey(AuthGroup)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser)
    permission = models.ForeignKey(AuthPermission)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', blank=True, null=True)
    user = models.ForeignKey(AuthUser)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class DwProjet(models.Model):
    id_parent = models.IntegerField()
    id_type_niveau = models.IntegerField()
    short_code_calculated = models.CharField(max_length=40, blank=True, null=True)
    code_questionnaire = models.CharField(max_length=20)
    nom_table = models.CharField(max_length=25, blank=True, null=True)
    type_projet = models.CharField(max_length=2)
    commentaire = models.TextField(blank=True, null=True)
    affiche = models.IntegerField(blank=True, null=True)
    url = models.CharField(max_length=80, blank=True, null=True)
    url_xform = models.CharField(max_length=80, blank=True, null=True)
    credential = models.TextField(blank=True, null=True)
    code_sujet = models.CharField(max_length=20, blank=True, null=True)
    doublon = models.CharField(max_length=80, blank=True, null=True)
    need_total = models.IntegerField(blank=True, null=True)
    xls_form = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dw_projet'


class DwQuestionnaire(models.Model):
    id_projet = models.IntegerField()
    questionnaire = models.TextField()
    nom_colonne = models.CharField(max_length=80)
    path = models.CharField(max_length=80, blank=True, null=True)
    libelle_fr = models.CharField(max_length=254)
    libelle_us = models.CharField(max_length=254, blank=True, null=True)
    data_type = models.CharField(max_length=40, blank=True, null=True)
    date_format = models.CharField(max_length=10, blank=True, null=True)
    rang = models.IntegerField(blank=True, null=True)
    sel = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dw_questionnaire'


class ReferralService(models.Model):
    id_app = models.CharField(max_length=30)
    id_service = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'referral_service'
        unique_together = (('id_app', 'id_service'),)


class Sms(models.Model):
    id_niveau = models.IntegerField()
    id_soumission = models.CharField(max_length=35)
    status = models.CharField(max_length=10)
    code_questionnaire = models.CharField(max_length=20)
    date_soumission = models.DateField()
    date_soumission_u = models.CharField(max_length=6)
    date_modification = models.DateField()
    date_modification_u = models.CharField(max_length=6)
    imported = models.IntegerField()
    short_code_calculated = models.IntegerField()
    phone_number = models.CharField(max_length=15)
    datasender_id = models.CharField(max_length=20)
    datasender_name = models.CharField(max_length=254)

    class Meta:
        managed = False
        db_table = 'sms'


class SmsApi(models.Model):
    id_niveau = models.IntegerField()
    status = models.CharField(max_length=10)
    code_questionnaire = models.CharField(max_length=20)
    date_soumission = models.DateField()
    date_soumission_u = models.CharField(max_length=6)
    imported = models.IntegerField()
    short_code_calculated = models.IntegerField()
    phone_number = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'sms_api'


class SmsFac(models.Model):
    id_niveau = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    code_questionnaire = models.CharField(max_length=20, blank=True, null=True)
    date_soumission = models.DateField(blank=True, null=True)
    date_soumission_u = models.CharField(max_length=6, blank=True, null=True)
    imported = models.IntegerField(blank=True, null=True)
    short_code_calculated = models.IntegerField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    quest_2 = models.CharField(max_length=250, blank=True, null=True)
    quest_3 = models.CharField(max_length=250, blank=True, null=True)
    quest_4 = models.CharField(max_length=250, blank=True, null=True)
    quest_5 = models.CharField(max_length=250, blank=True, null=True)
    quest_6 = models.CharField(max_length=250, blank=True, null=True)
    quest_7 = models.CharField(max_length=250, blank=True, null=True)
    quest_8 = models.CharField(max_length=250, blank=True, null=True)
    quest_9 = models.CharField(max_length=250, blank=True, null=True)
    quest_10 = models.CharField(max_length=250, blank=True, null=True)
    quest_11 = models.CharField(max_length=250, blank=True, null=True)
    quest_12 = models.CharField(max_length=250, blank=True, null=True)
    quest_13 = models.CharField(max_length=250, blank=True, null=True)
    quest_14 = models.CharField(max_length=250, blank=True, null=True)
    quest_15 = models.CharField(max_length=250, blank=True, null=True)
    quest_16 = models.CharField(max_length=250, blank=True, null=True)
    quest_17 = models.CharField(max_length=250, blank=True, null=True)
    quest_18 = models.CharField(max_length=250, blank=True, null=True)
    quest_19 = models.CharField(max_length=250, blank=True, null=True)
    quest_20 = models.CharField(max_length=250, blank=True, null=True)
    quest_21 = models.CharField(unique=True, max_length=250)
    quest_22 = models.CharField(max_length=250, blank=True, null=True)
    quest_23 = models.CharField(max_length=250, blank=True, null=True)
    quest_24 = models.CharField(max_length=250, blank=True, null=True)
    quest_25 = models.CharField(max_length=250, blank=True, null=True)
    quest_26 = models.CharField(max_length=250, blank=True, null=True)
    quest_27 = models.CharField(max_length=250, blank=True, null=True)
    quest_28 = models.CharField(max_length=250, blank=True, null=True)
    quest_29 = models.CharField(max_length=250, blank=True, null=True)
    quest_30 = models.CharField(max_length=250, blank=True, null=True)
    quest_31 = models.CharField(max_length=250, blank=True, null=True)
    quest_32 = models.CharField(max_length=250, blank=True, null=True)
    quest_33 = models.CharField(max_length=250, blank=True, null=True)
    quest_34 = models.CharField(max_length=250, blank=True, null=True)
    quest_35 = models.CharField(max_length=250, blank=True, null=True)
    quest_36 = models.CharField(max_length=250, blank=True, null=True)
    quest_37 = models.CharField(max_length=250, blank=True, null=True)
    quest_38 = models.CharField(max_length=250, blank=True, null=True)
    quest_39 = models.CharField(max_length=250, blank=True, null=True)
    quest_40 = models.CharField(max_length=250, blank=True, null=True)
    quest_41 = models.CharField(max_length=250, blank=True, null=True)
    quest_42 = models.CharField(max_length=250, blank=True, null=True)
    quest_43 = models.CharField(max_length=250, blank=True, null=True)
    quest_44 = models.CharField(max_length=250, blank=True, null=True)
    quest_45 = models.CharField(max_length=250, blank=True, null=True)
    quest_46 = models.CharField(max_length=250, blank=True, null=True)
    quest_47 = models.CharField(max_length=250, blank=True, null=True)
    quest_48 = models.CharField(max_length=250, blank=True, null=True)
    quest_49 = models.CharField(max_length=250, blank=True, null=True)
    quest_1 = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sms_fac'


class SmsFacTmp(models.Model):
    id = models.AutoField(primary_key=True)
    id_niveau = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    code_questionnaire = models.CharField(max_length=20, blank=True, null=True)
    date_soumission = models.DateField(blank=True, null=True)
    date_soumission_u = models.CharField(max_length=6, blank=True, null=True)
    imported = models.IntegerField(blank=True, null=True)
    short_code_calculated = models.IntegerField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    quest_2 = models.CharField(max_length=250, blank=True, null=True)
    quest_3 = models.CharField(max_length=250, blank=True, null=True)
    quest_4 = models.CharField(max_length=250, blank=True, null=True)
    quest_5 = models.CharField(max_length=250, blank=True, null=True)
    quest_6 = models.CharField(max_length=250, blank=True, null=True)
    quest_7 = models.CharField(max_length=250, blank=True, null=True)
    quest_8 = models.CharField(max_length=250, blank=True, null=True)
    quest_9 = models.CharField(max_length=250, blank=True, null=True)
    quest_10 = models.CharField(max_length=250, blank=True, null=True)
    quest_11 = models.CharField(max_length=250, blank=True, null=True)
    quest_12 = models.CharField(max_length=250, blank=True, null=True)
    quest_13 = models.CharField(max_length=250, blank=True, null=True)
    quest_14 = models.CharField(max_length=250, blank=True, null=True)
    quest_15 = models.CharField(max_length=250, blank=True, null=True)
    quest_16 = models.CharField(max_length=250, blank=True, null=True)
    quest_17 = models.CharField(max_length=250, blank=True, null=True)
    quest_18 = models.CharField(max_length=250, blank=True, null=True)
    quest_19 = models.CharField(max_length=250, blank=True, null=True)
    quest_20 = models.CharField(max_length=250, blank=True, null=True)
    quest_21 = models.CharField(max_length=250, blank=True, null=True)
    quest_22 = models.CharField(max_length=250, blank=True, null=True)
    quest_23 = models.CharField(max_length=250, blank=True, null=True)
    quest_24 = models.CharField(max_length=250, blank=True, null=True)
    quest_25 = models.CharField(max_length=250, blank=True, null=True)
    quest_26 = models.CharField(max_length=250, blank=True, null=True)
    quest_27 = models.CharField(max_length=250, blank=True, null=True)
    quest_28 = models.CharField(max_length=250, blank=True, null=True)
    quest_29 = models.CharField(max_length=250, blank=True, null=True)
    quest_30 = models.CharField(max_length=250, blank=True, null=True)
    quest_31 = models.CharField(max_length=250, blank=True, null=True)
    quest_32 = models.CharField(max_length=250, blank=True, null=True)
    quest_33 = models.CharField(max_length=250, blank=True, null=True)
    quest_34 = models.CharField(max_length=250, blank=True, null=True)
    quest_35 = models.CharField(max_length=250, blank=True, null=True)
    quest_36 = models.CharField(max_length=250, blank=True, null=True)
    quest_37 = models.CharField(max_length=250, blank=True, null=True)
    quest_38 = models.CharField(max_length=250, blank=True, null=True)
    quest_39 = models.CharField(max_length=250, blank=True, null=True)
    quest_40 = models.CharField(max_length=250, blank=True, null=True)
    quest_41 = models.CharField(max_length=250, blank=True, null=True)
    quest_42 = models.CharField(max_length=250, blank=True, null=True)
    quest_43 = models.CharField(max_length=250, blank=True, null=True)
    quest_44 = models.CharField(max_length=250, blank=True, null=True)
    quest_45 = models.CharField(max_length=250, blank=True, null=True)
    quest_46 = models.CharField(max_length=250, blank=True, null=True)
    quest_47 = models.CharField(max_length=250, blank=True, null=True)
    quest_48 = models.CharField(max_length=250, blank=True, null=True)
    quest_49 = models.CharField(max_length=250, blank=True, null=True)
    quest_1 = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sms_fac_tmp'


class SmsReg(models.Model):
    id = models.AutoField(primary_key=True)
    id_niveau = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    code_questionnaire = models.CharField(max_length=20, blank=True, null=True)
    date_soumission = models.DateField(blank=True, null=True)
    date_soumission_u = models.CharField(max_length=6, blank=True, null=True)
    imported = models.IntegerField(blank=True, null=True)
    short_code_calculated = models.IntegerField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    quest_1 = models.CharField(max_length=250, blank=True, null=True)
    quest_2 = models.CharField(max_length=250, blank=True, null=True)
    quest_3 = models.CharField(max_length=250, blank=True, null=True)
    quest_4 = models.CharField(max_length=250, blank=True, null=True)
    quest_5 = models.CharField(max_length=250, blank=True, null=True)
    quest_6 = models.CharField(max_length=250, blank=True, null=True)
    quest_7 = models.CharField(max_length=250, blank=True, null=True)
    quest_8 = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sms_reg'


class SmsRegTmp(models.Model):
    id = models.AutoField(primary_key=True)
    id_niveau = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    code_questionnaire = models.CharField(max_length=20, blank=True, null=True)
    date_soumission = models.DateField(blank=True, null=True)
    date_soumission_u = models.CharField(max_length=6, blank=True, null=True)
    imported = models.IntegerField(blank=True, null=True)
    short_code_calculated = models.IntegerField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    quest_1 = models.CharField(max_length=250, blank=True, null=True)
    quest_2 = models.CharField(max_length=250, blank=True, null=True)
    quest_3 = models.CharField(max_length=250, blank=True, null=True)
    quest_4 = models.CharField(max_length=250, blank=True, null=True)
    quest_5 = models.CharField(max_length=250, blank=True, null=True)
    quest_6 = models.CharField(max_length=250, blank=True, null=True)
    quest_7 = models.CharField(max_length=250, blank=True, null=True)
    quest_8 = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sms_reg_tmp'
