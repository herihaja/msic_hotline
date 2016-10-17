from referral_system.classes.AjaxFunction import AjaxFunction
import requests
from django.conf import settings
import json, urlparse
from datetime import datetime
from referral_system.models import MessagesLog


class Reports:
    
    def clientsPerStatus(self, start_date='', end_date = '', province = '', id_referrer = '', referrer_type=''):
        
        start_date = self.validate_date(start_date)
        end_date = self.validate_date(end_date)
        
        sqlReport = """ 
        SELECT 
        DISTINCT status ,
        count(referral_id) AS number_client
        FROM (SELECT
                CASE
                        WHEN ro.status = 1 and a.expiry_date > CURRENT_DATE THEN 5
                        ELSE ro.status END
                     as status,
                    a.referral_id,
                    a.referral_date,
                    a.id_client,
                    ro.actor_id
                FROM  appointment a
        INNER JOIN
        (
            SELECT  referral_id,
                    MAX(id) max_id
            FROM    referral_operation
            GROUP BY referral_id
        ) MaxId ON a.referral_id = MaxId.referral_id
        INNER JOIN referral_operation ro
        ON   MaxId.referral_id = ro.referral_id AND MaxId.max_id = ro.id
        ) as t
        INNER JOIN client cli ON cli.id_client = t.id_client
        WHERE 1 = 1
        
        """
        
        if start_date :
            sqlReport += " AND t.referral_date >= '%s' " % start_date

        if end_date :
            sqlReport += " AND t.referral_date <= '%s' " % end_date
            
        if province != '':
            sqlReport += " AND cli.adr_province = '" + province + "' "
            
        if id_referrer == 'all_counselors': #all hotline counsellor
            sqlReport += " AND t.actor_id IN (select u.id as actor_id FROM auth_user u inner join auth_user_groups ug on ug.authuser_id = u.id and ug.group_id = 1)"
        elif id_referrer != '' and str(int(id_referrer)) == id_referrer:
            sqlReport += " AND t.actor_id = '" + id_referrer + "' "

        dict_referrer_type = {'hotline_counselors': 1, 'hf': 3, 'garment_factory':2, "whc": 5}
        if referrer_type and dict_referrer_type.has_key(referrer_type):
            sqlReport += " AND t.actor_id IN (select u.id as actor_id FROM auth_user u inner join auth_user_groups " \
                + "ug on ug.authuser_id = u.id and ug.group_id = %d)" % dict_referrer_type.get(referrer_type)
            
        sqlReport += "GROUP BY t.status"
        return AjaxFunction.runSQL(sqlReport)
    
    def servicesDelivered(self, start_date='', end_date= '', province = '', id_referrer = '', referrer_type=''):
        
        start_date = self.validate_date(start_date)
        end_date = self.validate_date(end_date)
        
        sqlReport = """ 
        SELECT 
        ro.referred_services
        FROM    
        referral_operation ro
        INNER JOIN appointment a ON a.referral_id = ro.referral_id 
        INNER JOIN client cli ON cli.id_client = a.id_client
        WHERE status = 2
        """

        if start_date:
            sqlReport += " and a.referral_date >= '%s'" % start_date

        if end_date:
            sqlReport += " and a.referral_date <= '%s'" % end_date

        if province != '':
            sqlReport += " AND cli.adr_province = '" + province + "' "
            
        if id_referrer == 'all_counselors':
            sqlReport += " AND ro.actor_id IN (select u.id as actor_id FROM auth_user u inner join auth_user_groups" + \
                         " ug on ug.authuser_id = u.id and ug.group_id = 1)"
        elif id_referrer != '' and str(int(id_referrer)) == id_referrer:
            sqlReport += " AND ro.actor_id = '" + id_referrer + "' "

        dict_referrer_type = {'hotline_counselors': 1, 'hf': 3, 'garment_factory':2, "whc": 5}
        if referrer_type and dict_referrer_type.has_key(referrer_type):
            sqlReport += " AND ro.actor_id IN (select u.id as actor_id FROM auth_user u inner join auth_user_groups" + \
                         " ug on ug.authuser_id = u.id and ug.group_id = %d)" % dict_referrer_type.get(referrer_type)

        return AjaxFunction.runSQL(sqlReport)
    
    def smsTextNewReferral(self, referralId, actorId):
        # <Health facility name>, <house #>, <street>, <village>, 
        # <commune>, telephone number-<code> <expiry date>
        
        sqlSms = """
            SELECT
            facility.quest_19 AS facility_name,
            cli.adr_street,
            cli.id_client,
            cli.phone as client_phone,
            facility.quest_18 as adr_village,
            facility.quest_43 as adr_village_khmer,
            facility.quest_13 as adr_commune,
            facility.quest_39 as adr_commune_khmer,
            facility.quest_33 as house_number,
            facility.quest_16 as adr_street,
            facility.quest_34 as adr_street_khmer,
            CASE WHEN loc_village.quest_7 IS NULL THEN '' ELSE loc_village.quest_7 END AS client_adr_village_khmer,
            cli.adr_commune as client_adr_commune,
            CASE WHEN loc_commune.quest_2 IS NULL THEN '' ELSE loc_commune.quest_2 END AS client_adr_commune_khmer,
            facility.quest_26 as phone,
            facility.quest_12 AS facility_name_khmer,
            app.expiry_date,
            app.language AS ref_lang,
            op.referral_id
            FROM
            appointment app
            INNER JOIN referral_operation op ON op.referral_id = app.referral_id and op.status = 1
            INNER JOIN sms_fac facility ON  facility.quest_20 = op.facility_id
            INNER JOIN client cli ON cli.id_client = app.id_client
            LEFT JOIN sms_loc loc_village ON loc_village.quest_3 = cli.adr_village
            LEFT JOIN sms_loc loc_commune ON loc_commune.quest_9 = cli.adr_commune
            WHERE
            app.referral_id = '""" + referralId + """'
        """""

        resSms = AjaxFunction.runSQL(sqlSms)
        objSms = resSms[0]
        
        strSms = "The SMS below was sent to the client: <br><br><i>\""
        
        if objSms['ref_lang'] == 'english':
            sms = unicode(objSms["facility_name"])
            sms += self.cleanSmsContent(objSms["house_number"])
            sms += self.cleanSmsContent(objSms["adr_street"])
            sms += self.cleanSmsContent(objSms["adr_village"])
        else:
            sms = objSms["facility_name_khmer"]
            sms += self.cleanSmsContent(objSms["house_number"])
            sms += self.cleanSmsContent(objSms["adr_street_khmer"])
            sms += self.cleanSmsContent(objSms["adr_village_khmer"])

        sms += self.cleanSmsContent(objSms["phone"])
        sms += self.cleanSmsContent(objSms["expiry_date"])
        sms += self.cleanSmsContent(objSms["referral_id"])
        strSms = strSms + sms + "</i>\""

        message_content, status = self.sendMessage(objSms['client_phone'], sms, actorId, objSms['id_client'], objSms['ref_lang'])
        return strSms,status
    
    def cleanSmsContent(self, input):
        if len(unicode(input)) == 0 or input == 'n/a':
            return ''
        return ", %s" % unicode(input)

    def sendMessage(self, toNumber, message_content, actorId, recipientId, language="english"):
        # number_list = [ num1, num2, ...]
        # message_content <= 160 car
        # discussion_id : for log

        if toNumber[0] == "0":
            toNumber = "855%s" % toNumber[1:]
        
        if language == 'english':
            data_string_sample = "gw-text=%s&gw-username=mscambodia&gw-password=msckh2016&gw-from=mariestopes&gw-to=%s"
            conversion_method = english_conversion
        else:
            data_string_sample = "gw-coding=3&gw-text=%s&gw-username=mscambodia&gw-password=msckh2016&gw-from=mariestopes&gw-to=%s"
            conversion_method = khmer_conversion

        data_string = data_string_sample % (conversion_method(message_content), toNumber)
        response = requests.post(settings.SMS_API_URL, verify=False, data=data_string)

        status = self.saveSmsLog(response, toNumber, message_content.encode("UTF-8"), actorId, recipientId)
        return message_content, status

        
    def saveSmsLog(self, response, to_number, msg_content, actor_id, recipient_id):
        query_string = urlparse.parse_qs(response.content)
        if query_string.get('status')[0] == '0':
            msg_status = "Success: %s" % query_string.get('msgid')[0]
        else:
            msg_status = query_string.get('err_msg')[0]

        msg = MessagesLog(
                                  status = msg_status,
                                  content_sms = msg_content,
                                  from_number = 'mariestopes',
                                  to_number = to_number,
                                  id_actor = actor_id,
                                  id_recipient = recipient_id
                                  )
        msg.save()
        return query_string.get('status')[0] == '0'

    def validate_date(self, date_text):
        try:
            datetime.strptime(date_text, '%Y-%m-%d')
            return date_text
        except Exception:
            return ''
        

def english_conversion(input_text):
    return input_text

def khmer_conversion(input_text):
    output = ""
    for char in input_text:
        output += str("0x%0.4X" % ord(char))[2:]
    return output

