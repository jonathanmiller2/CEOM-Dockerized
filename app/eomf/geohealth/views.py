from django.template import Context, RequestContext, loader
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.files.base import ContentFile
from eomf.geohealth.models import Datainfo, Datatype
import numpy, math
import os, re, datetime, glob, sys

def down(request):
    return HttpResponse("Temporarily offline")

def index(request):
    #ds = Datainfo.objects.order_by('label','order').all()
    ds = Datainfo.objects.order_by('order', 'label').all()
    return render(request, 'geohealth/gemap.html', context={
        'content': "This is a map",
        'datasets': ds,
        'kml_path': request.path+'kml/',
        'kml_ext': ".kmz",
    })

def indices_kml(request):
    timespans = []
    for y in range(2002,2003):
        for d in range(1,96,8):
            time = datetime.date(y,1,1) + datetime.timedelta(d-1)
            timespans.append({'layers':"TOP%2CBOT%2Cocean_mask",
                             'params':"year=%d&day=%d&prod=evi"%(y,d),
                             'begin':time,
                             'end':time+datetime.timedelta(d+6) })
    
    #test = points[0].kml
    return render(request, 'kml/wrap_wms_time.kml', context={'timespans' : timespans, 'host':request.META['HTTP_HOST']}, mimetype="application/vnd.google-earth.kml+xml")


def evi_kml(request):
    timespans = []
    for y in range(2002,2003):
        for d in range(1,96,8):
            time = datetime.date(y,1,1) + datetime.timedelta(d-1)
            timespans.append({'layers':"TOP%2CBOT%2Cocean_mask",
                             'params':"year=%d&day=%d&prod=evi"%(y,d),
                             'begin':time,
                             'end':time+datetime.timedelta(d+6) })
    
    #test = points[0].kml
    return render(request, 'kml/wrap_wms_time.kml', context={'timespans' : timespans, 'host':request.META['HTTP_HOST']}, mimetype = "application/vnd.google-earth.kml+xml")


def kml(request, name):
    import eomf.geohealth.models as maps

    d = Datainfo.objects.get(name=name)
    
    if d.datatype.name == 'wms':
        service = ""
        if ':' in name:
            service, name = name.split(':')
            
        t = 'kml/wrap_wms.kml'
        c = {'service':service, 'layer': name }
        
    elif d.datatype.name == 'url':
        t = 'kml/wrap_url.kml'
        c = {'url': d.source }
        
    elif d.datatype.name == 'file':
        t = 'kml/'+d.source
        c = None
        
    elif d.datatype.name == 'object':
        targetModel = getattr(maps, d.source)
        objects = targetModel.objects.kml()
        
        try:
            styles = targetModel().styles()
        except AttributeError:
            styles = [{'name':'default', 'color':'8800ff00', 'icon':'http://maps.google.com/mapfiles/kml/shapes/info.png'}]
            
        t = 'kml/main.kml'
        c = {
            'styles':styles,
            'geometries':objects,
        }
        
    elif d.datatype.name == 'function':

        targetFunction = getattr(maps, d.source)
        objects, styles = targetFunction()
        
        if styles is None:
            styles = [{'name':'default', 'color':'8800ff00', 'icon':'http://maps.google.com/mapfiles/kml/shapes/info.png'}]
            
        t = 'kml/main.kml'
        c = {
            'styles':styles,
            'geometries':objects,
        }
        
    else:
        pass
            
    return render(request, t, context=c, mimetype="application/vnd.google-earth.kml+xml")    

