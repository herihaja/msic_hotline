from  django.db import connection


class AjaxFunction:
    
    @staticmethod
    def listFacilityProvince():
        listProvince = AjaxFunction.runSQL('''
        SELECT
        distinct
        quest_16 AS parent,
        quest_16 AS province,
        quest_42 AS province_khmer 
        FROM
        sms_fac
        GROUP BY quest_16, quest_42
        ''')
        return listProvince
    
    @staticmethod    
    def listFacilityDistrict( _province):
        listDistrict = AjaxFunction.runSQL('''
        SELECT
        distinct
        quest_16 AS parent,
        quest_31 AS district,
        quest_48 AS district_khmer  
        FROM
        sms_fac
        WHERE quest_16 LIKE \'''' + _province + '''\'
        ''')
        
        return listDistrict
    
    @staticmethod    
    def listFacilityVillage( _district, _province):
        listVillage = AjaxFunction.runSQL('''
        SELECT
        distinct
        quest_31 AS parent,
        quest_19 AS village,
        quest_44 AS village_khmer 
        FROM
        sms_fac
        WHERE quest_31 LIKE \'''' + _district + '''\'
        AND quest_16 LIKE \'''' + _province + '''\'  
        ''')
        
        return listVillage
    
    @staticmethod
    def listLocalityProvince():
        listProvince = AjaxFunction.runSQL('''
        SELECT
        distinct
        quest_6 AS parent,
        quest_6 AS province,
        quest_1 AS province_khmer  
        FROM
        sms_loc
        ORDER BY quest_6 ASC
        ''')
        return listProvince
    
    @staticmethod    
    def listLocalityDistrict( _province):
        listDistrict = AjaxFunction.runSQL('''
        SELECT
        distinct
        quest_6 AS parent,
        quest_4 AS district,
        quest_8 AS district_khmer 
        FROM
        sms_loc
        WHERE 
        quest_6 LIKE \'''' + _province + '''\'
        ORDER BY quest_4 ASC
        ''')
        
        return listDistrict
    
    @staticmethod    
    def listLocalityCommune( _district, _province):
        listCommune = AjaxFunction.runSQL('''
        SELECT
        distinct
        quest_4 AS parent,
        quest_9 AS commune,
        quest_2 AS commune_khmer 
        FROM
        sms_loc
        WHERE 
        quest_6 LIKE \'''' + _province + '''\' AND 
        quest_4 LIKE \'''' + _district + '''\'
        ORDER BY quest_9 ASC
        ''')
        
        return listCommune
    
    @staticmethod    
    def listLocalityVillage(_commune, _district, _province):
        listVillage = AjaxFunction.runSQL('''
        SELECT
        distinct
        quest_9 AS parent,
        quest_3 AS village,
        quest_7 AS village_khmer 
        FROM
        sms_loc
        WHERE
        quest_9 LIKE \'''' + _commune + '''\' AND  
        quest_6 LIKE \'''' + _province + '''\' AND 
        quest_4 LIKE \'''' + _district + '''\'
        ORDER BY quest_3 ASC
        ''')
        
        return listVillage
    
    @staticmethod    
    def runSQL( _sql):
        cursor = connection.cursor()
        cursor.execute(_sql)
        row = AjaxFunction.dictfetchall(cursor) #cursor.fetchall()
        return row
    
    @staticmethod
    def dictfetchall (cursor):
        "Return all rows from a cursor as a dict"
        columns = [col[0] for col in cursor.description]
        return [
                dict(zip(columns, row))
                for row in cursor.fetchall()
                ]