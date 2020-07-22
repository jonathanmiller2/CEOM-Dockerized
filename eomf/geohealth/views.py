from django.template import Context, RequestContext, loader
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.core.files.base import ContentFile
from models import Datainfo, Datatype
import numpy, math
import os, re, datetime, glob, sys

def down(request):
    return HttpResponse("Temporarily offline")

def index(request):
    #ds = Datainfo.objects.order_by('label','order').all()
    ds = Datainfo.objects.order_by('order', 'label').all()
    t = loader.get_template('geohealth/gemap.html')
    c = RequestContext(request,{
        'content': "This is a map",
        'datasets': ds,
        'kml_path': request.path+'kml/',
        'kml_ext': ".kmz",
    })
    return HttpResponse(t.render(c))

def indices_kml(request):
    timespans = []
    for y in xrange(2002,2003):
        for d in xrange(1,96,8):
            time = datetime.date(y,1,1) + datetime.timedelta(d-1)
            timespans.append({'layers':"TOP%2CBOT%2Cocean_mask",
                             'params':"year=%d&day=%d&prod=evi"%(y,d),
                             'begin':time,
                             'end':time+datetime.timedelta(d+6) })
    
    #test = points[0].kml
    return render_to_response('kml/wrap_wms_time.kml',{'timespans' : timespans, 'host':request.META['HTTP_HOST']},
        mimetype = "application/vnd.google-earth.kml+xml")


def evi_kml(request):
    timespans = []
    for y in xrange(2002,2003):
        for d in xrange(1,96,8):
            time = datetime.date(y,1,1) + datetime.timedelta(d-1)
            timespans.append({'layers':"TOP%2CBOT%2Cocean_mask",
                             'params':"year=%d&day=%d&prod=evi"%(y,d),
                             'begin':time,
                             'end':time+datetime.timedelta(d+6) })
    
    #test = points[0].kml
    return render_to_response('kml/wrap_wms_time.kml',{'timespans' : timespans, 'host':request.META['HTTP_HOST']},
        mimetype = "application/vnd.google-earth.kml+xml")


def kml(request, name):
    import eomf.geohealth.models as maps

    d = Datainfo.objects.get(name=name)
    
    if d.datatype.name == 'wms':
        service = ""
        if ':' in name:
            service, name = name.split(':')
            
        t = loader.get_template('kml/wrap_wms.kml')
        c = RequestContext(request,{'service':service, 'layer': name })
        
    elif d.datatype.name == 'url':
        t = loader.get_template('kml/wrap_url.kml')
        c = RequestContext(request, {'url': d.source })
        
    elif d.datatype.name == 'file':
        t = loader.get_template('kml/'+d.source)
        c = RequestContext(request)
        
    elif d.datatype.name == 'object':
        targetModel = getattr(maps, d.source)
        objects = targetModel.objects.kml()
        
        try:
            styles = targetModel().styles()
        except AttributeError:
            styles = [{'name':'default', 'color':'8800ff00', 'icon':'http://maps.google.com/mapfiles/kml/shapes/info.png'}]
            
        t = loader.get_template('kml/main.kml')
        c = RequestContext(request,{
            'styles':styles,
            'geometries':objects,
        })
        
    elif d.datatype.name == 'function':

        targetFunction = getattr(maps, d.source)
        objects, styles = targetFunction()
        
        if styles is None:
            styles = [{'name':'default', 'color':'8800ff00', 'icon':'http://maps.google.com/mapfiles/kml/shapes/info.png'}]
            
        t = loader.get_template('kml/main.kml')
        c = RequestContext(request,{
            'styles':styles,
            'geometries':objects,
        })
        
    else:
        pass
            
    return HttpResponse(t.render(c), mimetype="application/vnd.google-earth.kml+xml")    

