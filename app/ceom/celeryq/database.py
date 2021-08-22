import psycopg2

class pgDatabase:

    dbname = 'ceom'
    user = 'ceom'
    host = 'db'
    password = '30mfadmin'

    def __init__(self):
        try:
            self.conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'"%(self.dbname,self.user,self.host,self.password))
        except Exception as e :
            print(("Error: %s" % e.message))
            raise Exception("Unnable to connect to database")

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