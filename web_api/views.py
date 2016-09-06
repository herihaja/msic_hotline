from datetime import datetime
from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login
from referral_system.classes.Referral import Referral
import json
from referral_system.classes.AjaxFunction import AjaxFunction
from referral_system.models import SmsFac, Client, Appointment, ReferralOperation
from django.core import serializers
from referral_system.classes.ReferralFunctions import ReferralFunctions


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
    user = authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            login(request, user)
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
        mode = request.POST['mode']
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
        services = request.POST.getlist('services')  #should be an array
#        searchtype = request.POST['searchtype'] #search by GF or address
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

        print mode

        #Generate Voucher ID
        if(mode == 1):
            referralFunctions = ReferralFunctions()
            uniqueID = referralFunctions.generateUniqueID()
        else:
            uniqueID = request.POST['referral_id']


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
                                              last_actor_id = request.user.id,
                                              referred_services = ';'.join(services),
                                              other_services = service_other,
                                              status = 1 # 1 = referred
                                              )
        referralOperation.save()
        return HttpResponse(
        content_type='application/json',
        content=json.dumps({
                'success': 1,
                'error_msg': "Client Referral created SUCCESSFUL",
                "referral_id": uniqueID
        },default=_json_serial))

def saveRedeem(request):
    if request.method == 'POST':
        #here function
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
        return HttpResponse(
        content_type='application/json',
        content=json.dumps({
                'success': 1,
                'error_msg': "Client Referral created SUCCESSFUL",
                "operation_id": referralOperation.id
        },default=_json_serial))

def _json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError ("Type not serializable")