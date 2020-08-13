from pymongo import MongoClient
import datetime
uri = "mongodb://rose:rosepasswordq@mangrove.rccc.ou.edu/eomf_processing?authMechanism=MONGODB-CR"
client = MongoClient(uri)
# in seconds
EXPIRATION_TIME=0 
db = client.eomf_processing
query = db.celery_results.find( {'date_done': {"$lt": datetime.datetime.utcnow()-datetime.timedelta(seconds=EXPIRATION_TIME)}})
# print len(query.items())
print query[0]
# print query.retrieved