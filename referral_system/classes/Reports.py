from referral_system.classes.AjaxFunction import AjaxFunction
import requests
from django.conf import settings
import json
from datetime import datetime
from referral_system.models import MessagesLog


class Reports:
    
    def clientsPerStatus(self, date_period = '', province = '', id_referrer = ''):
        
        tDatePeriod = date_period.split("-") #2015-10
        
        sqlReport = """ 
        SELECT 
        DISTINCT ro.status ,
        count(a.referral_id) AS number_client
        FROM    appointment a 
        INNER JOIN
        (
            SELECT  referral_id,
                    MAX(id) max_id
            FROM    referral_operation
            GROUP BY referral_id
        ) MaxId ON a.referral_id = MaxId.referral_id 
        INNER JOIN client cli ON cli.id_client = a.id_client
        INNER JOIN referral_operation ro 
        ON   MaxId.referral_id = ro.referral_id AND MaxId.max_id = ro.id 
        
        WHERE 1 = 1 
        """
        
        if date_period != '':
            sqlReport += " AND EXTRACT(MONTH FROM a.referral_date) = " + str(int(tDatePeriod[1]))
            sqlReport += " AND EXTRACT(YEAR FROM a.referral_date)  = " + tDatePeriod[0]
            
        if province != '':
            sqlReport += " AND cli.adr_province = '" + province + "' "
            
        if id_referrer != '':
            sqlReport += " AND ro.actor_id = '" + id_referrer + "' "
            
        sqlReport += "GROUP BY ro.status"
                    
        return AjaxFunction.runSQL(sqlReport)
    
    def servicesDelivered(self, date_period = '', province = '', id_referrer = ''):
        
        tDatePeriod = date_period.split("-") #2015-10-05 
        
        sqlReport = """ 
        SELECT 
        ro.referred_services
        FROM    
        referral_operation ro
        INNER JOIN appointment a ON a.referral_id = ro.referral_id 
        INNER JOIN client cli ON cli.id_client = a.id_client
        WHERE status = 2
        """
        if date_period != '':
            sqlReport += " AND EXTRACT(MONTH FROM a.referral_date) = " + str(int(tDatePeriod[1]))
            sqlReport += " AND EXTRACT(YEAR FROM a.referral_date)  = " + tDatePeriod[0]
            
        if province != '':
            sqlReport += " AND cli.adr_province = '" + province + "' "
            
        if id_referrer != '':
            sqlReport += " AND ro.actor_id = '" + id_referrer + "' "
                    
        return AjaxFunction.runSQL(sqlReport)
    
    def smsTextNewReferral(self, referralId, actorId):
        # <Health facility name>, <house #>, <street>, <village>, 
        # <commune>, telephone number-<code> <expiry date>
        
        sqlSms = """ 
        SELECT 
        facility.quest_19 AS facility_name,
        cli.adr_street,
        cli.id_client,
        cli.adr_street AS adr_street_khmer,
        cli.adr_village,
        CASE WHEN loc_village.quest_7 IS NULL THEN '' ELSE loc_village.quest_7 END AS adr_village_khmer,
        cli.adr_commune,
        CASE WHEN loc_commune.quest_2 IS NULL THEN '' ELSE loc_commune.quest_2 END AS adr_commune_khmer,
        cli.phone,
        facility.quest_12 AS facility_name_khmer,
        app.expiry_date,
        app.language AS ref_lang
        FROM 
        appointment app
        INNER JOIN sms_fac facility ON  facility.quest_20 = app.id_facility
        INNER JOIN client cli ON cli.id_client = app.id_client
        LEFT JOIN sms_loc loc_village ON loc_village.quest_3 = cli.adr_village
        LEFT JOIN sms_loc loc_commune ON loc_commune.quest_9 = cli.adr_commune
        WHERE 
        app.referral_id = '""" + referralId + """'
        """
        
        resSms = AjaxFunction.runSQL(sqlSms)
        objSms = resSms[0]
        
        strSms = "The sms below is sent to the client: <br><br><i>\""
        
        sms = ''
        if objSms['ref_lang'] == 'english':
            sms = sms + str(objSms['facility_name'])
            sms = sms + ", " + str(objSms['adr_street'])
            sms = sms + ", " + str(objSms['adr_village'])
            sms = sms + ", " + str(objSms['adr_commune'] )                   
        else:
            sms = sms + objSms['facility_name_khmer']
            sms = sms + ", " + objSms['adr_street']
            sms = sms + ", " + objSms['adr_village_khmer']
            sms = sms + ", " + objSms['adr_commune_khmer']
        
        sms = sms + ", " + str(objSms['phone'])    
        sms = sms + ", " + str(objSms['expiry_date'])
        strSms = strSms + " " + sms + "</i>\""
        
        if objSms['ref_lang'] == 'english':
            self.sendMessage("261340341893", sms, actorId, objSms['id_client'])
        #    self.sendMessage(objSms['phone'], sms, actorId, objSms['id_client'])
        #else:
        #    self.sendMessage(objSms['phone'], sms, actorId, objSms['id_client'])
        
        
        
        return strSms
    
    def sendMessage(self, toNumber, message_content, actorId, recipientId):
        # number_list = [ num1, num2, ...]
        # message_content <= 160 car
        # discussion_id : for log
        
        corrected_list = self.set_as_valid_list(toNumber)
        data_dict = {}
        data_dict['numbers'] = corrected_list['string']
        data_dict['message'] = message_content
        
        data_string = '{"numbers":[%s],"message":"%s "}' %(corrected_list['string'], message_content.encode("cp874"))
        data_direct = '{"numbers":' + corrected_list['string'] + ',"message":"' + message_content.encode("UTF-8") + '"}'
        
        headers = {'Content-Type': 'Content-Type: text/html; charset=UTF-8'}
        ssl_verify = False
        response = requests.post(settings.DW_SMS_API_URL,
                                 verify=ssl_verify,
                                 data=data_string)
        
        self.saveSmsLog(response, toNumber, message_content.encode("UTF-8"), actorId, recipientId)
        
        return response
    
    def set_as_valid_list (self, number_string_list):
        # number_string_list may be like 261xxxx, 261xxx
        # hard correct to "261xxxx", "261xxx" 
        number_list = [n.strip() for n in number_string_list.split(",")] #remove "spaces" 
        cl =  '", "'.join(map(str, number_list))
        return {'string' : '"' + cl + '"',
            'list' : number_list}
        
    def saveSmsLog(self, response, to_number, msg_content, actor_id, recipient_id):        
        response_status = response.status_code
        
        if response.status_code == requests.codes.ok:# status_code=200
            msg_status = "%s, %s" %(response_status, response.json()[str(to_number)])
        else:
            msg_status = response_status
        
        msg = MessagesLog(
                                  status = msg_status,
                                  content_sms = msg_content,
                                  from_number = '',
                                  to_number = to_number,
                                  id_actor = actor_id,
                                  id_recipient = recipient_id
                                  )
        msg.save()
        
        