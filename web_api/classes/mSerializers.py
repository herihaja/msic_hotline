from django.db.models.query_utils import Q
from referral_system.models import SmsFac, Appointment, Client, AuthUser, ReferredServices, ReferralOperation, Occupation, SmsLoc

class MSerializers:



    def __init__(self):
        pass

    def select_all_facilities(self, date_last_update =None):
        facilities =[];
#        db_facilities = SmsFac.objects.all().extra(where=[" UPPER(quest_26) = 'YES' "])
        db_facilities = SmsFac.objects.all().filter(
            (Q(quest_50 = "Both (Referral System and Public Facing Platform)")|
            Q(quest_50 = "Referral System only"))|
            Q(quest_21 = "Garment factory infirmary")
        )

        for objFacility in db_facilities :
            facility = {}
            facility["id"] = objFacility.quest_20
            facility["name"] = objFacility.quest_19
            facility["name_khmer"] = objFacility.quest_12
            facility["coordinates"] = objFacility.quest_24
            facility["street"] = objFacility.quest_16
            facility["street_khmer"] = objFacility.quest_12
            facility["village"] = objFacility.quest_18
            facility["village_khmer"] = objFacility.quest_35
            facility["commune"] = objFacility.quest_13
            facility["commune_khmer"] = objFacility.quest_40
            facility["district"] = objFacility.quest_30
            facility["district_khmer"] = objFacility.quest_48
            facility["province"] = objFacility.quest_15
            facility["province_khmer"] = objFacility.quest_42
            facility["phone1"] = objFacility.quest_11
            facility["phone2"] = objFacility.quest_26
            facility["phone3"] = objFacility.quest_31
            facility["hours"] = objFacility.quest_49
            facility["services"] = objFacility.quest_49
            facility["facility_type"] = objFacility.quest_21

            facility["created"] = str(objFacility.date_soumission)
            facility["last_updated"] = str(objFacility.date_soumission)

            facilities.append(facility)
        return facilities

    def select_all_appointments(self, date_last_updated=None):
        appointments =[];
        db_appointments = Appointment.objects.all()
        for objAppointment in db_appointments :
            appointment = {}
            appointment["id"] = objAppointment.referral_id
            appointment["referral_date"] = str(objAppointment.referral_date)
            appointment["expiry_date"] = str(objAppointment.expiry_date)
            appointment["language"] = objAppointment.language
            appointment["notification_client_id"] = objAppointment.notification_client_id
            appointment["notification_facility_id"] = objAppointment.notification_facility_id
            appointment["mode"] = objAppointment.mode
            
            appointment["created"] = str(objAppointment.referral_date)
            appointment["last_updated"] = str(objAppointment.referral_date)

            client_id = objAppointment.id_client
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
                client["created"] = str(objAppointment.referral_date)
                client["last_updated"] = str(objAppointment.referral_date)
                appointment["appointment_client"] = client
                
            appointment["id_facility"] = objAppointment.id_facility
            appointment["id_garment"] = "whgf4"
            appointments.append(appointment)
        return appointments

    def select_all_services(self, date_last_updated=None):
        services =[];
        db_services = ReferredServices.objects.all()
        for objService in db_services :
            service = {}
            service["name"] = objService.service_name
            service["created"] = objService.created
            services.append(service)
        return services

    def getUser(self,username):
        auth_user = AuthUser.objects.get(username=username)
        res_user = {}
        res_user["username"] = auth_user.username
        res_user["first_name"] = auth_user.first_name
        res_user["last_name"] = auth_user.last_name
        res_user["email"] = auth_user.email
#        res_user["facility_id"] = auth_user.facility_id whgf4
        res_user["facility_id"] = "whgf4"
        res_user["group_id"] = 2
        return res_user;

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
            referOperations.append(referOperation)
        return referOperations

    def select_all_occupations(self):
        occupations = []
        db_occupations = Occupation.objects.all()
        i = 1;
        for objOccupation in db_occupations :
            occupation = {}
            occupation["occupation_id"] = i
            occupation["occupation_name"] = objOccupation.occupation_name
            occupations.append(occupation)
            i=i+1;
        return occupations

    def select_all_locations(self):
        referLocations = []
        db_locations = SmsLoc.objects.all()
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
            referLocation["created"] = str(objLocation.date_soumission)
            referLocation["last_updated"] = str(objLocation.date_soumission)
            referLocations.append(referLocation)
        return referLocations
