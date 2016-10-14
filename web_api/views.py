from datetime import datetime
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login
from msic_hotline import settings
from referral_system.classes.Referral import Referral
import json
from referral_system.classes.AjaxFunction import AjaxFunction
from referral_system.classes.Reports import Reports
from referral_system.models import SmsFac, Client, Appointment, ReferralOperation, AuthUser
from django.core import serializers
from referral_system.classes.ReferralFunctions import ReferralFunctions
from pyfcm import FCMNotification


# Create your views here.
from web_api.classes.mSerializers import MSerializers

def getFacilities(request):
    mSerializer = MSerializers()
    facilities = mSerializer.select_all_facilities()
    appointments = mSerializer.select_all_appointments()
    services = mSerializer.select_all_services()
#    referOperations = mSerializer.select_all_operation()
    referOperations = mSerializer.update_operations()
    occupations = mSerializer.select_all_occupations()
    referLocations = mSerializer.select_all_locations()
    garment_report = mSerializer.update_garment_report()
    garment_facility = mSerializer.update_facility_report()
    return HttpResponse(
        content_type='application/json',
        content=json.dumps({
                'success': 1,
                'error_msg': "Data Pull SUCCESSFUL",
                "facilities": facilities,
                "appointments": appointments,
                "services":services,
                "operations":referOperations,
                "occupations":occupations,
                "locations":referLocations,
                "garment_report":garment_report,
                "facility_report":garment_facility
        },default=_json_serial))

def getAllUpdate(request):
    user_id = request.POST['user_id']
    user_name = request.POST['user_name']
    facility_last_date = request.POST['facility_last_date']
    appointment_last_date = request.POST['appointment_last_date']
    location_last_date = request.POST['location_last_date']
    referral_status_last_date = request.POST['referral_status_last_date']
    nb_service = request.POST['nb_service']
    nb_occupation = request.POST['nb_occupation']

    mSerializer = MSerializers()
    user = mSerializer.getUser(user_name)
    facilities = mSerializer.select_all_facilities(facility_last_date)
    appointments = mSerializer.select_all_appointments(user,appointment_last_date)
    services = mSerializer.select_all_services(nb_service)
#    referOperations = mSerializer.select_all_operation()
    referOperations = mSerializer.update_operations(user,referral_status_last_date)
    occupations = mSerializer.select_all_occupations(nb_occupation)
    referLocations = mSerializer.select_all_locations(location_last_date)

    if(user["group_id"] == 2):
        garment_report = mSerializer.update_garment_report(user)
        return HttpResponse(
        content_type='application/json',
        content=json.dumps({
                'success': 1,
                'error_msg': "Data Pull SUCCESSFUL",
                "facilities": facilities,
                "appointments": appointments,
                "referred_services":services,
                "operations":referOperations,
                "occupations":occupations,
                "locations":referLocations,
                "refer_report":garment_report
        },default=_json_serial))
    else:
        facility_report = mSerializer.update_facility_report(user)
        return HttpResponse(
        content_type='application/json',
        content=json.dumps({
                'success': 1,
                'error_msg': "Data Pull SUCCESSFUL",
                "facilities": facilities,
                "appointments": appointments,
                "referred_services":services,
                "operations":referOperations,
                "occupations":occupations,
                "locations":referLocations,
                "refer_report":facility_report
        },default=_json_serial))




    
def updateGarmentReport(request):
    mSerializer = MSerializers()
    garment_report = mSerializer.update_garment_report()
    return HttpResponse(
        content_type='application/json',
        content=json.dumps({
                'success': 1,
                'error_msg': "Data Pull SUCCESSFUL",
                "garment_report":garment_report,
        },default=_json_serial))

def auth(request):
    username = request.POST['login']
    password = request.POST['password']
    token = request.POST['token']
#    user = authenticate(username=username, password=password)
    user = None
    try:
        user = authenticate(username=username, password=password)
    except ObjectDoesNotExist:
        user = None

    if user is not None:
        if user.is_active:
            login(request, user)
#            update FCM token
            user.fcm_token = token
            user.save()

            mSerializer = MSerializers()
            user = mSerializer.getUser(username)

            return HttpResponse(
                content_type='application/json',
                content=json.dumps({
                        'success': 1,
                        'error_msg': "SUCCESSFUL",
                        "error_msg": "You're Logged Successfully",
                        "user": user
                },default=_json_serial))
        else:
            # Return a 'disabled account' error message
#            return redirect(loginPage, error="inactive")
            return HttpResponse(
                content_type='application/json',
                content=json.dumps({
                        'success': -1,
                        'error_msg': "ERROR_INACTIVE",
                },default=_json_serial))

    else:
        # Return an 'invalid login' error message.
#        return redirect(loginPage, error="wrong")
        return HttpResponse(
            content_type='application/json',
            content=json.dumps({
                    'success': -2,
                    'error_msg': "ERROR_WRONG",
            },default=_json_serial))

def saveReferral(request):
    if request.method == 'POST':
        #here function
        mode = int(request.POST['mode'])
        client_sex = request.POST['sex']
        client_phone = request.POST['phone']
        client_age = request.POST['age']
        client_occupation = request.POST['occupation']
        id_selected_gf = request.POST['selected_gf']
        client_adr_street = request.POST['adr_street']
        client_adr_village = request.POST['adr_village']
        client_adr_commune = request.POST['adr_commune']
        client_adr_district = request.POST['adr_district']
        client_adr_province = request.POST['adr_province']
        services = request.POST['services']
        id_selected_facility = request.POST['id_selected_facility']
        referral_date = request.POST['referral_date']
        expiry_date = request.POST['expiry_date']
        language_sms = request.POST['language_sms']
        service_other = request.POST['service_other']
        actor_id = request.POST['actor_id']

        #Get selected Garment Factory
        #selectedGF = SmsFac.objects.get(quest_21=id_selected_gf)
        #Saving Client
        newClient = Client(
                           sex = client_sex,
                           age = client_age,
                           phone = client_phone,
                           occupation = client_occupation,
                           garment_id = id_selected_gf,
                           adr_street = client_adr_street,
                           adr_village = client_adr_village,
                           adr_commune = client_adr_commune,
                           adr_district = client_adr_district,
                           adr_province = client_adr_province
                           )
        newClient.save()

        #Generate Voucher ID
        if(mode == 1):
            referralFunctions = ReferralFunctions()
            uniqueID = referralFunctions.generateUniqueID()
        else:
            uniqueID = request.POST['referral_id']
            try:
                appoint = Appointment.objects.get(referral_id=uniqueID)
            except ObjectDoesNotExist:
                appoint = None
            if(appoint is not None):
                return HttpResponse(
                content_type='application/json',
                content=json.dumps({
                        'success': 4,
                        'error_msg': "The Referral ID is Duplicated,\nPlease Update it and Submit again",
                        "referral_id": uniqueID
                },default=_json_serial))

        #Save appointment
        appointment = Appointment(
                                 referral_id =  uniqueID,
                                 referral_date = referral_date,
                                 expiry_date = expiry_date,
                                 language = language_sms,
                                 id_client = newClient.id_client,
#                                 id_facility = id_selected_facility,
                                 mode = mode #1=new ; 2=existing
                                  )
        appointment.save()

        #save the operation
        referralOperation = ReferralOperation(
                                              referral_id = uniqueID,
                                              actor_id = actor_id,
                                              facility_id = id_selected_facility,
                                              last_actor_id = 0,
                                              referred_services = services,
                                              other_services = service_other,
                                              status = 1 # 1 = referred
                                              )
        referralOperation.save()

#        send notification
        _refer_send_notification(id_selected_facility)

#        sen SMS
        reports = Reports()
        sms_content,sms_status = reports.smsTextNewReferral(uniqueID, actor_id)
#        sms_status = "19"
#        sms_content = "It is Just a SMS Sample which should be displayed here!"'
        mSerial = MSerializers()
        appointment_return = mSerial.getAppointment(uniqueID,referralOperation.id)
        user = mSerial.getUserById(actor_id)
        garment_report = mSerial.update_garment_report(user)
        return HttpResponse(
        content_type='application/json',
        content=json.dumps({
                'success': 1,
                'error_msg': "Client Referral created SUCCESSFUL",
                "referral_id": uniqueID,
                "sms_status" : sms_status,
                "sms_content" : sms_content,
                "appointments" : appointment_return,
                "refer_report" : garment_report

        },default=_json_serial))

def saveRedeem(request):
    if request.method == 'POST':

        referral_id = request.POST['referral_id']
        actor_id = int(request.POST['actor_id'])
        last_actor_id = int(request.POST['last_actor_id'])
        referred_services = request.POST['referred_services']
        service_other = request.POST['service_other']
        status = int(request.POST['status'])
        is_completed = request.POST['is_completed']
        has_alternative = request.POST['has_alternative']
        provider = request.POST['provider']
        redeem_date = request.POST['redeem_date']
        id_selected_facility = request.POST['id_selected_facility']

        #save the operation
        referralOperation = ReferralOperation(
                                              referral_id = referral_id,
                                              actor_id = actor_id,
                                              last_actor_id = last_actor_id,
                                              referred_services = referred_services,
                                              other_services = service_other,
                                              status = status,
                                              is_completed = is_completed,
                                              has_alternative = has_alternative,
                                              provider = provider,
                                              redeem_date = redeem_date,
                                              facility_id = id_selected_facility
                                              )
        referralOperation.save()
#        send notification redeemed
        _redeem_send_notification(last_actor_id,status)
        mSerial = MSerializers()
        operation = mSerial.getOperation(referralOperation.id)
        user = mSerial.getUserById(actor_id)
        facility_report = mSerial.update_facility_report(user)
        
        return HttpResponse(
        content_type='application/json',
        content=json.dumps({
                'success': 1,
                'error_msg': "Client Referral created SUCCESSFUL",
                "referral_id": referral_id,
                "status": status,
                "operations": operation,
                "refer_report" : facility_report
        },default=_json_serial))
def saveReRefer(request):
    import datetime
    if request.method == 'POST':
        referral_id = request.POST['referral_id']
        mode = request.POST['mode']
        client_id = request.POST['client_id']
        client_sex = request.POST['sex']
        client_phone = request.POST['phone']
        client_age = request.POST['age']
        client_occupation = request.POST['occupation']
        id_selected_gf = request.POST['selected_gf']
        client_adr_street = request.POST['adr_street']
        client_adr_village = request.POST['adr_village']
        client_adr_commune = request.POST['adr_commune']
        client_adr_district = request.POST['adr_district']
        client_adr_province = request.POST['adr_province']
        services = request.POST['services']
        id_selected_facility = request.POST['id_selected_facility']
        referral_date = request.POST['referral_date']
        expiry_date = request.POST['expiry_date']
        language_sms = request.POST['language_sms']
        service_other = request.POST['service_other']
        actor_id = int(request.POST['actor_id'])

        last_actor_id = int(request.POST['last_actor_id'])
        status = int(request.POST['status'])
        redeem_date = datetime.date.today().strftime("%Y-%m-%d")

        #Get selected Garment Factory
        #selectedGF = SmsFac.objects.get(quest_21=id_selected_gf)
        #Saving Client
        newClient = Client(
                        id_client = client_id,
                        sex = client_sex,
                        age = client_age,
                        phone = client_phone,
                        occupation = client_occupation,
                        garment_id = id_selected_gf,
                        adr_street = client_adr_street,
                        adr_village = client_adr_village,
                        adr_commune = client_adr_commune,
                        adr_district = client_adr_district,
                        adr_province = client_adr_province
                           )
        newClient.save()

        #Save appointment
        appointment = Appointment(
                                 referral_id =  referral_id,
                                 referral_date = referral_date,
                                 expiry_date = expiry_date,
                                 language = language_sms,
                                 id_client = newClient.id_client,
                                 mode = mode
                                  )
        appointment.save()

        #save the operation
        #save the operation
        referralOperation = ReferralOperation(
                                              referral_id = referral_id,
                                              actor_id = actor_id,
                                              facility_id = id_selected_facility,
                                              last_actor_id = last_actor_id,
                                              referred_services = services,
                                              other_services = service_other,
                                              status = status, # 4 = re-referred
                                              redeem_date = redeem_date
                                              )
        referralOperation.save()

#        send notification re_referred
        _re_referred_send_notification(last_actor_id)

#        send SMS
        reports = Reports()
        sms_content,sms_status = reports.smsTextNewReferral(referral_id, actor_id)
#        sms_status = "19"
#        sms_content = "It is Just a SMS Sample which should be displayed here!"
        mSerial = MSerializers()
        appointment_return = mSerial.getAppointment(referral_id,referralOperation.id)
        user = mSerial.getUserById(actor_id)
        facility_report = mSerial.update_facility_report(user)

        return HttpResponse(
            content_type='application/json',
            content=json.dumps({
                    'success': 1,
                    'error_msg': "Client Referral created SUCCESSFUL",
                    "referral_id": referralOperation.referral_id,
                    "sms_status" : sms_status,
                    "sms_content" : sms_content,
                    "appointments" : appointment_return,
                    "refer_report" : facility_report
            },default=_json_serial))

def resetPassword(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        user_id = request.POST['user_id']
        user_name = request.POST['user_name']
        user = authenticate(username=user_name, password=current_password)

        if user is not None:
#            user = AuthUser.objects.get(id=user_id)
            new_password = make_password(new_password)
            user.password = new_password
            user.save()
            return HttpResponse(
                content_type='application/json',
                content=json.dumps({
                        'success': 1,
                        "error_msg": "Operation Successful",
                },default=_json_serial))
        else:
            return HttpResponse(
                content_type='application/json',
                content=json.dumps({
                        'success': 2,
                        "error_msg": "Wrong Password entered",
                },default=_json_serial))

def myPing(request):
    return HttpResponse(
        content_type='application/json',
        content=json.dumps({
                'sacasaca': 1,
                "piso messanga": "Written by Human Network International (hni.org)",
        },default=_json_serial))



def _json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError ("Type not serializable")

def _refer_send_notification(facility_id):
    registration_ids = []
    notified_users = AuthUser.objects.filter(facility_id=facility_id)
    if notified_users is not None:
        for user in notified_users:
            reg_id = user.fcm_token
            if reg_id:
                registration_ids.append(reg_id)

    data_message = {
        "status" : 1,
        "notification_type" : "new_referral",
        "facility_id": facility_id
    }
    if len(registration_ids) != 0:
        push_service = FCMNotification(api_key=settings.NOTIFICATION_FCM_API_KEY)
        result = push_service.notify_multiple_devices(registration_ids=registration_ids, data_message=data_message)

def _redeem_send_notification(last_actor_id,status):
    registration_id = None
    notified_user = AuthUser.objects.filter(pk=last_actor_id)
    if notified_user is not None and len(notified_user)!=0:
        registration_id = notified_user[0].fcm_token
    if registration_id is not None:
        data_message = {
            "status" : status,
            "notification_type" : "redeemed",
            "facility_id": last_actor_id
        }
        push_service = FCMNotification(api_key=settings.NOTIFICATION_FCM_API_KEY)
        result = push_service.notify_single_device(registration_id=registration_id, data_message=data_message)

def _re_referred_send_notification(last_actor_id):
    registration_id = None
    notified_user = AuthUser.objects.filter(pk=last_actor_id)
    if notified_user is not None and len(notified_user)!=0:
        registration_id = notified_user[0].fcm_token
    if registration_id is not None:
        data_message = {
            "status" : 4,
            "notification_type" : "re_referred",
            "facility_id": last_actor_id
        }
        push_service = FCMNotification(api_key=settings.NOTIFICATION_FCM_API_KEY)
        result = push_service.notify_single_device(registration_id=registration_id, data_message=data_message)