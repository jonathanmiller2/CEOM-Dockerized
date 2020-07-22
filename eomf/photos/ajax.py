import json
import os
from dajaxice.decorators import dajaxice_register

from django.conf import settings

from sorl.thumbnail import get_thumbnail

@dajaxice_register(method='GET',name='photos.get_thumbnail')
def get_task_progress(request,image_id,resolution):
    try:
        photo = Photo.objects.get(id=image_id)
        available_resolutions = ['100x100','300x300']
        if resolution not in available_resolutions:
            return json.dumps({'success':False,'message':'Resolution not supported: %s' % e.message})
        im = get_thumbnail(photo.file.name, resolution, crop='center', quality=95)
        return  json.dumps({'failure':True,'imageUrl':str(im)})
    except Exception, e:
        return json.dumps({'failure':False,'message':'Error: %s' % e.message})

def __test__():
    print 'OK'

def __test__():
    print 'OK'
