import json
import os
from dajaxice.decorators import dajaxice_register

from models import SingleTimeSeriesJob, TimeSeriesJob
from celery.result import AsyncResult
from django.db.models import Q
from django.conf import settings

ERROR_NOT_EXIST_MESSAGE = 'Could not retrieve task. It may not exist or may have expired.'
FAILURE_MESSAGE = 'We are sorry, but an error occured while processing the task. Please contact the administrator.'
PENDING_MESSAGE = 'Waiting in queue... (If it takes too long please contact the administrator)'
PROCESSING_MESAGE = 'Processing...'

@dajaxice_register(method='GET',name='visualization.get_task_progress')
def get_task_progress(request,task_id):
    try:
        task_db = SingleTimeSeriesJob.objects.get(task_id=task_id)
        if not task_db.completed:
            task = AsyncResult(str(task_id))
            if task.result is None:
                return json.dumps({'not_found':True,'message':ERROR_NOT_EXIST_MESSAGE})
            if task.status==u"FAILURE":
                return json.dumps({'failure':True,'message':FAILURE_MESSAGE})
            elif task.status==u"STARTED":
                # Task is still running
                data = json.dumps({
                    'progress':True,
                    'completed':task.result['completed'],
                    'errors': task.result['error'],
                    'total':task.result['total'],
                    'message': PROCESSING_MESAGE,
                    })
                return data
        else:
            return json.dumps({
                'success':True, 
                'url': str(task_db.result),
                })
    except Exception, e:
        return json.dumps({'failure':True,'message':'Unhandled exception: %s' % e.message})

def __test__():
    print 'OK'

@dajaxice_register(method='GET',name='visualization.get_multiple_task_progress')
def get_multiple_task_progress(request,tasks_ids):
    try:
        if not tasks_ids:
            raise Exception('Task List is empty')
        tasks = TimeSeriesJob.objects.filter(Q(user=request.user)&Q(reduce(lambda x, y: x | y, [Q(id__contains=task_id) for task_id in tasks_ids])))
        tasks_dict = [(t.toJSON()) for t in tasks]
        return json.dumps({'tasks':tasks_dict,'success':True})
    except Exception, e:
        return json.dumps({'success':False,'message':'Unhandled exception: %s' % e.message})

def __test__():
    print 'OK'
