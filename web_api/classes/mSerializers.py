from referral_system.models import SmsFac, Appointment, Client, AuthUser

class MSerializers:



    def __init__(self):
        pass

    def select_all_facilities(self, date_last_update =None):
        facilities =[];
        db_facilities = SmsFac.objects.all().extra(where=[" UPPER(quest_26) = 'YES' "])
        for objFacility in db_facilities :
            facility = {}
            facility["id"] = objFacility.quest_20
            facility["name"] = objFacility.quest_29
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
            facility["phone1"] = objFacility.quest_12
            facility["phone2"] = objFacility.quest_26
            facility["phone3"] = objFacility.quest_31
            facility["hours"] = objFacility.quest_49
            facility["fp_services"] = objFacility.quest_27
            facility["abortion_services1"] = objFacility.quest_26
            facility["abortion_services2"] = objFacility.quest_37

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
        db_services = Service.objects.all()
        for objService in db_services :
            service = {}
            service["id"] = objService.id_services
            service["name"] = objService.service_name
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
