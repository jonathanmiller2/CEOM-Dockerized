import psycopg2
import os

class pgDatabase:

    dbname = os.environ.get("SQL_DATABASE", default="ceom"),
    user = os.environ.get("SQL_USER", default="ceom"),
    host = os.environ.get("SQL_HOST", default="db"),
    password = os.environ.get("SQL_PASSWORD", default="password"),

    def __init__(self):
        try:
            self.conn = psycopg2.connect(f"dbname='{self.dbname[0]}' user='{self.user[0]}' host='{self.host[0]}' password='{self.password[0]}'")
        except Exception as e :
            print(e)
            raise Exception("Unable to connect to database")

        self.cur = self.conn.cursor()

    def execute(self, query):
        try:
            self.cur.execute(query)
        except:
            raise Exception("Error with query: %s"%query)
        self.conn.commit()
        self.cur.close()

    def updateCompletedSingleTimeSeriestask(self,task_id,result):
        try:
            sql = '''UPDATE visualization_singletimeseriesjob set result='%s', completed=True WHERE task_id='%s'; ''' % (result,task_id)
            self.execute(sql)
        except Exception as e:
            print(("Error with query:" + sql))
            raise Exception("Error msg: %s" % str(e))
            pass
    def updateMultipleSiteTimeSeries(self,task_id,result,message,progress,total_sites,completed,error,working):
        try:
            sql = '''UPDATE visualization_timeseriesjob 
                     SET result='%s',message='%s',progress=%d,total_sites=%d,
                         completed=%s, error=%s,working=%s 
                     WHERE task_id='%s'; 
            ''' % (result,message,progress,total_sites,completed,error,working,task_id)
            self.execute(sql)
        except Exception as e:
            print(("Error with query:" + sql))
            raise Exception("Error msg: %s" % str(e))
            pass

if __name__ == '__main__':
    #test
    db = pgDatabase()
    # db.updateCompletedSingleTimeSeriestask('3965d349-f05b-4f2b-8ae3-4da022710b0a','/test/')