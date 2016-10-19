from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser


class Appointment(models.Model):
    referral_id = models.CharField(primary_key=True, max_length=30)
    referral_date = models.DateField(blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    language = models.CharField(max_length=20, blank=True, null=True)
    id_client = models.IntegerField(blank=True, null=True)
    notification_client_id = models.IntegerField(blank=True, null=True)
    notification_facility_id = models.IntegerField(blank=True, null=True)
    mode = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(default=datetime.now, blank=True, null=True)
    last_updated = models.DateTimeField(default=datetime.now, blank=True, null=True)

    def save(self):
        if self.referral_id:
            self.last_updated = datetime.now()
        super(Appointment,self).save()

    class Meta:
        managed = True
        db_table = 'appointment'

class AuthUser(AbstractUser):
    facility_id = models.CharField(max_length=30,null=True)
    fcm_token = models.CharField(max_length=512,null=True)

    class Meta:
        managed = True
        db_table = 'auth_user'


class Client(models.Model):
    id_client = models.AutoField(primary_key=True)
    sex = models.CharField(max_length=10, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    occupation = models.IntegerField(blank=True, null=True)
    garment_id = models.CharField(max_length=100, blank=True, null=True)
    adr_street = models.CharField(max_length=255, blank=True, null=True)
    adr_village = models.CharField(max_length=255, blank=True, null=True)
    adr_commune = models.CharField(max_length=255, blank=True, null=True)
    adr_district = models.CharField(max_length=255, blank=True, null=True)
    adr_province = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'client'


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
        managed = True
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
        managed = True
        db_table = 'dw_questionnaire'
        
class MessagesLog(models.Model):
    id_message = models.AutoField(primary_key=True)
    date_sent = models.DateTimeField(default=datetime.now, blank=True, null=True)
    status = models.CharField(max_length=250, blank=True, null=True)
    content_sms = models.TextField(blank=True, null=True)
    from_number = models.CharField(max_length=100, blank=True, null=True)
    to_number = models.CharField(max_length=100, blank=True, null=True)
    id_actor = models.IntegerField(blank=True, null=True)
    id_recipient = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        app_label = 'referral_system'
        db_table = 'messages_log'
        
class Occupation(models.Model):
    id = models.AutoField(primary_key=True)
    occupation_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'occupation'


class ReferralOperation(models.Model):
    referral_id = models.CharField(max_length=20, blank=True, null=True)
    actor_id = models.IntegerField(blank=True, null=True)
    last_actor_id = models.IntegerField(blank=True, null=True)
    referred_services = models.TextField(blank=True, null=True)
    other_services = models.TextField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    last_updated = models.DateTimeField(default=datetime.now, blank=True, null=True)
    is_completed = models.CharField(max_length=4, blank=True, null=True)
    has_alternative = models.CharField(max_length=4, blank=True, null=True)
    provider = models.CharField(max_length=255, blank=True, null=True)
    redeem_date = models.DateField(blank=True, null=True)
    facility_id = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'referral_operation'


class ReferredServices(models.Model):
    service_name = models.CharField(primary_key=True, max_length=250)
    created = models.DateTimeField(default=datetime.now, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'referred_services'

    @classmethod
    def get_all_in_customized_order(cls):
        allServices = ReferredServices.objects.all()
        unordered_list = []
        expected = ["Pills", "Injectable", "Implant insertion", "Implant removal", "IUD Insertion", "IUD removal",
                    "Voluntary permanent method", "STI screening and treatment", "Cervical cancer screening"]
        dict_order = dict()
        for index, service in enumerate(allServices):
            if service.service_name in expected:
                dict_order.update({service.service_name: index})
            else:
                unordered_list.append(service)

        ordered = [allServices[dict_order.get(service_name)] for service_name in expected if dict_order.get(service_name)]
        ordered.extend(unordered_list)
        return ordered


    def __repr__(self):
        return self.service_name

    def __str__(self):
        return self.service_name


class Sms(models.Model):
    id_niveau = models.IntegerField(null=True)
    id_soumission = models.CharField(max_length=35, null=True)
    status = models.CharField(max_length=10, null=True)
    code_questionnaire = models.CharField(max_length=20)
    date_soumission = models.DateField(null=True)
    date_soumission_u = models.CharField(max_length=6)
    date_modification = models.DateField()
    date_modification_u = models.CharField(max_length=6, null=True)
    imported = models.IntegerField(null=True)
    short_code_calculated = models.IntegerField(null=True)
    phone_number = models.CharField(max_length=15, null=True)
    datasender_id = models.CharField(max_length=20, null=True)
    datasender_name = models.CharField(max_length=254, null=True)

    class Meta:
        managed = True
        db_table = 'sms'


class SmsApi(models.Model):
    id_niveau = models.IntegerField()
    status = models.CharField(max_length=10)
    code_questionnaire = models.CharField(max_length=20)
    date_soumission = models.DateField()
    date_soumission_u = models.CharField(max_length=6)
    imported = models.IntegerField()
    short_code_calculated = models.IntegerField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'sms_api'


class SmsFac(models.Model):
    id = models.AutoField(primary_key=True)
    id_niveau = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=10, null=True)
    code_questionnaire = models.CharField(max_length=20)
    date_soumission = models.DateField()
    date_soumission_u = models.CharField(max_length=6)
    imported = models.IntegerField(null=True)
    short_code_calculated = models.IntegerField(null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    quest_1 = models.CharField(max_length=250, blank=True, null=True)
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
    quest_18 = models.CharField(max_length=250, blank=True, null=True) #village english
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
    quest_48 = models.CharField(max_length=1000, blank=True, null=True) #working hour
    quest_49 = models.CharField(max_length=250, blank=True, null=True)
    quest_50 = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'sms_fac'

    @classmethod
    def get_all_garment_factories(cls):
        return SmsFac.objects.filter(quest_50__in=["Both (Referral System and Public Facing Platform)",
                                                   "Referral System only"], quest_21="Garment factory infirmary", ).order_by('quest_19')


class SmsFacTmp(models.Model):
    id = models.AutoField(primary_key=True)
    id_niveau = models.IntegerField(null=True)
    status = models.CharField(max_length=10, null=True)
    code_questionnaire = models.CharField(max_length=20)
    date_soumission = models.DateField()
    date_soumission_u = models.CharField(max_length=6)
    imported = models.IntegerField(null=True)
    short_code_calculated = models.IntegerField(null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    quest_1 = models.CharField(max_length=250, blank=True, null=True)
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
    quest_50 = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'sms_fac_tmp'


class SmsLoc(models.Model):
    id = models.AutoField(primary_key=True)
    id_niveau = models.IntegerField(null=True)
    status = models.CharField(max_length=10, null=True)
    code_questionnaire = models.CharField(max_length=20)
    date_soumission = models.DateField()
    date_soumission_u = models.CharField(max_length=6)
    imported = models.IntegerField(null=True)
    short_code_calculated = models.IntegerField(null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    quest_1 = models.CharField(max_length=250, blank=True, null=True)
    quest_2 = models.CharField(max_length=250, blank=True, null=True)
    quest_3 = models.CharField(max_length=250, blank=True, null=True)
    quest_4 = models.CharField(max_length=250, blank=True, null=True)
    quest_5 = models.CharField(max_length=250, blank=True, null=True)
    quest_6 = models.CharField(max_length=250, blank=True, null=True)
    quest_7 = models.CharField(max_length=250, blank=True, null=True)
    quest_8 = models.CharField(max_length=250, blank=True, null=True)
    quest_9 = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'sms_loc'


class SmsLocTmp(models.Model):
    id = models.AutoField(primary_key=True)
    id_niveau = models.IntegerField(null=True)
    status = models.CharField(max_length=10, null=True)
    code_questionnaire = models.CharField(max_length=20)
    date_soumission = models.DateField()
    date_soumission_u = models.CharField(max_length=6)
    imported = models.IntegerField(null=True)
    short_code_calculated = models.IntegerField(null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    quest_1 = models.CharField(max_length=250, blank=True, null=True)
    quest_2 = models.CharField(max_length=250, blank=True, null=True)
    quest_3 = models.CharField(max_length=250, blank=True, null=True)
    quest_4 = models.CharField(max_length=250, blank=True, null=True)
    quest_5 = models.CharField(max_length=250, blank=True, null=True)
    quest_6 = models.CharField(max_length=250, blank=True, null=True)
    quest_7 = models.CharField(max_length=250, blank=True, null=True)
    quest_8 = models.CharField(max_length=250, blank=True, null=True)
    quest_9 = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'sms_loc_tmp'


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
        managed = True
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
        managed = True
        db_table = 'sms_reg_tmp'


class VoucherCode(models.Model):
    unique_id = models.CharField(primary_key=True, max_length=10)

    class Meta:
        managed = True
        db_table = 'voucher_code'
