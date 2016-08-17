from datetime import datetime
from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login
from referral_system.classes.Referral import Referral
import json
from referral_system.classes.AjaxFunction import AjaxFunction
from referral_system.models import SmsFac, Client, Appointment, ReferralService,\
    OtherServices
from django.core import serializers
from referral_system.classes.ReferralFunctions import ReferralFunctions


# Create your views here.
from web_api.classes.mSerializers import MSerializers

def getFacilities(request):
    mSerializer = MSerializers()
    facilities = mSerializer.select_all_facilities()
    appointments = mSerializer.select_all_appointments()
    services = mSerializer.select_all_services()
    return HttpResponse(
        content_type='application/json',
        content=json.dumps({
                'success': "OK",
                'error_msg': "OK",
                "facilities": facilities,
                "appointments": appointments,
                "services":services
        },default=_json_serial))




def group_check(user):
    return user.groups.filter(name__in=['Hotline Consellor'])

def index(request):
    context = {'variable': 1234}
    return render(request, 'referral/index.html', context)

def viewClient(request, client_id):
    return HttpResponse("You're looking at client %s." % client_id)

def loginPage(request, error=""):

    if(error == 'inactive'):
        errorText = "This user exists but not active !"
    elif(error == 'wrong'):
        errorText = "Wrong username or/and password !"
    elif(error == 'access'):
        errorText = "You do not have access to this page !"
    elif(error == 'logout'):
        errorText = "You are successfully logged out !"
    else:
        errorText = ""

    context = {"error" : errorText}
    return render(request, 'referral/login.html', context)

def authenticateMsicHotline(request):

    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to a success page.
            return redirect(referralFormOnline)
        else:
            # Return a 'disabled account' error message
            return redirect(loginPage, error="inactive")

    else:
        # Return an 'invalid login' error message.
        return redirect(loginPage, error="wrong")

def notificationPage(request, typenotif):
    notificationMessage = ""
    typeNotification = ""

    if(typenotif == '01'):
        typeNotification = "success"
        notificationMessage = 'Appointment saved successfully !'

    context = {
               'notifications_message': notificationMessage,
               'type_notification': typeNotification
               }

    return render(request, 'referral/notification_page.html', context)


@login_required(login_url='/referral_system/loginPage/')
@user_passes_test(group_check, login_url='/referral_system/loginPage/access')
def referralFormOnline(request):

    referralClass = Referral()

    allServices = referralClass.getAllServices()
    allFacilities = referralClass.getAllFacilities()
    markerList = referralClass.getFacilityMarkerList()
    infowList = referralClass.getFacilityInfowList()

    garmentProvinces = AjaxFunction.listGarmentProvince()

    #notifications
    notif = ''
    notificationMessage = 'bla'
    if notif == 'online_saved':
        notificationMessage += 'Appointment saved successfully !'

    context = {"allServices" : allServices,
               "allFacilities" : allFacilities,
               "markerList" : markerList,
               "garmentProvinces" : garmentProvinces,
               "menuactive" : "online",
               "notificationMessage" : notif,
               "infowList" : infowList}
    return render(request, 'referral/form_online.html', context)

@login_required(login_url='/referral_system/loginPage/')
@user_passes_test(group_check, login_url='/referral_system/loginPage/access')
def referralFormExisting(request):

    referralClass = Referral()

    allServices = referralClass.getAllServices()
    allFacilities = referralClass.getAllFacilities()
    markerList = referralClass.getFacilityMarkerList()
    infowList = referralClass.getFacilityInfowList()

    allProvinces = AjaxFunction.listFacilityProvince()
    garmentProvinces = AjaxFunction.listGarmentProvince()

    context = {"allServices" : allServices,
               "allFacilities" : allFacilities,
               "markerList" : markerList,
               "allProvinces" : allProvinces,
               "garmentProvinces" : garmentProvinces,
               "menuactive" : "existing",
               "infowList" : infowList}
    return render(request, 'referral/form_existing.html', context)

@login_required(login_url='/referral_system/loginPage/')
@user_passes_test(group_check, login_url='/referral_system/loginPage/access')
def referralSaveOnlineForm(request):
    if request.method == 'POST':
        #here function
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
        services = request.POST.getlist('service')  #should be an array
        searchtype = request.POST['searchtype'] #search by GF or address
        id_selected_facility = request.POST['id_selected_facility']
        referral_date = request.POST['referral_date']
        expiry_date = request.POST['expiry_date']
        language_sms = request.POST['language_sms']
        service_other = request.POST['service_other']

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
        referralFunctions = ReferralFunctions()
        uniqueID = referralFunctions.generateUniqueID()

        #Save appointment
        appointment = Appointment(
                                 referral_id =  uniqueID,
                                 referral_date = referral_date,
                                 language = language_sms,
                                 id_client = newClient.id_client,
                                 id_facility = id_selected_facility,
                                 mode = 1 #1=new ; 2=existing
                                  )
        appointment.save()

        #Save Services
        for itemService in services:
            objReferralService = ReferralService(
                                                 id_app = appointment.referral_id,
                                                 id_service = itemService
                                                 )
            objReferralService.save()

        #Save other service if exists
        if(service_other.strip() <> ''):
            otherService = OtherServices(
                                         other_services_name = service_other.strip(),
                                         id_appointment = appointment.referral_id
                                         )
            otherService.save()


    return redirect(notificationPage, typenotif = '01')

@login_required(login_url='/referral_system/loginPage/')
@user_passes_test(group_check, login_url='/referral_system/loginPage/access')
def referralSaveExistingForm(request):
    if request.method == 'POST':
        #here function

        referral_id = request.POST['referral_id']
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
        services = request.POST.getlist('service')  #should be an array
        id_selected_facility = request.POST['id_selected_facility']
        referral_date = request.POST['referral_date']
        expiry_date = request.POST['expiry_date']
        language_sms = request.POST['language_sms']
        service_other = request.POST['service_other']

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

        #Typed Referral ID
        uniqueID = referral_id

        #Save appointment
        appointment = Appointment(
                                 referral_id =  uniqueID,
                                 referral_date = referral_date,
                                 language = language_sms,
                                 id_client = newClient.id_client,
                                 id_facility = id_selected_facility,
                                 mode = 2 #1=new ; 2=existing
                                  )
        appointment.save()

        #Save Services
        for itemService in services:
            objReferralService = ReferralService(
                                                 id_app = appointment.referral_id,
                                                 id_service = itemService
                                                 )
            objReferralService.save()

        #Save other service if exists
        if(service_other.strip() <> ''):
            otherService = OtherServices(
                                         other_services_name = service_other.strip(),
                                         id_appointment = appointment.referral_id
                                         )
            otherService.save()


    return redirect(notificationPage, typenotif = '01')

#Ajax functions for facilities
def ajaxListDistrict(request):
    listDistricts = ''
    if request.method == 'POST':
        allDistricts  = AjaxFunction.listFacilityDistrict(request.POST['province'])
        listDistricts = json.dumps(allDistricts)

    return HttpResponse(listDistricts)

def ajaxListVillage(request):
    listVillage = ''
    if request.method == 'POST':
        allVillages  = AjaxFunction.listFacilityVillage(request.POST['district'], request.POST['province'])
        listVillage = json.dumps(allVillages)

    return HttpResponse(listVillage)

def ajaxListFacilities(request):
    listFacilities = ''
    if request.method == 'POST':
        listFacilities = serializers.serialize("json", SmsFac.objects.filter(
                                                                             quest_16=request.POST['province'],
                                                                             quest_31=request.POST['district'],
                                                                             quest_44=request.POST['village']
                                                                             ))
        #listFacilities = json.dumps(listFacilities)

    return HttpResponse(listFacilities)

def ajaxSelectFacility(request):
    facility = ''
    if request.method == 'POST':
        objFacility = SmsFac.objects.get(quest_21=request.POST['quest_21'])

        facility += "" + (objFacility.quest_20).replace("'", " ") #name 0
        facility += "====" + objFacility.quest_25 #coordinnates 1
        facility += "====" + (objFacility.quest_17).replace("'", " ") #street 2
        facility += "====" + (objFacility.quest_19).replace("'", " ") #village 3
        facility += "====" + (objFacility.quest_14).replace("'", " ") #commune 4
        facility += "====" + (objFacility.quest_31).replace("'", " ") #district 5
        facility += "====" + (objFacility.quest_16).replace("'", " ") #province 6
        facility += "====" + (objFacility.quest_13).replace("'", " ") #phone 7
        facility += "; " + (objFacility.quest_27).replace("'", " ")
        facility += "; " + (objFacility.quest_32).replace("'", " ")
        facility += "====" + (objFacility.quest_49).replace("'", " ") #hours 8
        facility += "====" + (objFacility.quest_28).replace("'", " ") #FP Services 9
        facility += "====" + (objFacility.quest_29).replace("'", " ") #Safe abortion services 10
        facility += "====" + (objFacility.quest_38).replace("'", " ") #Safe abortion services 11
        #khmer version
        facility += "====" + objFacility.quest_12 #name khmer 12
        facility += "====" + objFacility.quest_35 #street khmer 13
        facility += "====" + objFacility.quest_44 #village khmer 14
        facility += "====" + objFacility.quest_40 #commune khmer 15
        facility += "====" + objFacility.quest_48 #district khmer 16
        facility += "====" + objFacility.quest_42 #province khmer 17


    return HttpResponse(facility)

#Ajax functions for Garment factory
def ajaxListGFDistrict(request):
    listDistricts = ''
    if request.method == 'POST':
        allDistricts  = AjaxFunction.listGarmentDistrict(request.POST['province'])
        listDistricts = json.dumps(allDistricts)

    return HttpResponse(listDistricts)

def ajaxListGFVillage(request):
    listVillage = ''
    if request.method == 'POST':
        allVillages  = AjaxFunction.listGarmentVillage(request.POST['district'], request.POST['province'])
        listVillage = json.dumps(allVillages)

    return HttpResponse(listVillage)

def ajaxListGarment(request):
    listGarment = ''
    if request.method == 'POST':
        listGarment = serializers.serialize("json", SmsFac.objects.filter(
                                                                          quest_16=request.POST['province'],
                                                                          quest_19=request.POST['village'],
                                                                          quest_22="Garment factory infirmary",
                                                                          quest_31=request.POST['district']
                                                                          )
                                            )
        #listFacilities = json.dumps(listFacilities)

    return HttpResponse(listGarment)

def _json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError ("Type not serializable")