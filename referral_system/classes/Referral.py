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
                self.facilityMarkerList += "['" + (itemFacility.quest_20).replace("'", " ") #name
                self.facilityMarkerList += "'," + itemFacility.quest_25 #coordinnates
                self.facilityMarkerList += ",'" + (itemFacility.quest_17).replace("'", " ") #street
                self.facilityMarkerList += "','" + (itemFacility.quest_19).replace("'", " ") #village
                self.facilityMarkerList += "','" + (itemFacility.quest_40).replace("'", " ") #commune
                self.facilityMarkerList += "','" + (itemFacility.quest_48).replace("'", " ") #district
                self.facilityMarkerList += "','" + (itemFacility.quest_16).replace("'", " ") #province
                self.facilityMarkerList += "','" + (itemFacility.quest_27).replace("'", " ") #phone
                self.facilityMarkerList += "','" + (itemFacility.quest_49).replace("'", " ") #hours
                self.facilityMarkerList += "','" + (itemFacility.quest_28).replace("'", " ") #FP Services
                self.facilityMarkerList += "','" + (itemFacility.quest_29).replace("'", " ") #Safe abortion services
                self.facilityMarkerList += "','" + (itemFacility.quest_38).replace("'", " ") #Safe abortion services
                self.facilityMarkerList += "']"
            
                markerCptr = markerCptr + 1
                
    def createFacilityInfoswindow(self):
        infowCptr = 0;
        for  itemFacility in self.allFacilities:
            if(itemFacility.quest_25 != ""):
                if(infowCptr != 0):
                    self.facilityInfowList += ","
                self.facilityInfowList += "['<div class=\"info_content\">" 
                self.facilityInfowList += "<h6>" + json.dumps(itemFacility.quest_20).replace("'", " ") + "</h6>" 
                self.facilityInfowList += "<p>" + json.dumps(itemFacility.quest_27).strip('"') + "</p>" 
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
                
    
                
                