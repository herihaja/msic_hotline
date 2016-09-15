from referral_system.models import SmsFac, ReferredServices, Occupation
import json
from django.db import connection
from referral_system.classes.AjaxFunction import AjaxFunction
from django.db.models import Q


class Referral:
    allFacilities = ''
    facilityMarkerList = ""
    allServices = ''
    facilityInfowList = ""
    
    def __init__(self):
        self.populateFacilities()
        self.populateServices()
        self.createFacilitiesMarkers()
        self.createFacilityInfoswindow()
    
    def populateFacilities(self):
        dictFacilities = AjaxFunction.runSQL('''
        SELECT
        * 
        FROM
        sms_fac
        WHERE
        quest_50 LIKE 'Both (Referral System and Public Facing Platform)' 
        OR 
        quest_50 LIKE 'Referral System only'
        ''')
        
        #self.allFacilities = list(dictFacilities)
        
        self.allFacilities = SmsFac.objects.all().filter(
                                                         Q(quest_50 = "Both (Referral System and Public Facing Platform)")                                                         
                                                         |
                                                         Q(quest_50 = "Referral System only")
                                                         ).order_by('quest_12') #show on GIS ? Yes or No
        
    def populateServices(self):
        self.allServices = ReferredServices.objects.all()
    
    def createFacilitiesMarkers(self):
        markers = [self.createMarker(facility) for facility in self.allFacilities if facility.quest_24 != '' ]
        self.facilityMarkerList = ','.join(markers)
                
    def createFacilityInfoswindow(self):
        infowCptr = 0;
        for  itemFacility in self.allFacilities:           
                if(infowCptr != 0):
                    self.facilityInfowList += ","
                self.facilityInfowList += "['<div class=\"info_content\">" 
                self.facilityInfowList += "<h6><b>" + (itemFacility.quest_20).replace("'", " ") + "<br />" + (itemFacility.quest_12).replace("'", " ")+ "</b></h6><hr />" 
                self.facilityInfowList += "<p><b>Address [EN]:</b>: " + json.dumps(itemFacility.quest_17) + " "
                self.facilityInfowList += json.dumps(itemFacility.quest_19).replace("'", " ") + " "
                self.facilityInfowList += json.dumps(itemFacility.quest_14).replace("'", " ") + " "
                self.facilityInfowList += json.dumps(itemFacility.quest_31).replace("'", " ") + " "
                self.facilityInfowList += json.dumps(itemFacility.quest_16).replace("'", " ") + " "
                self.facilityInfowList += "</p>"
                self.facilityInfowList += "<p><b>Address [KHMER]:</b>: " + json.dumps(itemFacility.quest_35) + " "
                self.facilityInfowList += json.dumps(itemFacility.quest_44).replace("'", " ") + " "
                self.facilityInfowList += json.dumps(itemFacility.quest_40).replace("'", " ") + " "
                self.facilityInfowList += json.dumps(itemFacility.quest_48).replace("'", " ") + " "
                self.facilityInfowList += json.dumps(itemFacility.quest_42).replace("'", " ") + " "
                self.facilityInfowList += "</p>"
                self.facilityInfowList += "<p><b>Opening Hours:</b>: " + json.dumps(itemFacility.quest_49).replace("'", " ") + " </p>"
                self.facilityInfowList += "<p><a href=\"#\">More details</a></p>"
                
                
                #self.facilityInfowList += "<p><b>Address:</b>: " + json.dumps(itemFacility.quest_17) + " " + "</p>" 
                self.facilityInfowList += "</div>'] "
                infowCptr = infowCptr + 1
                
    
        
                
    #getters
    def getFacilityMarkerList(self):
        return self.facilityMarkerList
    
    def getFacilityInfowList(self):
        return self.facilityInfowList
    
    def getAllServices(self):
        return self.allServices 
    
    def getAllFacilities(self):
        return self.allFacilities     
    
    def getAllOccupations(self):
        return Occupation.objects.all()
    
    def createMarker(self, facility):
        marker = "['" + (facility.quest_19).replace("'", " ") #name 0
        marker += "'," + facility.quest_24 #coordinnates 1-2
        marker += ",'" + (facility.quest_16).replace("'", " ") #street 3
        marker += "','" + (facility.quest_18).replace("'", " ") #village 4
        marker += "','" + (facility.quest_13).replace("'", " ") #commune 5
        marker += "','" + (facility.quest_30).replace("'", " ") #district 6
        marker += "','" + (facility.quest_15).replace("'", " ") #province 7
        marker += "','<ul>"  #phone 8
        if(facility.quest_11.replace("'", " ").strip() != ''):
            marker += "<li>" + (facility.quest_11).replace("'", " ") + "</li>" #phone 0st
        if(facility.quest_26.replace("'", " ").strip() != ''):
            marker += "<li>" + (facility.quest_26).replace("'", " ") + "</li>" #phone 1st
        if(facility.quest_31.replace("'", " ").strip() != ''):
            marker += "<li>" + (facility.quest_31).replace("'", " ") + "</li>" #phone 2nd
        marker += "</ul>','" + (facility.quest_48).replace("'", " ") #hours 9
        marker += "','" + (facility.quest_27).replace("'", " ") #FP Services 10
        marker += "','" + (facility.quest_28).replace("'", " ") #Safe abortion services 11
        marker += "','" + (facility.quest_37).replace("'", " ") #Safe abortion services 12
        marker += "','" + (facility.quest_20).replace("'", " ") #ID 13

        #khmer
        marker += "','" + (facility.quest_41).replace("'", " ") #province khmer 14
        marker += "','" + (facility.quest_47).replace("'", " ") #district khmer 15
        marker += "','" + (facility.quest_39).replace("'", " ") #commune khmer 16
        marker += "','" + (facility.quest_43).replace("'", " ") #village khmer 17
        marker += "','" + (facility.quest_34).replace("'", " ") #street khmer 18
        marker += "','" + (facility.quest_12).replace("'", " ") #name khmer 19
        
        marker += "','" + (facility.quest_49).replace("'", " ") # referred service 20

        marker += "']"
        return marker
                
    
                
                