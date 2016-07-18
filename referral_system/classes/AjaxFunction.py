from  django.db import connection


class AjaxFunction:
    
    @staticmethod
    def listFacilityProvince():
        listProvince = AjaxFunction.runSQL('''
        SELECT
        distinct
        quest_16 AS parent,
        quest_16 AS province 
        FROM
        sms_fac
        GROUP BY quest_16
        ''')
        return listProvince
    
    @staticmethod    
    def listFacilityDistrict( _province):
        listDistrict = AjaxFunction.runSQL('''
        SELECT
        distinct
        quest_16 AS parent,
        quest_31 AS district 
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
        quest_44 AS village 
        FROM
        sms_fac
        WHERE quest_31 LIKE \'''' + _district + '''\'
        AND quest_16 LIKE \'''' + _province + '''\'  
        ''')
        
        return listVillage
    
    @staticmethod
    def listGarmentProvince():
        listProvince = AjaxFunction.runSQL('''
        SELECT
        distinct
        quest_16 AS parent,
        quest_16 AS province 
        FROM
        sms_fac
        WHERE quest_22 LIKE 'Garment factory infirmary'
        GROUP BY quest_16
        ''')
        return listProvince
    
    @staticmethod    
    def listGarmentDistrict( _province):
        listDistrict = AjaxFunction.runSQL('''
        SELECT
        distinct
        quest_16 AS parent,
        quest_31 AS district 
        FROM
        sms_fac
        WHERE 
        quest_22 LIKE 'Garment factory infirmary' AND 
        quest_16 LIKE \'''' + _province + '''\'
        ''')
        
        return listDistrict
    
    @staticmethod    
    def listGarmentVillage( _district, _province):
        listVillage = AjaxFunction.runSQL('''
        SELECT
        distinct
        quest_31 AS parent,
        quest_44 AS village 
        FROM
        sms_fac
        WHERE
        quest_22 LIKE 'Garment factory infirmary' AND  
        quest_16 LIKE \'''' + _province + '''\' AND 
        quest_31 LIKE \'''' + _district + '''\'
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