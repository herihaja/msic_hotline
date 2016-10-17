# -*- coding: utf-8 -*-
from __future__ import division
from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login
from referral_system.classes.Referral import Referral
import json, xlwt
from referral_system.classes.AjaxFunction import AjaxFunction
from referral_system.models import SmsFac, Client, Appointment,\
    ReferralOperation, VoucherCode, ReferredServices, AuthUser
from django.core import serializers
from referral_system.classes.ReferralFunctions import ReferralFunctions
from referral_system.classes.Reports import Reports
from django.contrib.auth import models




# Create your views here.
from web_api.views import _refer_send_notification

def group_check(user):
    return user.groups.filter(name__in=['Hotline Counselor'])

def index(request):
    context = {}
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
            redirect_view = referralFormOnline if user.groups.all()[0].name == 'Hotline Counselor' else viewReferral
                
            return redirect(redirect_view)
        else:
            # Return a 'disabled account' error message
            return redirect(loginPage, error="inactive")
            
    else:
        # Return an 'invalid login' error message.
        return redirect(loginPage, error="wrong")
    
def notificationPage(request, typenotif):
    notificationMessage = ""
    typeNotification = ""
    descriptionText = ""
    reports = Reports()
    
    
    if(typenotif[:3] == 'ok_'):
        tReferralID = typenotif.split("_")
        referralId = tReferralID[1]
        typeNotification = "success"
        notificationMessage = '<h4>Referral was saved successfully ! </h4><br> Referral ID: ' + referralId
        
        descriptionText,status = reports.smsTextNewReferral(referralId, request.user.id)
        
    elif(typenotif[:4] == 'nok_'):
        tReferralID = typenotif.split("_")
        referralId = tReferralID[2]
        typeNotification = "alert"
        notificationMessage = '<h4>Could not save the referral ! </h4><br> The Referral ID <b>' + referralId + '</b> already exist !'
    
    context = {
               'notifications_message': notificationMessage,
               'type_notification': typeNotification,
               'descriptionText' : descriptionText
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
    
    localityProvinces = AjaxFunction.listLocalityProvince()
    occupations = referralClass.getAllOccupations()
    listGarment = SmsFac.get_all_garment_factories()
    listAge = range(14, 51);
    
    #notifications
    notif = ''
    notificationMessage = 'bla'
    if notif == 'online_saved':
        notificationMessage += 'Appointment saved successfully !'
        
    context = {"allServices" : allServices, 
               "allFacilities" : allFacilities, 
               "markerList" : markerList,
               "localityProvinces" : localityProvinces,
               "menuactive" : "online",
               "listAge": listAge,
               "listGarment" : listGarment,
               "occupations" : occupations,
               "notificationMessage" : notif,
               "infowList" : infowList}
    return render(request, 'referral/form_online.html', context)

@login_required(login_url='/referral_system/loginPage/')
@user_passes_test(group_check, login_url='/referral_system/loginPage/access')
def referralFormExisting(request):
    
    referralClass = Referral()
    
    allServices = referralClass.getAllServices()
    allFacilities = referralClass.getAllFacilities() 
    
    localityProvinces = AjaxFunction.listLocalityProvince()
    occupations = referralClass.getAllOccupations()
    listGarment = SmsFac.get_all_garment_factories()
    listAge = range(14, 51);
        
    context = {"allServices" : allServices, 
               "allFacilities" : allFacilities, 
               "occupations" : occupations,               
               "localityProvinces" : localityProvinces,
               "menuactive" : "existing",
               "listAge": listAge,
               "listGarment" : listGarment}
    return render(request, 'referral/form_existing.html', context)

@login_required(login_url='/referral_system/loginPage/')
def viewReferral(request):
    
    startDate, endDate = '', ''
    adr_province = ''
    referrer = ''
    referrer_type = ''
    export = request.method == 'POST' and request.POST.get('action') == 'export'
    
    if request.method == 'POST':
        #here function
        startDate = request.POST['start_date']
        endDate = request.POST['end_date']
        adr_province = request.POST['adr_province']
        referrer = request.POST['referrer']
        referrer_type = request.POST.get('referrer_type', '')
    
    reports = Reports()
    localityProvinces = AjaxFunction.listLocalityProvince()
    
    ### CLIENTS
    referralReports = reports.clientsPerStatus(startDate, endDate, adr_province, referrer, referrer_type)
    """
    {
                    name: 'Microsoft Internet Explorer',
                    y: 56.33,
                    drilldown: 'Microsoft Internet Explorer'
                }
    """
    status = ['','Not visited yet','Redeemed','Service not taken','Re-referred', 'Expired']
    listClientData = []
    listClientObject = []

    numberClients = sum([itemReport["number_client"] for itemReport in referralReports])
    
    for itemReport in referralReports:
        itemObj = []
        _name = status[itemReport["status"]]
        status[itemReport["status"]] = ''
        
        _y = (itemReport["number_client"] * 100) / numberClients

        itemObj.append(_name)
        itemObj.append("%.2f%s" % (_y, "%"))
        itemObj.append(itemReport["number_client"])
        
        listClientObject.append(itemObj)
        
        listClientData.append("{name:'" + _name + "',y:" + str(_y) + ",drilldown:'" + _name + "'}")

    for _name in status:
        if not _name: continue
        itemObj = [_name, "0%", 0]
        listClientObject.append(itemObj)

        listClientData.append("{name:'" + _name + "',y:0,drilldown:'" + _name + "'}")

    strData = ",".join(listClientData)
    
    ## SERVICES DELIVERED
    servicesDelivered = reports.servicesDelivered(startDate, endDate, adr_province, referrer, referrer_type)
    allServices = ReferredServices.get_all_in_customized_order()
    
    reportServices = {}
    listService = []
    listObjectService = []
    numberServices = 0
    allServicesName = [service.service_name for service in allServices]
    for itemServiceDelivered in servicesDelivered:
        listServicesDelivered = [itemS for itemS in itemServiceDelivered['referred_services'].split(";") if itemS in allServicesName]
        numberServices += len(listServicesDelivered)
            
    for itemService in allServices:
        itemObj = []
        nb = 0
        for itemServiceDelivered in servicesDelivered:
            listServicesDelivered = itemServiceDelivered['referred_services'].split(";")
            for itemS in listServicesDelivered:
                if itemS.strip() == itemService.service_name.strip():
                    nb = nb + 1
                    
                    
        reportServices[itemService.service_name] = nb
        listService.append("{name:'" + itemService.service_name + "',y:" + str(nb) + ",drilldown:'" + itemService.service_name + "'}")
        
        
        if numberServices == 0:
            _percentage = 0
        else:
            _percentage = (nb * 100) / numberServices
        
        itemObj.append(itemService.service_name)
        itemObj.append("%.2f%s" % (_percentage, "%"))
        itemObj.append(nb)
        listObjectService.append(itemObj)
        
    jsonService = ",".join(listService)

    from collections import OrderedDict
    referrerList = OrderedDict({})
    if request.user.groups.all()[0].name == "Hotline Counselor":
        referrerList.update({u"%s" % request.user.id:'My Referral', 'all_counselors': 'All counselors'})
    else:
        for counselor in AuthUser.objects.filter(is_staff=False).exclude(groups__name__in=['Project Team']).order_by('first_name'):
            referrerList.update({u"%s" % counselor.id:"%s %s" % (counselor.first_name, counselor.last_name)})

    
    context = {
               "listObject" : listClientObject ,
               "listObjectService" : listObjectService ,
               "reportServices" : reportServices ,
               "jsonService" : jsonService ,
               "menuactive" : "view",
               "jsonData" : strData,
               "numberClients" : numberClients,
               "numberServices" : numberServices,
               "localityProvinces" : localityProvinces,
               "startDate" : startDate,
               "endDate": endDate,
               "adr_province" : adr_province,
               "user_id" : str(request.user.id),
               "referrer" : referrer,
               "totalReferrals": "100" if numberClients > 0 else "0",
               "totalServices": "100" if numberServices > 0 else "0",
               "referrerList": referrerList,
               "referrer_type": referrer_type,
               }

    if export:
        return exportExcel(request, context)

    return render(request, 'referral/view_referral.html', context)

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
        client_adr_province = request.POST.get('adr_province', '')
        services = request.POST.getlist('service[]')  #should be an array
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
                                 expiry_date = expiry_date,
                                 language = language_sms,
                                 id_client = newClient.id_client,
#                                 id_facility = id_selected_facility,
                                 mode = 1 #1=new ; 2=existing
                                  )
        appointment.save()
        
        #save the operation
        referralOperation = ReferralOperation(
                                              referral_id = uniqueID,
                                              actor_id = request.user.id,
                                              facility_id = id_selected_facility,
                                              last_actor_id = request.user.id,
                                              referred_services = ';'.join(services),
                                              other_services = service_other,
                                              status = 1 # 1 = referred                                               
                                              )
        referralOperation.save()

        _refer_send_notification(id_selected_facility)
        
        #Notification format: ok_referalid
        notifParam = "ok_" + uniqueID
              
            
        
    return redirect(notificationPage, typenotif = notifParam)

@login_required(login_url='/referral_system/loginPage/')
@user_passes_test(group_check, login_url='/referral_system/loginPage/access')
def referralSaveExistingForm(request):
    if request.method == 'POST':
        #here function
        
        referral_id = request.POST['referral_id'].upper()
        client_sex = request.POST['sex']
        client_phone = request.POST['phone']
        client_age = request.POST['age']
        client_occupation = request.POST['occupation']
        id_selected_gf = request.POST['selected_gf']
        client_adr_street = request.POST['adr_street']
        client_adr_village = request.POST['adr_village']
        client_adr_commune = request.POST['adr_commune']
        client_adr_district = request.POST['adr_district']
        client_adr_province = request.POST.get('adr_province', '')
        services = request.POST.getlist('service[]')  #should be an array
        id_selected_facility = request.POST['id_selected_facility']
        referral_date = request.POST['referral_date']
        expiry_date = request.POST['expiry_date']
        language_sms = request.POST['language_sms']
        service_other = request.POST['service_other']
        
        #Get selected Garment Factory
        #selectedGF = SmsFac.objects.get(quest_21=id_selected_gf)
        
        #Test if inserted unique ID already exist
        if Appointment.objects.filter(referral_id=referral_id):
            #Notification format: nok_uniqueiderror_id
            notifParam = "nok_uniqueiderror_" + referral_id
            return redirect(notificationPage, typenotif = notifParam)
        
        #Typed Referral ID        
        uniqueID = referral_id
        
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
        
        
        
        #Save appointment
        appointment = Appointment(
                                 referral_id =  uniqueID,
                                 referral_date = referral_date,
                                 expiry_date = expiry_date,
                                 language = language_sms,
                                 id_client = newClient.id_client,
#                                 id_facility = id_selected_facility,
                                 mode = 2 #1=new ; 2=existing
                                  )
        appointment.save()
        
        #save the operation
        referralOperation = ReferralOperation(
                                              referral_id = uniqueID,
                                              actor_id = request.user.id,
                                              facility_id = id_selected_facility,
                                              last_actor_id = request.user.id,
                                              referred_services = ';'.join(services),
                                              other_services = service_other,
                                              status = 1 # 1 = referred                                               
                                              )
        referralOperation.save()

        _refer_send_notification(id_selected_facility)
        
        
        #Notification format: ok_referalid
        notifParam = "ok_" + uniqueID  
        
    return redirect(notificationPage, typenotif = notifParam)

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
        objFacility = SmsFac.objects.get(quest_20=request.POST['quest_20'])
        
        facility += "" + (objFacility.quest_19).replace("'", " ") #name 0
        facility += "====" + objFacility.quest_24 #coordinnates 1
        facility += "====" + (objFacility.quest_16).replace("'", " ") #street 2
        facility += "====" + (objFacility.quest_18).replace("'", " ") #village 3
        facility += "====" + (objFacility.quest_13).replace("'", " ") #commune 4
        facility += "====" + (objFacility.quest_30).replace("'", " ") #district 5
        facility += "====" + (objFacility.quest_15).replace("'", " ") #province 6
        facility += "====" + (objFacility.quest_11).replace("'", " ") #phone 7
        facility += "; " + (objFacility.quest_26).replace("'", " ")
        facility += "; " + (objFacility.quest_31).replace("'", " ")
        facility += "====" + (objFacility.quest_48).replace("'", " ") #hours 8
        facility += "====" + (objFacility.quest_27).replace("'", " ") #FP Services 9
        facility += "====" + (objFacility.quest_28).replace("'", " ") #Safe abortion services 10
        facility += "====" + (objFacility.quest_37).replace("'", " ") #Safe abortion services 11
        #khmer version
        facility += "====" + objFacility.quest_12 #name khmer 12
        facility += "====" + objFacility.quest_34 #street khmer 13
        facility += "====" + objFacility.quest_43 #village khmer 14
        facility += "====" + objFacility.quest_39 #commune khmer 15
        facility += "====" + objFacility.quest_47 #district khmer 16
        facility += "====" + objFacility.quest_41 #province khmer 17
        
        facility += "====" + objFacility.quest_49 # referred service 18
        
        
        
        
    return HttpResponse(facility)

#Ajax functions for Garment factory
def ajaxListLocalityDistrict(request):
    listDistricts = ''
    if request.method == 'POST':
        allDistricts  = AjaxFunction.listLocalityDistrict(request.POST['province'])
        listDistricts = json.dumps(allDistricts)
        
    return HttpResponse(listDistricts)

def ajaxListLocalityCommune(request):
    listCommune = ''
    if request.method == 'POST':
        allCommunes  = AjaxFunction.listLocalityCommune(request.POST['district'], request.POST['province'])
        listCommune = json.dumps(allCommunes)
        
    return HttpResponse(listCommune)

def ajaxListLocalityVillage(request):
    listVillage = ''
    if request.method == 'POST':
        allVillages  = AjaxFunction.listLocalityVillage(request.POST['commune'],request.POST['district'], request.POST['province'])
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


def exportExcel(request, context):
    book = xlwt.Workbook(encoding="utf-8")
    row = 1
    
    referral_sheet = book.add_sheet("Referral")
    referral_sheet.write(0,0, "Status")
    referral_sheet.write(0,1, "Percentage")
    referral_sheet.write(0,2, "Referral")

    for object in context.get('listObject'):
        referral_sheet.write(row, 0, object[0].capitalize())
        referral_sheet.write(row, 1, object[1])
        referral_sheet.write(row, 2, int(object[2]))
        row += 1


    referral_sheet.write(row, 0, "Total")
    referral_sheet.write(row, 1, "%s%s" % (context.get('totalReferrals'), "%"))
    referral_sheet.write(row, 2, context.get('numberClients'))

    services_sheet = book.add_sheet("Services referred")
    services_sheet.write(0,0, "Services")
    services_sheet.write(0,1, "Percentage")
    services_sheet.write(0,2, "Number of services")

    row = 1
    for service in context.get('listObjectService'):
        services_sheet.write(row,0, service[0].capitalize())
        services_sheet.write(row,1, service[1])
        services_sheet.write(row,2, service[2])
        row += 1

    services_sheet.write(row, 0, "Total")
    services_sheet.write(row, 2, context.get("numberServices"))
    services_sheet.write(row, 1, "%s%s" % (context.get("totalServices"),"%"))

        
    response = HttpResponse(content_type="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=report.xls'
    book.save(response)
    return response

def send_sms(request):
    sms_content = "this is a very long sms to test the behavior when the message is longer than one sixty characters, Aimee, Please let me know when you get it, if possible to have a screenshot that will be very helpful, thanks"
    sms_content = "Hi Aimee, did you get my previous sms from the system? It's Heri."
    sms_content = unicode("នេះគឺជាការផ្ញើសារជាអក្សរបានយ៉ាងយូរដើម្បីសាកល្បងឥរិយាបថពេលដែលសារនេះគឺជាតួអក្សរហុកសិបយូរជាងមួយរបស់ Aimee, សូមអនុញ្ញាតឱ្យខ្ញុំដឹងថានៅពេលដែលអ្នកទទួលបានវាបើអាចធ្វើទៅបានដើម្បីឱ្យមានរូបថតអេក្រង់ដែលនឹងមានប្រយោជន៍ខ្លាំងណាស់, អរគុណ")
    Reports().sendMessage("012818614", sms_content, 1, 1, 'khmer')
    return HttpResponse(sms_content)
