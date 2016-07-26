from referral_system.models import SmsFac, Service
import json
from django.db import connection


class Referral:
    allFacilities = ''
    facilityMarkerList = "";
    allServices = ''
    facilityInfowList = "";
    
    def __init__(self):
        self.populateFacilities()
        self.populateServices()
        self.createFacilitiesMarkers()
        self.createFacilityInfoswindow()
    
    def populateFacilities(self):
        self.allFacilities = SmsFac.objects.all().extra(where=[" UPPER(quest_26) = 'YES' "])
        #self.allFacilities = SmsFac.objects.all().filter(quest_26="Yes") #show on GIS ? Yes or No
        
    def populateServices(self):
        self.allServices = Service.objects.all()
    
    def createFacilitiesMarkers(self):
        markerCptr = 0;
        
        for  itemFacility in self.allFacilities:
            if(itemFacility.quest_25 != ""):
                if(markerCptr != 0):
                    self.facilityMarkerList += ","
                self.facilityMarkerList += "['" + (itemFacility.quest_20).replace("'", " ") #name 0
                self.facilityMarkerList += "'," + itemFacility.quest_25 #coordinnates 1-2
                self.facilityMarkerList += ",'" + (itemFacility.quest_17).replace("'", " ") #street 3
                self.facilityMarkerList += "','" + (itemFacility.quest_19).replace("'", " ") #village 4
                self.facilityMarkerList += "','" + (itemFacility.quest_14).replace("'", " ") #commune 5
                self.facilityMarkerList += "','" + (itemFacility.quest_31).replace("'", " ") #district 6
                self.facilityMarkerList += "','" + (itemFacility.quest_16).replace("'", " ") #province 7
                self.facilityMarkerList += "','" + (itemFacility.quest_13).replace("'", " ") #phone 8
                self.facilityMarkerList += "; "+ (itemFacility.quest_27).replace("'", " ") #phone 1st
                self.facilityMarkerList += "; "+ (itemFacility.quest_32).replace("'", " ") #phone 2nd
                self.facilityMarkerList += "','" + (itemFacility.quest_49).replace("'", " ") #hours 9
                self.facilityMarkerList += "','" + (itemFacility.quest_28).replace("'", " ") #FP Services 10
                self.facilityMarkerList += "','" + (itemFacility.quest_29).replace("'", " ") #Safe abortion services 11
                self.facilityMarkerList += "','" + (itemFacility.quest_38).replace("'", " ") #Safe abortion services 12
                self.facilityMarkerList += "','" + (itemFacility.quest_21).replace("'", " ") #ID 13
                
                #khmer
                self.facilityMarkerList += "','" + (itemFacility.quest_42).replace("'", " ") #province khmer 14
                self.facilityMarkerList += "','" + (itemFacility.quest_48).replace("'", " ") #district khmer 15
                self.facilityMarkerList += "','" + (itemFacility.quest_40).replace("'", " ") #commune khmer 16
                self.facilityMarkerList += "','" + (itemFacility.quest_44).replace("'", " ") #village khmer 17
                self.facilityMarkerList += "','" + (itemFacility.quest_35).replace("'", " ") #street khmer 18
                self.facilityMarkerList += "','" + (itemFacility.quest_12).replace("'", " ") #name khmer 19
                
                self.facilityMarkerList += "']"
            
                markerCptr = markerCptr + 1
                
    def createFacilityInfoswindow(self):
        infowCptr = 0;
        for  itemFacility in self.allFacilities:
            if(itemFacility.quest_25 != ""):
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
                
    
                
                