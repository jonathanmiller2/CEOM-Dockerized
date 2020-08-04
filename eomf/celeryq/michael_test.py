from celery import task
from celery import Celery

#app = Celery('micahel_test', broker='amqp://')
app = Celery('micahel_test', backend='amqp', broker='amqp://')
app.config_from_object('celeryconfig_copy')

@app.task(bind=True)
def function_test(self):
    print "Hi from test!"
    return "Hi from test!"
