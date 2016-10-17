from collections import Counter
import datetime
from django.db.models.query_utils import Q
from msic_hotline import settings
from referral_system.models import SmsFac, Appointment, \
    Client, AuthUser, ReferredServices, ReferralOperation, \
    Occupation, SmsLoc
from web_api.classes.StaticTools import StaticTools
from pyfcm import FCMNotification

class MSerializers:



    def __init__(self):
        pass

    def select_all_facilities(self, date_last_update=None):
        date_last_update = self.my_format_date(date_last_update)
        facilities =[];
#        db_facilities = SmsFac.objects.all().extra(where=[" UPPER(quest_26) = 'YES' "])
        db_facilities = SmsFac.objects.all().filter(
            (Q(quest_50 = "Both (Referral System and Public Facing Platform)")|
            Q(quest_50 = "Referral System only"))|
            Q(quest_21 = "Garment factory infirmary"),
            date_soumission__gt=date_last_update
        )\
        .distinct('quest_20')\
        .order_by('quest_20','-date_soumission')

        for objFacility in db_facilities :
            facility = {}
            facility["id"] = objFacility.quest_20
            facility["name"] = objFacility.quest_19
            facility["name_khmer"] = objFacility.quest_12
            facility["coordinates"] = objFacility.quest_24
            facility["street"] = objFacility.quest_16
            facility["street_khmer"] = objFacility.quest_34
            facility["village"] = objFacility.quest_18
            facility["village_khmer"] = objFacility.quest_34
            facility["commune"] = objFacility.quest_13
            facility["commune_khmer"] = objFacility.quest_39
            facility["district"] = objFacility.quest_30
            facility["district_khmer"] = objFacility.quest_41
            facility["province"] = objFacility.quest_15
            facility["province_khmer"] = objFacility.quest_42
            facility["phone1"] = objFacility.quest_11
            facility["phone2"] = objFacility.quest_26
            facility["phone3"] = objFacility.quest_31
            facility["hours"] = objFacility.quest_48
            facility["services"] = objFacility.quest_49
            facility["facility_type"] = objFacility.quest_21

            facility["created"] = objFacility.date_soumission.strftime('%Y-%m-%d %H:%M:%S.%f')
            facility["last_updated"] = objFacility.date_soumission.strftime('%Y-%m-%d %H:%M:%S.%f')

            facilities.append(facility)
        return facilities

    def select_all_appointments(self, user=None, date_last_updated=None):
        appointments =[];
        if(user["group_id"] == 2):
#            db_appointments = Appointment.objects.all().filter(date_soumission__gt=date_last_updated)
            sql = '''
            select
            ap.*
            from referral_operation op
            inner join appointment ap on ap.referral_id = op.referral_id
            where 1=1
            and (op.actor_id = '%s')
            and op.status = 1
            and ap.last_updated > '%s';
            '''%(user["user_id"],date_last_updated)
            db_appointments = StaticTools.run_sql(sql)
        else:
            sql = '''
            select
            ap.*
            from referral_operation op
            inner join appointment ap on ap.referral_id = op.referral_id
            where 1=1
            and (op.facility_id = '%s' or op.actor_id = '%s')
            and op.status = 1
            and ap.last_updated > '%s';
            '''%(user["facility_id"],user["user_id"],date_last_updated)
            db_appointments = StaticTools.run_sql(sql)
        for objAppointment in db_appointments :
            appointment = {}
            appointment["id"] = objAppointment['referral_id']
            appointment["referral_date"] = objAppointment["referral_date"].strftime('%Y-%m-%d')
            appointment["expiry_date"] = objAppointment["expiry_date"].strftime('%Y-%m-%d')
            appointment["language"] = objAppointment["language"]
            appointment["notification_client_id"] = objAppointment["notification_client_id"]
            appointment["notification_facility_id"] = objAppointment["notification_facility_id"]
            appointment["mode"] = objAppointment["mode"]
            
            appointment["created"] = objAppointment["created"].strftime('%Y-%m-%d %H:%M:%S.%f')
            appointment["last_updated"] = objAppointment["last_updated"].strftime('%Y-%m-%d %H:%M:%S.%f')

            client_id = objAppointment["id_client"]
            appointment["appointment_client_id"] = client_id
            db_client = Client.objects.get(pk=client_id)
            if db_client is not None:
                client = {}
                client["id"] = db_client.id_client
                client["sex"] = db_client.sex
                client["age"] = db_client.age
                client["phone"] = db_client.phone
                client["occupation"] = db_client.occupation
                client["garment_id"] = db_client.garment_id
                client["adr_street"] = db_client.adr_street
                client["adr_village"] = db_client.adr_village
                client["adr_commune"] = db_client.adr_commune
                client["adr_district"] = db_client.adr_district
                client["adr_province"] = db_client.adr_province
    #            client["created"] = db_client.created
    #            client["last_updated"] = db_client.last_updated
                client["created"] = objAppointment["last_updated"].strftime('%Y-%m-%d %H:%M:%S.%f')
                client["last_updated"] = objAppointment["last_updated"].strftime('%Y-%m-%d %H:%M:%S.%f')
                appointment["appointment_client"] = client
                
#            appointment["id_facility"] = objAppointment["id_facility
#            appointment["id_garment"] = "whgf4"
            appointments.append(appointment)
        return appointments

    def select_all_services(self, nb_service=None):
        services =[];
        db_services = ReferredServices.objects.all()
        if len(db_services) > int(nb_service) :
            for objService in db_services :
                if objService is not None :
                    service = {}
                    service["name"] = objService.service_name
                    service["created"] = objService.created.strftime('%Y-%m-%d %H:%M:%S.%f')
                    services.append(service)
        return services

    def getUser(self,username):
        auth_user = AuthUser.objects.get(username=username)
        res_user = {}
        res_user["user_id"] = auth_user.id
        res_user["username"] = auth_user.username
        res_user["first_name"] = auth_user.first_name
        res_user["last_name"] = auth_user.last_name
        res_user["email"] = auth_user.email
        res_user["token"] = auth_user.fcm_token
        res_user["facility_id"] = auth_user.facility_id #whgf4
#        res_user["facility_id"] = "whgf4"
        group = auth_user.groups.all()[0]#AuthUserGroups.objects.get(user=auth_user)
#        res_user["group_id"] = 2
        res_user["group_id"] = group.id
#        res_user["group_name"] = "Garment Factory"
        res_user["group_name"] = group.name
        return res_user

    def getUserById(self,user_id):
        auth_user = AuthUser.objects.get(pk=user_id)
        res_user = {}
        res_user["user_id"] = auth_user.id
        res_user["username"] = auth_user.username
        res_user["first_name"] = auth_user.first_name
        res_user["last_name"] = auth_user.last_name
        res_user["email"] = auth_user.email
        res_user["token"] = auth_user.fcm_token
        res_user["facility_id"] = auth_user.facility_id #whgf4
#        res_user["facility_id"] = "whgf4"
        group = auth_user.groups.all()[0]#AuthUserGroups.objects.get(user=auth_user)
#        res_user["group_id"] = 2
        res_user["group_id"] = group.id
#        res_user["group_name"] = "Garment Factory"
        res_user["group_name"] = group.name
        return res_user

    def select_all_operation(self):
        referOperations=[];
        db_operations = ReferralOperation.objects.all()
        for objOperation in db_operations :
            referOperation = {}
            referOperation["referral_id"] = objOperation.referral_id
            referOperation["actor_id"] = objOperation.actor_id
            referOperation["referred_services"] = objOperation.referred_services
            referOperation["other_services"] = objOperation.other_services
            referOperation["status"] = objOperation.status
            referOperation["last_updated"] = objOperation.last_updated
            referOperation["is_completed"] = objOperation.is_completed
            referOperation["has_alternative"] = objOperation.has_alternative
            referOperation["provider"] = objOperation.provider
            referOperation["redeem_date"] = objOperation.redeem_date
            referOperations.append(referOperation)
        return referOperations

    def update_operations(self, user=None, date_last_updated=None):
        referOperations = []
        listOperations = []
        if(user["group_id"] == 2):
            sql = '''
            SELECT op.*
            ,u.username as u_user_name
            ,u.first_name as u_first_name
            ,u.last_name as u_last_name
            ,f.quest_20 as f_id
            ,gr.id as group_id
            ,gr.name as group_name
            from referral_operation as op
            INNER JOIN auth_user as u on u.id = op.actor_id
            LEFT JOIN sms_fac as f on f.quest_20 = u.facility_id
            INNER JOIN auth_user_groups ug on ug.authuser_id = u.id
            INNER JOIN auth_group gr on gr.id = ug.group_id
            WHERE 1=1
            and (actor_id = %s or last_actor_id = %s)
            and op.last_updated > '%s'
            ORDER BY op.last_updated
            '''%(user["user_id"],user["user_id"],date_last_updated)
            listOperations = StaticTools.run_sql(sql)
        else:
            sql = '''
            SELECT op.*
            ,u.username as u_user_name
            ,u.first_name as u_first_name
            ,u.last_name as u_last_name
            ,f.quest_20 as f_id
            ,gr.id as group_id
            ,gr.name as group_name
            from referral_operation as op
            INNER JOIN auth_user as u on u.id = op.actor_id
            LEFT JOIN sms_fac as f on f.quest_20 = u.facility_id
            INNER JOIN auth_user_groups ug on ug.authuser_id = u.id
            INNER JOIN auth_group gr on gr.id = ug.group_id
            WHERE 1=1
            and (op.actor_id = %s or op.facility_id = '%s')
            and op.last_updated > '%s'
            ORDER BY op.last_updated
            '''%(user["user_id"],user["facility_id"],date_last_updated)
            listOperations = StaticTools.run_sql(sql)

        for objOperation in listOperations :
            referOperation = {}
            referOperation["op_id"] = objOperation["id"]
            referOperation["op_referral_id"] = objOperation["referral_id"]
            referOperation["op_actor_id"] = objOperation["actor_id"]
            referOperation["op_actor_username"] = objOperation["u_user_name"]
            referOperation["op_actor_last_name"] = objOperation["u_last_name"]
            referOperation["op_actor_first_name"] = objOperation["u_first_name"]
            referOperation["op_actor_facility_id"] = objOperation["f_id"]
            referOperation["op_actor_group_id"] = objOperation["group_id"]
            referOperation["op_actor_group_name"] = objOperation["group_name"]
            referOperation["op_referred_services"] = objOperation["referred_services"]
            referOperation["op_other_services"] = objOperation["other_services"]
            referOperation["op_status"] = objOperation["status"]
            if(objOperation["last_updated"] is not None):
                referOperation["op_last_updated"] = objOperation["last_updated"].strftime('%Y-%m-%d %H:%M:%S.%f')
            else:
                referOperation["op_last_updated"] = ""

            referOperation["op_is_completed"] = objOperation["is_completed"]
            referOperation["op_has_alternative"] = objOperation["has_alternative"]
            referOperation["op_provider"] = objOperation["provider"]
            if(objOperation["redeem_date"] is not None):
                referOperation["op_redeem_date"] = objOperation["redeem_date"].strftime('%Y-%m-%d')
            else:
                referOperation["op_redeem_date"] = ""
            referOperation["op_facility_id"] = objOperation["facility_id"]
            referOperations.append(referOperation)
        return referOperations

    def select_all_occupations(self,nb_occupation):
        occupations = []
        db_occupations = Occupation.objects.all()
        if(len(db_occupations) > int(nb_occupation)):
            i = 1;
            for objOccupation in db_occupations :
                occupation = {}
                occupation["occupation_id"] = objOccupation.id
                occupation["occupation_name"] = objOccupation.occupation_name
                occupations.append(occupation)
                i=i+1;
        return occupations

    def select_all_locations(self, date_last_updated=None):
        date_last_updated = self.my_format_date(date_last_updated)
        referLocations = []
        db_locations = SmsLoc.objects.all()\
            .filter(date_soumission__gt=date_last_updated)\
            .distinct('quest_5')\
            .order_by('quest_5','-date_soumission')
        for objLocation in db_locations :
            referLocation = {}
            referLocation["id_location"] = objLocation.quest_5
            referLocation["village"] = objLocation.quest_3
            referLocation["village_khmer"] = objLocation.quest_7
            referLocation["commune"] = objLocation.quest_9
            referLocation["commune_khmer"] = objLocation.quest_2
            referLocation["district"] = objLocation.quest_4
            referLocation["district_khmer"] = objLocation.quest_8
            referLocation["province"] = objLocation.quest_6
            referLocation["province_khmer"] = objLocation.quest_1
            referLocation["created"] = objLocation.date_soumission.strftime('%Y-%m-%d %H:%M:%S.%f')
            referLocation["last_updated"] = objLocation.date_soumission.strftime('%Y-%m-%d %H:%M:%S.%f')
            referLocations.append(referLocation)
        return referLocations

    def update_garment_report(self,user=None):
        today = datetime.date.today().strftime("%Y-%m-%d")
        report_garment = {}
        sql = '''
            SELECT
            (
                SELECT count(*)
                FROM referral_operation pa
                WHERE pa.actor_id = '%s' and pa.status=1) as grep_all_referred
            ,(SELECT
                count(*)
                FROM
                (SELECT pa.referral_id, count(referral_id)
                FROM referral_operation pa
                WHERE 1=1
                and (pa.actor_id = '%s' or pa.last_actor_id = '%s')
                GROUP BY referral_id HAVING count(referral_id) < 2) as op
                INNER JOIN appointment ap on ap.referral_id = op.referral_id
                WHERE 1=1
                and NOT(ap.expiry_date < '%s')
            ) as grep_new
            ,(
                SELECT
                count(*)
                FROM
                (SELECT pa.referral_id, count(referral_id)
                FROM referral_operation pa
                WHERE 1=1
                and (pa.actor_id = '%s' or pa.last_actor_id = '%s')
                GROUP BY referral_id HAVING count(referral_id) < 2) as op
                INNER JOIN appointment ap on ap.referral_id = op.referral_id
                WHERE 1=1
                and (ap.expiry_date < '%s')
            ) as grep_expired
            ,(
                SELECT count(*)
                FROM referral_operation rp
                WHERE rp.last_actor_id = '%s' and rp.status=3
                and (rp.referred_services IS NULL or trim(rp.referred_services) = '')
            ) as grep_give_up
            ,(
                SELECT count(*)
                FROM referral_operation rp
                WHERE rp.last_actor_id = '%s' and rp.status=2
                and NOT(rp.referred_services IS NULL or trim(rp.referred_services) = '')
            ) as grep_redeemed
            ,(
                SELECT count(*)
                FROM referral_operation rp
                WHERE rp.last_actor_id = '%s' and rp.status=4
                and NOT(rp.referred_services IS NULL or trim(rp.referred_services) = '')
                and (
                SELECT count(*) FROM referral_operation rop
                WHERE rop.referral_id = rp.referral_id
                AND rop.status = 2
                )=0
            ) as grep_re_referred
            ,(SELECT array_to_string(array(SELECT rp.referred_services
            FROM referral_operation rp
            WHERE rp.actor_id = '%s' and rp.status=1
            ),';')) as grep_all_services
            , op.last_updated
            FROM referral_operation op
            ORDER BY op.last_updated DESC
            LIMIT 1;
            '''%(user["user_id"],user["user_id"],user["user_id"]
            ,today,user["user_id"],user["user_id"]
            ,today,user["user_id"],user["user_id"]
            ,user["user_id"],user["user_id"])
        print sql
        list_report = StaticTools.run_sql(sql)
        if len(list_report) == 0:
            return report_garment
        res_report = list_report[0]
        report_garment["grep_all_referred"] = res_report["grep_all_referred"]
        report_garment["grep_new"] = res_report["grep_new"]
        report_garment["grep_expired"] = res_report["grep_expired"]
        report_garment["grep_give_up"] = res_report["grep_give_up"]
        report_garment["grep_redeemed"] = res_report["grep_redeemed"]
        report_garment["grep_re_referred"] = res_report["grep_re_referred"]
        all_services = res_report["grep_all_services"]
        list_services = all_services.split(';')
        report_garment["grep_all_services"] = len(list_services)
        report_garment["grep_services_dispatched"] = Counter(list_services)
        report_garment["grep_last_updated"] = res_report["last_updated"]
        return report_garment

    def update_facility_report(self,user=None):
        today = datetime.date.today().strftime("%Y-%m-%d")
        report_garment = {}
        sql = '''
            SELECT
            (
                SELECT count(*)
                FROM referral_operation pa
                WHERE pa.facility_id = '%s' and pa.status=1) as grep_all_referred
            ,(SELECT
                count(*)
                FROM
                (SELECT pa.referral_id, count(referral_id)
                FROM referral_operation pa
                WHERE 1=1
                and (pa.facility_id = '%s' or pa.actor_id = '%s')
                GROUP BY referral_id HAVING count(referral_id) < 2) as op
                INNER JOIN appointment ap on ap.referral_id = op.referral_id
                WHERE 1=1
                and NOT(ap.expiry_date < '%s')
            ) as grep_new
            ,(
                SELECT
                count(*)
                FROM
                (SELECT pa.referral_id, count(referral_id)
                FROM referral_operation pa
                WHERE 1=1
                and (pa.facility_id = '%s' or pa.actor_id = '%s')
                GROUP BY referral_id HAVING count(referral_id) < 2) as op
                INNER JOIN appointment ap on ap.referral_id = op.referral_id
                WHERE 1=1
                and (ap.expiry_date < '%s')
            ) as grep_expired
            ,(
                SELECT count(*)
                FROM referral_operation rp
                WHERE rp.actor_id = '%s' and rp.status=3
                and (rp.referred_services IS NULL or trim(rp.referred_services) = '')
            ) as grep_give_up
            ,(
                SELECT count(*)
                FROM referral_operation rp
                WHERE rp.actor_id = '%s' and rp.status=2
                and NOT(rp.referred_services IS NULL or trim(rp.referred_services) = '')
            ) as grep_redeemed
            ,(
                SELECT count(*)
                FROM referral_operation rp
                WHERE rp.actor_id = '%s' and rp.status=4
                and NOT(rp.referred_services IS NULL or trim(rp.referred_services) = '')
                and (
                SELECT count(*) FROM referral_operation rop
                WHERE rop.referral_id = rp.referral_id
                AND rop.status = 2
                )=0
            ) as grep_re_referred
            ,(SELECT array_to_string(array(SELECT rp.referred_services
            FROM referral_operation rp
            WHERE rp.facility_id = '%s' and rp.status=1
            ),';')) as grep_all_services
            , op.last_updated
            FROM referral_operation op
            ORDER BY op.last_updated DESC
            LIMIT 1;
            '''%(user["facility_id"],user["facility_id"],user["user_id"]
                ,today,user["facility_id"],user["user_id"]
                ,today,user["user_id"],user["user_id"]
                ,user["user_id"],user["facility_id"])
        list_report = StaticTools.run_sql(sql)
        if len(list_report) == 0:
            return report_garment
        res_report = list_report[0]
        report_garment["grep_all_referred"] = res_report["grep_all_referred"]
        report_garment["grep_new"] = res_report["grep_new"]
        report_garment["grep_expired"] = res_report["grep_expired"]
        report_garment["grep_give_up"] = res_report["grep_give_up"]
        report_garment["grep_redeemed"] = res_report["grep_redeemed"]
        report_garment["grep_re_referred"] = res_report["grep_re_referred"]
        all_services = res_report["grep_all_services"]
        list_services = all_services.split(';')
        report_garment["grep_all_services"] = len(list_services)
        report_garment["grep_services_dispatched"] = Counter(list_services)
        report_garment["grep_last_updated"] = res_report["last_updated"]
        return report_garment

    def getOperation (self,id):
        sql = '''
            SELECT op.*
            ,u.username as u_user_name
            ,u.first_name as u_first_name
            ,u.last_name as u_last_name
            ,f.quest_20 as f_id
            ,gr.id as group_id
            ,gr.name as group_name
            from referral_operation as op
            INNER JOIN auth_user as u on u.id = op.actor_id
            LEFT JOIN sms_fac as f on f.quest_20 = u.facility_id
            INNER JOIN auth_user_groups ug on ug.authuser_id = u.id
            INNER JOIN auth_group gr on gr.id = ug.group_id
            WHERE 1=1
            and op.id = %s
            ORDER BY op.last_updated
            '''%(id)
        listOperations = StaticTools.run_sql(sql)
        objOperation = listOperations[0]
        referOperation = {}
        referOperation["op_id"] = objOperation["id"]
        referOperation["op_referral_id"] = objOperation["referral_id"]
        referOperation["op_actor_id"] = objOperation["actor_id"]
        referOperation["op_actor_username"] = objOperation["u_user_name"]
        referOperation["op_actor_last_name"] = objOperation["u_last_name"]
        referOperation["op_actor_first_name"] = objOperation["u_first_name"]
        referOperation["op_actor_facility_id"] = objOperation["f_id"]
        referOperation["op_actor_group_id"] = objOperation["group_id"]
        referOperation["op_actor_group_name"] = objOperation["group_name"]
        referOperation["op_referred_services"] = objOperation["referred_services"]
        referOperation["op_other_services"] = objOperation["other_services"]
        referOperation["op_status"] = objOperation["status"]
        if(objOperation["last_updated"] is not None):
            referOperation["op_last_updated"] = objOperation["last_updated"].strftime('%Y-%m-%d %H:%M:%S.%f')
        else:
            referOperation["op_last_updated"] = ""

        referOperation["op_is_completed"] = objOperation["is_completed"]
        referOperation["op_has_alternative"] = objOperation["has_alternative"]
        referOperation["op_provider"] = objOperation["provider"]
        if(objOperation["redeem_date"] is not None):
            referOperation["op_redeem_date"] = objOperation["redeem_date"].strftime('%Y-%m-%d')
        else:
            referOperation["op_redeem_date"] = ""
        referOperation["op_facility_id"] = objOperation["facility_id"]
        return referOperation;

    def getAppointment(self, appointment_id, operation_id):
        sql = '''
        select
        ap.*
        from appointment ap
        where 1=1
        and ap.referral_id = '%s';
        '''%(appointment_id)
        db_appointments = StaticTools.run_sql(sql)
        objAppointment = db_appointments[0]
        appointment = {}
        appointment["id"] = objAppointment['referral_id']
        appointment["referral_date"] = objAppointment["referral_date"].strftime('%Y-%m-%d')
        appointment["expiry_date"] = objAppointment["expiry_date"].strftime('%Y-%m-%d')
        appointment["language"] = objAppointment["language"]
        appointment["notification_client_id"] = objAppointment["notification_client_id"]
        appointment["notification_facility_id"] = objAppointment["notification_facility_id"]
        appointment["mode"] = objAppointment["mode"]

        appointment["created"] = objAppointment["created"].strftime('%Y-%m-%d %H:%M:%S.%f')
        appointment["last_updated"] = objAppointment["last_updated"].strftime('%Y-%m-%d %H:%M:%S.%f')

        client_id = objAppointment["id_client"]
        appointment["appointment_client_id"] = client_id
        db_client = Client.objects.get(pk=client_id)
        if db_client is not None:
            client = {}
            client["id"] = db_client.id_client
            client["sex"] = db_client.sex
            client["age"] = db_client.age
            client["phone"] = db_client.phone
            client["occupation"] = db_client.occupation
            client["garment_id"] = db_client.garment_id
            client["adr_street"] = db_client.adr_street
            client["adr_village"] = db_client.adr_village
            client["adr_commune"] = db_client.adr_commune
            client["adr_district"] = db_client.adr_district
            client["adr_province"] = db_client.adr_province
#            client["created"] = db_client.created
#            client["last_updated"] = db_client.last_updated
            client["created"] = objAppointment["last_updated"].strftime('%Y-%m-%d %H:%M:%S.%f')
            client["last_updated"] = objAppointment["last_updated"].strftime('%Y-%m-%d %H:%M:%S.%f')
            appointment["appointment_client"] = client
        appointment["operations"] = self.getOperation (operation_id)
        return appointment


#    def my_format_date(self, date_str="", format="%Y-%m-%d %H:%M:%S"):frep_all_referred
#        from datetime import datetime
#        if not date_str:
#            return datetime.today().date()
#        return datetime.strptime(date_str, format).date().strftime('%Y-%m-%d')
    def my_format_date(self, date_str="", format="%Y-%m-%d %H:%M:%S"):
        dates = date_str.split()
        return dates[0]


