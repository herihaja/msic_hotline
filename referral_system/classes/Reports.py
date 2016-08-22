from referral_system.classes.AjaxFunction import AjaxFunction


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
    
    def smsTextNewReferral(self, referralId):
        # <Health facility name>, <house #>, <street>, <village>, 
        # <commune>, telephone number-<code> <expiry date>
        
        sqlSms = """ 
        SELECT 
        facility.quest_19 AS facility_name,
        cli.adr_street,
        cli.adr_street AS adr_street_khmer,
        cli.adr_village,
        loc_village.quest_7 AS adr_village_khmer,
        cli.adr_commune,
        loc_commune.quest_2 AS adr_commune_khmer,
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
        
        if objSms['ref_lang'] == 'english':
            strSms = strSms + objSms['facility_name']
            strSms = strSms + ", " +objSms['adr_street']
            strSms = strSms + ", " +objSms['adr_village']
            strSms = strSms + ", " +objSms['adr_commune']                    
        else:
            strSms = strSms + objSms['facility_name_khmer']
            strSms = strSms + ", " +objSms['adr_street']
            strSms = strSms + ", " +objSms['adr_village_khmer']
            strSms = strSms + ", " +objSms['adr_commune_khmer']
        
        strSms = strSms + ", " +objSms['phone']    
        strSms = strSms + ", " + str(objSms['expiry_date'])
        strSms = strSms + "</i>\""
        
        return strSms