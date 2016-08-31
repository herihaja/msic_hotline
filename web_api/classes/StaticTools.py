from  django.db import connection


class StaticTools:

    @staticmethod
    def run_sql( _sql):
        cursor = connection.cursor()
        cursor.execute(_sql)
        row = StaticTools.dict_fetch_all(cursor) #cursor.fetchall()
        return row

    @staticmethod
    def dict_fetch_all (cursor):
        "Return all rows from a cursor as a dict"
        columns = [col[0] for col in cursor.description]
        return [
                dict(zip(columns, row))
                for row in cursor.fetchall()
                ]


  