from referral_system.classes.AjaxFunction import AjaxFunction
from referral_system.models import SmsFac, Service, VoucherCode
import json
from django.db import connection



class ReferralFunctions:
    
    def generateUniqueID(self):
        lastVoucher = VoucherCode.objects.latest('unique_id')
        
        return self.returnNextId(lastVoucher.unique_id)
        
    def returnNextId(self,_currentID):
        number = int(_currentID[1:])
        number += 1
        number = str(number)
        idString = self.returnIDString(number)
        
        return self.insertedUniqueID(idString)
        
    def insertedUniqueID(self, idString):
        #check if exist
        if VoucherCode.objects.filter(unique_id=idString):
            return self.returnNextId(idString)
        else:
            voucherCode = VoucherCode(unique_id = idString)
            voucherCode.save()
            return idString
        
        
        
    
    def returnIDString(self, number):
        numberLength = len(number)
        numberOfZero = 6 - numberLength
        idString = 'A'
        for x in range(0, numberOfZero):
            idString = idString + '0'
        
        idString = idString + number
        
        return idString
        
        
        