from referral_system.classes.AjaxFunction import AjaxFunction


class Reports:
    
    def clientsPerStatus(self):
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
        INNER JOIN referral_operation ro 
        ON   MaxId.referral_id = ro.referral_id AND MaxId.max_id = ro.id 
        GROUP BY ro.status
        """
                    
        return AjaxFunction.runSQL(sqlReport)
    
    def servicesDelivered(self):
        sqlReport = """ 
        SELECT 
        referred_services
        FROM    
        referral_operation 
        WHERE status = 2
        """
                    
        return AjaxFunction.runSQL(sqlReport)
    
    def smsTextNewReferral(self, referralId):
        # <Health facility name>, <house #>, <street>, <village>, 
        # <commune>, telephone number-<code> <expiry date>
        
        sqlSms = """ 
        SELECT 
        facility.quest_19 AS facility_name,
        cli.adr_street,
        cli.adr_village,
        cli.adr_commune,
        cli.phone,
        app.expiry_date
        FROM 
        appointment app
        INNER JOIN sms_fac facility ON  facility.quest_20 = app.id_facility
        INNER JOIN client cli ON cli.id_client = app.id_client
        WHERE 
        app.referral_id = '""" + referralId + """'
        """
        
        resSms = AjaxFunction.runSQL(sqlSms)
        objSms = resSms[0]
        
        strSms = "The sms below is sent to the client: "
        strSms = strSms + objSms['facility_name']
        strSms = strSms + ", " +objSms['adr_street']
        strSms = strSms + ", " +objSms['adr_village']
        strSms = strSms + ", " +objSms['adr_commune']
        strSms = strSms + ", " +objSms['phone']
        strSms = strSms + ", " + str(objSms['expiry_date'])
        
        return strSms