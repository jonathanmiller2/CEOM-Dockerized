from django.template import Context, RequestContext, loader, Template
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Q, Sum, Case, When
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count
from django.db import connection, transaction
from django.contrib.gis.geos import GEOSGeometry, Polygon, Point
from django.contrib.auth import authenticate, login, logout

import json as simplejson 

from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from django.core.files.base import ContentFile
from django.core.files import File
from django.shortcuts import redirect


from django.views.decorators.csrf import csrf_exempt
from django.template.defaultfilters import wordwrap
from ceom.photos.models import PhotoUser


from ceom.photos.templatetags.photos_tags import thumbnail, point2str
from ceom.photos.models import Photo, Category, CategoryVote
from ceom.photos.forms import SearchForm, PhotoForm, BatchEditForm

import datetime
import dateutil.parser as date_parser
import pickle
import itertools
import shutil
import os
import zlib, bz2, base64, pylzma, binascii


from pykml.factory import KML_ElementMaker as KML
from pykml import parser
from lxml import etree
from django.shortcuts import render

from django.utils.encoding import smart_str
import json
import csv

def zencode(obj):
    d = pylzma.compress(binascii.hexlify(pickle.dumps(obj,pickle.HIGHEST_PROTOCOL)))
    return base64.urlsafe_b64encode(d)


def zdecode(zstr):
    s = binascii.unhexlify(base64.urlsafe_b64decode(zstr))
    return pickle.loads(pylzma.decompress(s))


def compress(obj):
    #TODO: For some reason, pickle dumps are causing issues. If you see "could not decode bytes to JSON", with a confusing stack trace, it probably originates here.
    return pickle.dumps(obj)

def decompress(data):
    return pickle.loads(str(data))

def ranges(i):
    for a, b in itertools.groupby(enumerate(sorted(i)), lambda x, y: y - x):
        b = list(b)
        yield b[0][1], b[-1][1]


def home(request):
    return render(request, 'photos/overview.html')

def leaderboard(request):
    points = User.objects.annotate(user_points=Count('categoryvote')).order_by("-user_points")

    #Paginator 
    page_num = request.GET.get('page')
    paginator = Paginator(points, 100)
    page = paginator.get_page(page_num)

    return render(request, 'photos/leaderboard.html', {'page': page})    
#    return render(request, 'photos/leaderboard.html', context=data)


def search_for_photos(request):

    if 'sort' in request.POST:
        photos = Photo.objects.select_related("category").order_by(request.POST['sort']).reverse()
        request.session['sort'] = request.POST['sort']
    elif 'sort' in request.session:
        photos = Photo.objects.select_related("category").order_by(request.session['sort']).reverse()
    else:
        photos = Photo.objects.select_related("category").order_by('uploaddate').reverse()
        
    if request.user.is_authenticated:
        photos = photos.filter(Q(status=1) | (Q(status=2) & Q(user=request.user)))
    else:
        photos = photos.filter(status=1)

    if request.method == 'POST' or 'query' in request.session:
        if request.method == 'POST':
            search = SearchForm(request.POST)
        else:
            search = SearchForm(request.session['query'])

        if search.is_valid():
            if request.method == 'POST':
                request.session['query'] = request.POST #pickle.dumps(request.POST)


            l, t, r, b = -180, 90, 180, -90
            bbox = False
            if search.cleaned_data['lon_min'] is not None:
                l = search.cleaned_data['lon_min']
                bbox = True
            if search.cleaned_data['lon_max'] is not None:
                r = search.cleaned_data['lon_max']
                bbox = True
            if search.cleaned_data['lat_min'] is not None:
                b = search.cleaned_data['lat_min']
                bbox = True
            if search.cleaned_data['lat_max'] is not None:
                t = search.cleaned_data['lat_max']
                bbox = True
            if bbox:
                bbox = Polygon.from_bbox((l, t, r ,b))
                photos = photos.filter(point__bboverlaps=bbox)

            if search.cleaned_data['date_min'] is not None and search.cleaned_data['date_min'] != "" and search.cleaned_data['date_min'] != datetime.datetime(1990,1,1):
                dmin = search.cleaned_data['date_min']
                photos = photos.filter(takendate__gt=dmin)
            if search.cleaned_data['date_max'] is not None and search.cleaned_data['date_min'] != "" and search.cleaned_data['date_max'] != datetime.date.today():
                dmax = search.cleaned_data['date_max']
                photos = photos.filter(takendate__lt=dmax)

            if search.cleaned_data['user'] is not None:
                u = search.cleaned_data['user']
                photos = photos.filter(user__username=u)

            if search.cleaned_data['category'] is not None:
                cat = search.cleaned_data['category']
                photos = photos.filter(category=cat)

            if search.cleaned_data['country'] is not None:
                country = search.cleaned_data['country']
                photos = photos.filter(point__within=country.geometry)

            if search.cleaned_data['continent'] is not None:
                c = search.cleaned_data['continent']
                photos = photos.filter(point__within=c.geometry)

            if search.cleaned_data['keywords'] is not None:
                text = search.cleaned_data['keywords']
                words = text.split()
                for w in words:
                    photos = photos.filter(Q(notes__icontains=w)|Q(file__icontains=w))

    else:
        search = SearchForm()

    return photos, search


def user_photos(request):
    
    if request.user.is_authenticated:
        base, search = search_for_photos(request)

        # if 'sort' in request.GET: #Sorts by Takendate
        #     dates = base.distinct('takendate').filter(user=request.user).order_by('-takendate')
        # else:                     #Sorts by UploadDate
        #     dates = base.distinct('uploaddate').filter(user=request.user).order_by('-uploaddate')           
        
        data = {}
        data['search'] = search

        photos = base.filter(user=request.user)
        if len(photos)>0:
            if photos[0].takendate:
                data['gallerytitle'] = photos[0].takendate
        
        
        
        #Paginator Stuff
        page = request.GET.get('page',1)
        ppp = request.GET.get('ppp', 24)
        ppp = min(int(ppp),192)
        if page != "all" and ppp != "All":
            paginator = Paginator(photos, int(ppp))

            try:
                photos = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                photos = paginator.page(int(page))
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                photos = paginator.page(paginator.num_pages)

            page = int(page)
            page_range = sorted(list(set(range(page-4,page+4)).intersection(set(paginator.page_range))))
            
            data['paginator'] = paginator
            data['ppp']= ppp
            data['page_range']= page_range

        else:
            paginator = None
            page_range = list(range(10))
        
        data['photos'] = photos
        
        
        data['checkbox'] = True
        data['batch_edit_form'] = BatchEditForm()
        data['modis_timeseries'] = True

        request.session['next'] = '/photos/user/'
        return render(request, 'photos/user.html', context=data)
    else:
        return HttpResponseRedirect("/accounts/login/")


def browse(request):
    photos, search = search_for_photos(request)
    
    page = request.GET.get('page',1)
    ppp = request.GET.get('ppp', 24)
    ppp = min(int(ppp),192)
    if page != "all" and ppp != "All":
        paginator = Paginator(photos, int(ppp))

        try:
            photos = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            photos = paginator.page(int(page))
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            photos = paginator.page(paginator.num_pages)

        page = int(page)
        page_range = sorted(list(set(range(page-4,page+4)).intersection(set(paginator.page_range))))
    else:
        paginator = None
        page_range = list(range(10))
    
    
    request.session['next'] = '/photos/browse/'
    return render(request, 'photos/browse.html', context={
        'photos': photos,
        'paginator' : paginator,
        'search': search,
        'ppp': ppp,
        'page_range': page_range,
        'batch_edit_form': BatchEditForm(),
        'checkbox': True,
        'modis_timeseries': True,
    })


def map(request):

    #TODO: Once the map is working, go through and trim/optimize map(), clusters(), and gmapclusters(). Clusters() is likely not needed.

    photos, search = search_for_photos(request)

    kml = ""

    if 'bbox' in request.GET:
        kml = gmapclusters(request, photos)
    
    
    request.session['next'] = '/photos/map/'
    return render(request, 'photos/map.html', context={
        'search': search,
        'cluster_kml':kml,
        'checkbox':True,
        'modis_timeseries':True
    })
    

#TODO: Clusters may be unused, in favor of gmapclusters
def clusters(request):
    photos, search = search_for_photos(request)
    photos = photos.exclude(Q(point__bboverlaps=Point(0,0))|Q(point__isnull=True))

    if 'bbox' in request.GET:
        bb = request.GET['bbox'].split(',')
        bb = [float(x) for x in bb]
        poly = Polygon.from_bbox(bb)
        x_size = abs(bb[2] - bb[0])/50.0;
        y_size = x_size / 1.5
        clause = " 1=1 "
        photos = photos.filter(point__bboverlaps=poly)
        #die
    else:
        x_size = 22.25
        y_size = 11.125

    #QuerySet internals, could break on upgrade
    # Django 1.7+ fix
    compiler = photos.query.get_compiler(using='default')
    where, where_params = compiler.compile(photos.query.where)
    # This line worked on Django 1.4 (old)
    # where = photos.query.where.as_sql(connection.ops.quote_name, connection)

    # query = '''   SELECT
                      # array_to_string(array_agg(photos.id), ',') as ids,
                      # COUNT( photos.point ) AS count,
                      # ST_SnapToGrid(photos.point, %f, %f) as cluster,
                      # ST_AsKML(ST_Centroid(ST_Collect(point))) as point
                  # FROM photos INNER JOIN auth_user ON (photos.userid = auth_user.id) WHERE %s
                  # GROUP BY cluster
                  # ORDER BY count DESC ''' % (x_size, y_size, where[0])

    query = '''SELECT min(photos.id) as ids,
                      COUNT( photos.point ) AS count,
                      ST_SnapToGrid(photos.point, %f, %f) as cluster,
                      ST_AsKML(ST_Centroid(ST_Collect(point))) as point,
                      %f as x_size,
                      %f as y_size
                  FROM photos INNER JOIN auth_user ON (photos.userid = auth_user.id)  WHERE %s
                  GROUP BY cluster
                  ORDER BY count DESC;''' % (x_size, y_size,x_size,y_size, where)
    cursor = connection.cursor()
    cursor.execute(query, where_params)

    folder =  KML.folder(KML.name("Clusters"))
    pmid = 0
    for row in cursor.fetchall():
        pmid += 1
        ids, count, cluster, point,x_size,y_size = row
        pm = KML.Placemark(
            KML.name('Cluster: '+str(pmid)),
            KML.description(str(count)+" photos in cluster"),
            KML.ExtendedData(
                KML.Data(
                    KML.displayName('ids'),
                    KML.value(ids),
                    name='ids'
                ),
                KML.Data(
                    KML.displayName('count'),
                    KML.value(count),
                    name='count'
                ),
                KML.Data(
                    KML.displayName('x_size'),
                    KML.value(x_size),
                    name='x_size'
                ),
                KML.Data(
                    KML.displayName('y_size'),
                    KML.value(y_size),
                    name='y_size'
                )
            ),
            parser.fromstring(point)
        )
        folder.append(pm)

    doc = KML.document(
        KML.name("CEOM Photos"),
        folder
    )

    return HttpResponse(etree.tostring(doc))

def gmapclusters(request):
    photos, search = search_for_photos(request)
    photos = photos.exclude(Q(point__bboverlaps=Point(0,0))|Q(point__isnull=True))

    if 'bbox' in request.GET:
        bb = request.GET['bbox'].split(',')
        bb = [float(x) for x in bb]
        poly = Polygon.from_bbox(bb)
        x_size = abs(bb[2] - bb[0])/50.0;
        y_size = x_size / 1.5
        clause = " 1=1 "
        photos = photos.filter(point__bboverlaps=poly)
    else:
        x_size = 22.25
        y_size = 11.125

    #QuerySet internals, could break on upgrade
    # Django 1.7+ fix
    compiler = photos.query.get_compiler(using='default')
    where, where_params = compiler.compile(photos.query.where)
    # This line worked on Django 1.4 (old)
    # where = photos.query.where.as_sql(connection.ops.quote_name, connection)

    # query = '''   SELECT
                      # array_to_string(array_agg(photos.id), ',') as ids,
                      # COUNT( photos.point ) AS count,
                      # ST_SnapToGrid(photos.point, %f, %f) as cluster,
                      # ST_AsKML(ST_Centroid(ST_Collect(point))) as point
                  # FROM photos INNER JOIN auth_user ON (photos.userid = auth_user.id) WHERE %s
                  # GROUP BY cluster
                  # ORDER BY count DESC ''' % (x_size, y_size, where[0])

    query = '''SELECT min(photos.id) as ids,
                      COUNT( photos.point ) AS count,
                      ST_SnapToGrid(photos.point, %f, %f) as cluster,
                      ST_AsKML(ST_Centroid(ST_Collect(point))) as point,
                      %f as x_size,
                      %f as y_size
                  FROM photos INNER JOIN auth_user ON (photos.userid = auth_user.id)  WHERE %s
                  GROUP BY cluster
                  ORDER BY count DESC;''' % (x_size, y_size,x_size,y_size, where)
    cursor = connection.cursor()
    cursor.execute(query, where_params)


    doc = KML.kml(
        KML.Document(
            KML.name("CEOM Photos"),
        )
    )


    pmid = 0
    for row in cursor.fetchall():
        pmid += 1
        ids, count, cluster, point,x_size,y_size = row
        pm = KML.Placemark(
            KML.name('Cluster: '+str(pmid)),
            KML.styleUrl("#dotstyle"),
            KML.description(str(count)+" photos in cluster"),
            KML.ExtendedData(
                KML.Data(
                    KML.displayName('ids'),
                    KML.value(ids),
                    name='ids'
                ),
                KML.Data(
                    KML.displayName('count'),
                    KML.value(count),
                    name='count'
                ),
                KML.Data(
                    KML.displayName('x_size'),
                    KML.value(x_size),
                    name='x_size'
                ),
                KML.Data(
                    KML.displayName('y_size'),
                    KML.value(y_size),
                    name='y_size'
                )
            ),
            parser.fromstring(point)
        )
        doc.Document.append(pm)

    #Add xml tag
    response = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" + etree.tostring(doc).decode('utf-8')

    return HttpResponse(response)


def get_photos_id_from_cluster_photo_id(request, id, x_size=22.25, y_size=11.125):
    photos, search = search_for_photos(request)
    photos = photos.exclude(Q(point__bboverlaps=Point(0,0))|Q(point__isnull=True))

    #QuerySet internals, could break on upgrade
    # Django 1.7+ fix
    compiler = photos.query.get_compiler(using='default')
    where, where_params = compiler.compile(photos.query.where)
    id = int(id)
    scaping = '%s'
    query = '''SELECT array_to_string(array_agg(photos.id), ',') as ids ,      
                      COUNT( photos.point ) AS count,
                      ST_SnapToGrid(photos.point, %f, %f) as cluster,
                      ST_AsKML(ST_Centroid(ST_Collect(point))) as point
                  FROM photos INNER JOIN auth_user ON (photos.userid = auth_user.id) WHERE %s
                  GROUP BY cluster
                  having   
                        array_to_string(array_agg(photos.id), ',') like E'%%%%,%d,%%%%'
                    or  array_to_string(array_agg(photos.id), ',') like E'%d,%%%%'
                    or  array_to_string(array_agg(photos.id), ',') like E'%%%%,%d'
                    or  array_to_string(array_agg(photos.id), ',') like E'%d'
                  ORDER BY count DESC;''' % (x_size, y_size, where,id,id,id,id)
    cursor = connection.cursor()
    cursor.execute(query,where_params)
    for row in cursor.fetchall():
        ids, count, cluster, point = row
        return ids
        
def photos_json(request):
    id = request.GET['ids']
    ids = get_photos_id_from_cluster_photo_id(request, id)
    photos = Photo.objects.filter(id__in=ids.split(','))

    data = []
    for p in list(photos):
        url = thumbnail(p.file, "150x150")
        desc = '''
            <div class='row-fluid'>
                <div class='pull-left'><a href='http://%s/photos/view/%s/' class='thumbnail' target='_blank'>
                    <img class='thumb' src='%s'>
                </a></div>
            </div>
                %s <br/>
                %s <br/>''' % (request.META['SERVER_NAME'], p.id, url, p.takendate, point2str(p.point))

        if p.dir_card is not None and p.dir_card.strip() != '':
            desc += "Aspect: "+p.dir_card+"<br/>"
        if p.category:
            desc += p.category.name+"<br/>"
        if p.notes:
            desc += wordwrap(p.notes,45)+"<br/>"

        data.append({
            "id": p.id,
            "name": "Photo: "+p.file.name[-25:],
            "description": desc,
            "lon": p.point.x,
            "lat": p.point.y,
            "alt": p.alt
        })

    return HttpResponse(simplejson.dumps(data))

def map_gallery(request):
    photos, search = search_for_photos(request)

    id = request.GET['ids']
    x_size = float(request.GET['x_size'])
    y_size = float(request.GET['y_size'])
    ids = get_photos_id_from_cluster_photo_id(request, id, x_size,y_size)
    photos = photos.filter(id__in=ids.split(','))

    page = request.GET.get('page',1)
    ppp = request.GET.get('ppp', 24)
    ppp = min(int(ppp),192)
    if page != "all" and ppp != "All":
        paginator = Paginator(photos, int(ppp))

        try:
            photos = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            photos = paginator.page(int(page))
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            photos = paginator.page(paginator.num_pages)

        page = int(page)
        page_range = sorted(list(set(range(page-4,page+4)).intersection(set(paginator.page_range))))
    else:
        paginator = None
        page_range = range(10)
    
    
    request.session['next'] = '/photos/map/'
    return render(request, 'photos/browse_gallery_map.html', context={
        'photos': photos,
        'paginator' : paginator,
        'search': search,
        'ppp': ppp,
        'page_range': page_range,
        'batch_edit_form': BatchEditForm(),
        'checkbox': True,
        'modis_timeseries': True
    })

def kml(request):
    return HttpResponse()


def view(request, id):
    photo = get_object_or_404(Photo,pk=id) 
    return render(request, 'photos/view.html', context={
        'photo': photo,
    })

def batchedit(request):
    if 'next' in request.GET:
        next = request.GET['next']
    elif 'next' in request.session:
        next = request.session['next']
    else:
        next = "/photos/"

    if request.method == 'POST':
        form = BatchEditForm(request.POST)
        ids = request.POST.getlist('ids')
        photos = Photo.objects.filter(id__in=ids)
        #changed_fields = form.changed_data
        if form.is_valid():
            for p in photos:
                if request.user.is_authenticated==False:
                    return HttpResponseRedirect(next)
                if p.user != request.user and not request.user.is_superuser:
                    continue

                if form.cleaned_data['field_notes']:
                    p.notes = form.cleaned_data['field_notes']
                if form.cleaned_data['category']:
                    p.category = form.cleaned_data['category']
                if form.cleaned_data['status']:
                    p.status = form.cleaned_data['status']
                p.save()
    else:
        form = BatchEditForm()

    return HttpResponseRedirect(next)

def batchdelete(request):
    ids = request.POST.getlist('ids')
    photos = Photo.objects.filter(id__in=ids)

    for p in photos:
        if p.has_change_permission(request):
            p.status = 0
            p.save()

    if 'next' in request.POST:
        return redirect(request.POST['next'])
    else:
        return redirect("/photos/user/")

def detailedit(request):
    if 'ids' in request.GET:
        ids = request.GET.getlist('ids')

        valid_ids = []
        for id in ids:
            if Photo.objects.get(id=id).user == request.user or request.user.is_superuser:
                valid_ids.append(id)

        if len(valid_ids) > 0:
            photo_id = valid_ids[0]
            request.session['remaining_ids'] = valid_ids[1:]
            return HttpResponseRedirect('/photos/edit/' + photo_id)
    else:
        while Photo.objects.get(id=request.session['remaining_ids'][0]).user != request.user and not request.user.is_superuser and len(request.session['remaining_ids']) > 0:
            request.session['remaining_ids'] = request.session['remaining_ids'][1:]
        
        if len(request.session['remaining_ids']) > 0:
            photo_id = request.session['remaining_ids'][0]
            request.session['remaining_ids'] = request.session['remaining_ids'][1:]
            return HttpResponseRedirect('/photos/edit/' + photo_id)
        
    if 'next' in request.GET:
        next = request.GET['next']
    elif 'next' in request.session:
        next = request.session['next']
    else:
        next = "/photos/"
    
    return HttpResponseRedirect(next)

def edit(request, id):
    if 'next' in request.GET:
        next = request.GET['next']
    elif 'next' in request.session:
        next = request.session['next']
    else:
        next = '/photos/'

    if request.user.is_authenticated==False:
        return redirect(next)

    photo = Photo.objects.get(id=id)
    
    if photo.user != request.user and not request.user.is_superuser:
        return redirect(next)

    if photo.status == 0:
        return HttpResponse("<h2>Requested Photo Not Found</h2>")
        
    if request.method == 'POST':
        if request.POST['lat'] and request.POST['lon']:
            photo.lat = float(request.POST['lat'])
            photo.lon = float(request.POST['lon'])

        if request.POST['alt']:
            photo.alt = request.POST['alt']
        else:
            photo.alt = None

        if request.POST['takendate']:
            photo.takendate = request.POST['takendate']
        else:
            photo.takendate = None

        if request.POST['dir_card']:
            photo.dir_card = request.POST['dir_card']
        else:
            photo.dir_card = None
        
        if request.POST['status']:
            photo.status = request.POST['status']
        else:
            photo.statue = None

        if request.POST['category']:
            photo.category = Category.objects.get(name=request.POST['category'])
        else:
            photo.category = None

        photo.notes = request.POST['notes']
        photo.save()

        
        if 'del' in request.POST:
            photo.status = 0
            photo.save()
            return HttpResponseRedirect(next)
        
        if 'Save_and_Goto_Next_Photo' in request.POST:
            return HttpResponseRedirect("/photos/detailedit/")
        
        request.session['remaining_ids'] = []
        return HttpResponseRedirect(next)

    if 'remaining_ids' in request.session:
        show_next = len(request.session['remaining_ids']) > 0
    else:
        show_next = False

    return render(request, 'photos/edit.html', {
        'photo': photo,
        'show_next': show_next,
        'landcover_categories': Category.objects.all()
    })

def delete(request, id):
    photo = Photo.objects.get(pk=id)

    if photo.has_change_permission(request):
        photo.status = 0
        photo.save()
    
    if 'next' in request.GET:
        # Fix for photo tiles in the map gallery. You can only redirect to the map, not to the map gallery
        if "/photos/map_gallery" in request.GET["next"]:
            return redirect('/photos/map/')    

        return redirect(request.GET['next'])
    else:
        return redirect("/photos/user/")
 

def exif(request, id):
    photo = Photo.objects.get(pk=id)

    if photo.has_change_permission(request):
        return render(request, 'photos/exif.html', context={
            'photo': photo
        })
    else:
        return HttpResponseRedirect("/photos/browse/")


@csrf_exempt
def download(request):
    if request.method != 'POST':
        return HttpResponseRedirect("/photos/browse/")

    # return HttpResponse(json.dumps({'request':request.POST}))
    import zipfile, os, tempfile
    from io import StringIO, BytesIO

    work_dir = get_work_dir(request)
    ids = request.POST.getlist('ids')
    # return HttpResponse(json.dumps({'request':ids}))
    photos = Photo.objects.filter(id__in=ids)

    if request.POST['format'] != 'csv':
        photos = photos.exclude(Q(point__bboverlaps=Point(0,0))|Q(point__isnull=True))

    zipf = BytesIO()
    ziphandle = zipfile.ZipFile(zipf, mode="w")
    metadata = StringIO()

    if request.POST['format'] == 'csv':
        w = csv.writer(metadata)
        w.writerow(["id","filename","longitude","latitude","altitude","category","field_notes"])
        for p in list(photos):
            notes = smart_str(p.notes)
            row = ['','','','','','','']
            try:
                row = [p.id,p.file.name,p.lon,p.lat,p.alt,p.category,notes]
            except:
                if p.category != None and notes != None:
                    row = [p.id,str(p.file.name),p.lon,p.lat,p.alt,p.category,str(notes)]
                elif p.category == None:
                    row = [p.id,str(p.file.name),p.lon,p.lat,p.alt,str(notes)]
                elif notes == None:
                    row = [p.id,str(p.file.name),p.lon,p.lat,p.alt,p.category,"No notes"]
                else:
                    row = [p.id,str(p.file.name),p.lon,p.lat,p.alt,p.category,str(notes)]
                pass
            w.writerow(row)
            ziphandle.write(p.file.file.name, arcname=os.path.basename(p.file.name))

        metadata.flush()
        ziphandle.writestr("files.csv",metadata.getvalue())
        ziphandle.close()
        zipf.flush()
        fn = "archive_csv.zip"

    elif request.POST['format'] == 'kmz':
        folder =  KML.Folder(KML.name("Photos"))
        pmid = 0
        text = ''
        for p in list(photos):
            pmid += 1
            desc = '''<a href='http://%s/photos/view/%s/' target='_blank'>
                        <img width="300" height="224" src="%s"/>
                    </a><br/>
                    Date: %s <br/>
                    %s''' % (request.META['SERVER_NAME'], p.id, p.file.name, p.takendate, point2str(p.point))

            if p.dir_card is not None:
                desc += "Aspect: "+p.dir_card+"<br/>"
            if p.category:
                desc += "Category: "+p.category.name+"<br/>"
            if p.notes:
                desc += "Field notes: "+wordwrap(p.notes,45)+"<br/>"

            pm = KML.Placemark(
                KML.name("Photo"),
                KML.description(desc),
                KML.styleUrl("#pushpinstyle"),
                parser.fromstring(p.point.kml)
            )
            folder.append(pm)

            if request.POST['img'] ==  'big':
                ziphandle.write(p.file.file.name, os.path.basename(p.file.name))
            else:
                ziphandle.write(p.thumb_path("big"), p.file.name)

        doc = KML.kml(KML.Document(
            KML.name("CEOM Photos"),
            KML.Style(
              KML.IconStyle(
                KML.scale(1.0),
                KML.Icon(
                  KML.href("http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png"),
                ),
                id="mystyle"
              ),
              id="pushpin"
            ),
            KML.open(1),
            folder
        ))
        ziphandle.writestr("doc.kml", etree.tostring(doc, pretty_print=True))
        ziphandle.close()
        zipf.flush()
        fn = "archive.kmz"
    elif request.POST['format'] == 'shp':
        pass

    response = HttpResponse(zipf.getvalue())
    zipf.close()
    response['Content-Disposition'] = 'attachment; filename=%s' % (fn)
    response['Content-Type'] = 'application/x-zip'
    # return HttpResponse(json.dumps({'response':response}))
    return response

##############################################################################
#Upload stuff
#############

def upload(request):

    if request.method == 'POST':
        work_dir = get_work_dir(request)
        files = os.listdir(work_dir)
        ids = []
        for file in files:
            file_path = os.path.join(work_dir, file)
            if not os.path.isdir(file_path):
                photo = Photo(user=request.user)
                content = File(open(file_path,'rb'))
                photo.file.save(file, content, save=False)
                photo.exifPopulate()

                if 'private' in request.POST and request.POST['private'] == 'Yes':
                    photo.status = 2

                photo.save()
                os.remove(file_path)
                ids.append(int(photo.id))
                #photo.point = Point(lon,lat)

    return render(request, 'photos/upload.html')  

def get_file_info(file, work_url):

    if type(file) == str:
        file = open(file)
    filename = os.path.basename(file.name)

    if hasattr(file, "size"):
        file_size = file.size
    else:
        file_size =  os.fstat(file.fileno()).st_size

    thumb_url = thumbnail(file, "80x80", prefix="thumbs/")
    #settings imports
    file_delete_url = '/photos/upload/preload/delete/'+filename
    file_url = work_url+'/'+filename

    return {"name":filename,
            "size":file_size,
            "url":file_url,
            "thumbnail_url":thumb_url,
            "delete_url":file_delete_url,
            "delete_type":"DELETE",}

def get_work_dir(request):
    return os.path.join(settings.MEDIA_ROOT, "photos", request.user.username , "work")

@csrf_exempt
def preload_delete(request, name):
    work_dir = get_work_dir(request)
    file_path = os.path.join(work_dir, name)
    success = os.path.isfile(file_path) and name[0] != "." and os.remove(file_path)
    return HttpResponse(success)

@csrf_exempt
def preload(request):

    work_dir = get_work_dir(request)
    work_url = "/media/photos/"+request.user.username+"/work/"

    if not os.path.exists(work_dir):
        os.makedirs(work_dir)

    if '_method' in request.GET and request.GET['_method'] == 'DELETE':
        return preload_delete(request, request.POST['file'])
    elif '_method' in request.POST and request.POST['_method'] == 'DELETE':
        return preload_delete(request, request.POST['file'])

    if request.method == 'POST':
        result = []

        #getting file data for further manipulations
        for file in request.FILES.getlist('file'):

            if 'image' not in file.content_type.lower():
                return HttpResponse("Only Image Files Allowed")

            wrapped_file = UploadedFile(file)
            work_file = open(work_dir+"/"+wrapped_file.file.name, 'w+b')
            shutil.copyfileobj(wrapped_file.file, work_file)
            work_file.flush()
            #generating json response array
            result.append(get_file_info(File(work_file), work_url))

        response_data = simplejson.dumps(result)

    else:
        if "file" in request.GET:
            filename = os.path.basename(request.REQUEST['file'])
            file_path = os.path.join(work_dir, filename)
            response_data = simplejson.dumps(get_file_info(file_path, work_url))
        else:
            results = []
            for file in os.listdir(work_dir):
                file_path = os.path.join(work_dir, file)
                if not os.path.isdir(file_path):
                    results.append(get_file_info(file_path, work_url))

            response_data = simplejson.dumps(results)
        

    #checking for json data type
    #big thanks to Guy Shapiro
    try:
        if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
            mimetype = 'application/json'
        else:
            mimetype = 'text/plain'
    except:
        mimetype = 'text/plain'


    return HttpResponse()

@csrf_exempt
def mobile_upload(request):
	
    '''
        Middleware login doesn't seem to be working for me, so this endpoint is for uploading images when getting user via request.user doesn't work
    '''

    #TODO: Authenticate using Middleware, rather than sending password with request

    work_dir = get_work_dir(request)

    if not os.path.exists(work_dir):
        os.makedirs(work_dir)

    data = {}

    try:
        landcover_cat = int(request.POST['landcover_cat'])
        notes = request.POST['notes']
        tmp_file = request.FILES['file']
        if 'image' not in tmp_file.content_type.lower():
            raise Exception("Only Image Files Allowed")
        category = Category.objects.get(id=landcover_cat)

        user = authenticate(username=request.POST['username'], password=request.POST['password'])

        photo = Photo(user=user, file=tmp_file, category = category, notes= notes )
        if 'private' in request.POST and request.POST['private'] == 'Yes':
            photo.status = 2

        try:

            time_string = request.POST['date_taken']
            taken_time = date_parser.parse(time_string)

            lat = float(request.POST['lat'])
            lon = float(request.POST['lon'])
            alt = float(request.POST['alt'])
            dir_deg = float(request.POST['dir_deg'])

            #HttpResponse('Lat: ' + str(lat) + ' Lon: ' + str(lon) + ' Alt: ' + str(alt) + ' Dir-deg: ' + str(dir_deg))

            photo.fieldPopulate(lat, lon, alt, dir_deg, taken_time)

        except Exception as e:
        	return HttpResponse('ERROR:'+ str(e), status=404)
        
        photo.save()
        
        data['id'] = int(photo.id)
        data['success'] = "true"

    except Exception as e:
        data['success'] = "false"
        data['error'] = str(e)

    response_data = simplejson.dumps(data)

    try:
        if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
            mimetype = 'application/json'
        else:
            mimetype = 'text/plain'
    except:
        mimetype = 'text/plain'

    return HttpResponse(response_data, content_type=mimetype)
    

def photos_coord(request,lat ,lon,radius):
    MAX_PHOTOS = 40
    photos = Photo.objects.raw('''
        SELECT  *, ST_Distance_Sphere( ST_Point(ST_X(ST_Centroid(point)), ST_Y(ST_Centroid(point))), (ST_MakePoint(%f, %f))) as dist
        FROM photos
        WHERE GeometryType(ST_Centroid(point)) = 'POINT' 
          AND ST_Distance_Sphere( ST_Point(ST_X(ST_Centroid(point)), ST_Y(ST_Centroid(point))), (ST_MakePoint(%f, %f))) <=%f *2
        order by dist
        ''' % (float(lat),float(lon),float(lat),float(lon),float(radius)))[0:MAX_PHOTOS]

    data = []
    for p in list(photos):
        url = thumbnail(p.file, "150x150")
        desc = '''
            <div class='row-fluid'>
                <div class='pull-left'><a href='http://%s/photos/view/%s/' class='thumbnail' target='_blank'>
                    <img class='thumb' src='%s'>
                </a></div>
            </div>
                %s <br/>
                %s <br/>''' % (request.META['SERVER_NAME'], p.id, url, p.takendate, point2str(p.point))

        if p.dir_card is not None and p.dir_card.strip() != '':
            desc += "Aspect: "+p.dir_card+"<br/>"
        if p.category:
            desc += p.category.name+"<br/>"
        if p.notes:
            desc += wordwrap(p.notes,45)+"<br/>"

        data.append({
            "id": p.id,
            "name": "Photo: "+p.file.name[-25:],
            "date": str(p.takendate),
            "photo_file_url": url,
            "complete_file_url": '''http://%s%s'''%(request.META['SERVER_NAME'],url),
            "photo_url": '''http://%s/photos/view/%s/'''%(request.META['SERVER_NAME'],p.id),
            "lon": p.point.x,
            "lat": p.point.y,
            "alt": p.alt
        })

    return HttpResponse(simplejson.dumps(data))


def FieldPhoto(request):
    return render(request, 'photos/Field_photo_weekend.html')


def classification(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/accounts/login/")

    if request.method == 'POST':
        # Check if someone is trying to vote "unclassified"
        unclassified_category = Category.objects.get(name__iexact='Unclassified')
        if not request.POST['categoryid'] or int(unclassified_category.id) == int(request.POST['categoryid']):
            return HttpResponseRedirect("/photos/classification/")

        cat = Category.objects.get(id=request.POST['categoryid'])
        photo = Photo.objects.get(id=request.POST['photoid'])

        # Create new vote
        CategoryVote.objects.update_or_create(photo=photo, user=request.user, defaults={'category': cat})

        # Re-evalute photo to see if classification has changed
        scores = CategoryVote.objects.filter(photo=request.POST['photoid']).values('category').annotate(
                                        score=Sum(
                                            Case(
                                                When(user=photo.user, then=2),
                                                default=1
                                            )
                                        )
                                    ).order_by('-score')
        winning_category_id = scores[0]['category']

        # Update photo's stored category
        photo.category = Category.objects.get(id=winning_category_id)
        photo.save()

        return HttpResponseRedirect("/photos/classification/")


    data = {}

    unclassified_category = Category.objects.get(name__iexact='Unclassified')
    users_voted_photos = CategoryVote.objects.filter(user=request.user).values_list('photo')
    user_vote_count = len(users_voted_photos)
    photo_set = Photo.objects.filter(point__isnull=False).filter(Q(category__isnull=True) | Q(category=unclassified_category)).filter(status=1).exclude(id__in=users_voted_photos).order_by('?')

    #If there are no photos that are geolocated, unclassified, and public
    if photo_set.count() <= 0:
        #Then just show a photo that is geolocated, classified, and public
        photo_set = Photo.objects.filter(point__isnull=False).filter(status=1).exclude(id__in=users_voted_photos).order_by('?')
    
    #If there are still no photos
    if photo_set.count() <= 0:
        return render(request, 'photos/classification.html')

    data['score'] = user_vote_count
    data['photo'] = photo_set[0]
    data['landcover_categories'] = Category.objects.all()
    return render(request, 'photos/classification.html', context=data)