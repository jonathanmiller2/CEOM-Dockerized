from django.shortcuts import render
from django.template import Context, RequestContext, loader, Template
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.aggregates import Count
from django.db import connection, transaction
from django.contrib.gis.geos import GEOSGeometry, Polygon, Point
import json as simplejson 
import json

from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from django.core.files.base import ContentFile
from django.core.files import File
from django.shortcuts import redirect
from django.contrib.auth.models import User


from django.views.decorators.csrf import csrf_exempt
from django.template.defaultfilters import wordwrap
from django.db import connection


import datetime
from datetime import date
import itertools
import shutil
import os
import zlib, bz2, pickle, base64, pylzma, binascii


from pykml.factory import KML_ElementMaker as KML
from pykml import parser
from lxml import etree
from django.shortcuts import render
import numpy, math
from eomf.maps.models import roi, map_gallery, poi

from eomf.maps.forms import map_gallery_form, CommentForm, PoiForm, roiForm

from wsgiref.util import FileWrapper
import tempfile, zipfile

#simplekml

import simplekml
from eomf.photos.models import Category

# Create your views here.
def latlon2sin(lat,lon,modis='mod09a1',npix=2400.0):

    const =(36.*npix)/(2.*math.pi)
    folder = ''
    yg = 9.*npix - math.radians(const*lat)
    xg = math.radians(const*lon*math.cos(math.radians(lat))) + 18.*npix

    ih = int(xg/npix)
    iv = int(yg/npix)

    x = xg-ih*npix
    y = yg-iv*npix
 
    xi = int(x)
    yi = int(y)
    folder = u'h%02dv%02d' % (ih,iv) 
    return ih,iv,xi,yi,folder

def getuser(request):
    try:
        user = request.user
        if str(user) == "AnonymousUser":
            user = User.objects.get(username="bhargav018")
    except:
        print("exception raised")
    return user


def ROI(request):
    t = loader.get_template('maps/roi.html')
    c = RequestContext(request,{})
    if request.method == 'POST':
        # do something here
        # For now print the form back
        # return HttpResponse(json.dumps({'request':request.POST}))
        # x = request.POST
        # z3 = latlon2sin(float(x['longitude']),float(x['latitude']))
        # return HttpResponse(json.dumps({'request':request.POST, 'add':z3, 'user':str(request.user)}))
        # m = roi()
        # m.lon = float(x['longitude'])
        # m.lat = float(x['latitude'])
        # m.user =  getuser(request)
        # m.tile = str(x['Tile_selected'])
        # m.image = None # For now it is none.
        # m.score = 0
        # m.description = str(x['Description'])
        # m.classification = str(x['Classification'])
        # m.pixelsize = int(x['pixel'])
        # m.save()
        form = roiForm(request.POST)
        if form.is_valid():
            v = form.save(commit=False)
            v.user = getuser(request)
            v.save()
            xform = roiForm()
            c = RequestContext(request,{'form':xform,'success_roi':True})
            return HttpResponse(t.render(c))
        else:
            return HttpResponse("Something went wrong. Please contact the administrator.")
    else:
        form = roiForm()
        c = RequestContext(request,{'form':form})
        return HttpResponse(t.render(c))


def POI(request):
    t = loader.get_template('maps/poi.html')
    c = RequestContext(request,{})
    x_form = PoiForm()
    if request.method == 'POST':
        # do something here
        # For now print the form back
        # return HttpResponse(json.dumps({'request':request.POST}))
        form = PoiForm(request.POST)
        if form.is_valid():
            v = form.save(commit=False)
            v.user = getuser(request)
            v.save()
            xform = PoiForm()
            c = RequestContext(request,{'form':xform,'success_poi':True})
            return HttpResponse(t.render(c))
    else:
        c = RequestContext(request,{'form':x_form})
        return HttpResponse(t.render(c))


def VIEW_ROI(request):
    t = loader.get_template('maps/viewroi.html')
    roi_data = roi.objects.all() # sending all objects and rendering them to HTML
    classification = Category.objects.all().order_by('order')
    c = RequestContext(request,{'rois':roi_data, 'classif':classification})
    return HttpResponse(t.render(c))


def VIEW_POI(request):
    t = loader.get_template('maps/viewpoi.html')
    poi_data = poi.objects.all() # sending all objects and rendering them to HTML
    c = RequestContext(request,{'pois':poi_data,})
    return HttpResponse(t.render(c))


def VIEW_MAPS(request):
    t = loader.get_template('maps/map_gallery.html')
    maps = map_gallery.objects.all()
    c = RequestContext(request,{'maps':maps})
    return HttpResponse(t.render(c))

def DETAIL_MAP(request, id):
    t = loader.get_template('maps/detail_map.html')
    map_detail = map_gallery.objects.get(id=id)
    if request.method == 'POST':
        post_form = CommentForm(request.POST)
        if post_form.is_valid():
            v = post_form.save(commit=False)
            v.Comment_id = map_detail
            v.save()
            saved = True
        else:
            return HttpResponse("<b>Something wrong with the comment</b>")
    comment_form = CommentForm()
    comments = map_detail.comment.all()
    c = RequestContext(request,{'x':map_detail, 'form':comment_form, 'comments':comments})
    return HttpResponse(t.render(c))

def ADD_MAPS(request):
    t = loader.get_template('maps/add_maps.html')
    if request.method == 'POST':
        form = map_gallery_form(data=request.POST, files=request.FILES)
        if form.is_valid():
            v = form.save(commit=False)
            v.validated = False
            v.user =  getuser(request)
            v.save()
            xform = map_gallery_form()
            c = RequestContext(request,{'map_form':xform, 'SuccessForm':True})
            return HttpResponse(t.render(c))
        else:
            return HttpResponse("<b>Something went wrong: Form not valid</b>")
    elif request.method == 'GET':
        form = map_gallery_form()
        c = RequestContext(request,{'map_form':form})
        return HttpResponse(t.render(c))
    else:
        return HttpResponse("<b>No GET or POST received</b>")


def test_kml(request):
    rois = roi.objects.all()
    x = prepare_kml(rois)
    return x
    return HttpResponse("success?")

def prepare_kml(rois):
    kml = simplekml.Kml()
    for single_roi in rois:
        pol = kml.newpolygon(name=single_roi.category.name)
        return_list = build_tuples(rois_get_boundary_list(single_roi.points))
        pol.outerboundaryis = return_list
        pol.innerboundaryis = return_list
        pol.style.linestyle.color = simplekml.Color.green
        pol.style.linestyle.width = 5
    kml.save("download.kml")
    filename = "download.kml"
    wrapper = FileWrapper(file(filename))
    response = HttpResponse(wrapper, content_type='text/plain')
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = 'attachment; filename="eomf_rois.kml"'
    return response


# -104.62400049487444,43.92916666666666
# |-104.61667202513078,43.925|-104.62245706560994,43.925|-104.62978594059966,43.92916666666666|
def rois_get_boundary_list(string_points):
    char_array = list(string_points)
    list_points = []
    build_point = ""
    for x in char_array:
        if x == '|':
            list_points.append(float(build_point))
            build_point = ""
        elif x == ',':
            list_points.append(float(build_point))
            build_point = ""
        else:
            build_point = build_point + x
    return list_points

def build_tuples(list_of_points):
    new_list = []
    i = 0
    for x in list_of_points:
        if i%2 == 1:
            pass
        else:
            new_list.append((list_of_points[i],list_of_points[i+1]))
        i = i+1
    new_list.append(new_list[0])
    return new_list

def filter_kml(request):
    t = loader.get_template('maps/filter_rois.html')
    if request.method == 'POST':
        z = request.POST
        # return HttpResponse(json.dumps({'request':request.POST, 'z':z, 'test':z['lon']+str(5), 'test2':float(z['lon'])+5}))
        rois = roi.objects.all()
        if z['lon']:
            rois = rois.filter(lon__lt=(float(z['lon'])+5))
            rois = rois.filter(lon__gt=(float(z['lon'])-5))
        if z['lat']:
            rois = rois.filter(lat__lt=(float(z['lat'])+5))
            rois = rois.filter(lat__gt=(float(z['lat'])-5))
        if z['category']:  
            rois = rois.filter(category=Category.objects.get(pk = int(z['category'])))
        result = prepare_kml(rois)
        return result
    else:
        x = roiForm()
        c = RequestContext(request,{'form':x})
        return HttpResponse(t.render(c))