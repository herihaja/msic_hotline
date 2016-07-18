from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login
from referral_system.classes.Referral import Referral
import json
from referral_system.classes.AjaxFunction import AjaxFunction
from referral_system.models import SmsFac
from django.core import serializers


# Create your views here.

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

@login_required(login_url='/referral_system/loginPage/')
@user_passes_test(group_check, login_url='/referral_system/loginPage/access')
def referralFormOnline(request):
    
    referralClass = Referral()
    
    allServices = referralClass.getAllServices()
    allFacilities = referralClass.getAllFacilities()
    markerList = referralClass.getFacilityMarkerList()
    infowList = referralClass.getFacilityInfowList()
    
    garmentProvinces = AjaxFunction.listGarmentProvince()
        
    context = {"allServices" : allServices, 
               "allFacilities" : allFacilities, 
               "markerList" : markerList,
               "garmentProvinces" : garmentProvinces,
               "menuactive" : "online",
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
        
        facility += "" + (objFacility.quest_20).replace("'", " ") #name
        facility += "====" + objFacility.quest_25 #coordinnates
        facility += "====" + (objFacility.quest_17).replace("'", " ") #street
        facility += "====" + (objFacility.quest_19).replace("'", " ") #village
        facility += "====" + (objFacility.quest_40).replace("'", " ") #commune
        facility += "====" + (objFacility.quest_48).replace("'", " ") #district
        facility += "====" + (objFacility.quest_16).replace("'", " ") #province
        facility += "====" + (objFacility.quest_27).replace("'", " ") #phone
        facility += "====" + (objFacility.quest_49).replace("'", " ") #hours
        facility += "====" + (objFacility.quest_28).replace("'", " ") #FP Services
        facility += "====" + (objFacility.quest_29).replace("'", " ") #Safe abortion services
        facility += "====" + (objFacility.quest_38).replace("'", " ") #Safe abortion services
        
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
                                                                          quest_22="Garment factory infirmary",
                                                                          quest_31=request.POST['district'],
                                                                          quest_44=request.POST['village']
                                                                          )
                                            )
        #listFacilities = json.dumps(listFacilities)
        
    return HttpResponse(listGarment)