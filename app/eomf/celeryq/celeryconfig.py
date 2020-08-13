BROKER_URL='redis://redis:6379/0'
#CELERY_RESULT_BACKEND = 'amqp://rose:rosepasswordq@mangrove.rccc.ou.edu:5672/eomf_processing'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
#CELERY_MONGODB_BACKEND_SETTINGS = {
#    "host": "mangrove.rccc.ou.edu",
#    "user": 'rose',
#    "password": 'rosepasswordq',
#    "port": 27017,
#    "database": "eomf_processing",
#    "taskmeta_collection": "celery_results" # Collection name to use for task output
#}
CELERY_TASK_RESULT_EXPIRES = 300  # 5 minutes.
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT=['json']
CELERY_TIMEZONE = 'US/Central'
CELERY_ENABLE_UTC = True
CELERY_ROUTES = {
    'tasks.get_modis_raw_data':   {'queue': 'control'},
    'tasks.get_modis_year_data':   {'queue': 'processing'},
}
#from kombu import serialization
# serialization.registry._decoders.pop("application/x-python-serialize")

