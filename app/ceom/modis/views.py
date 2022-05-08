from ceom.modis.models import File, Product, Dataset, Tile
from django.template import Context, loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
import numpy
import sys, os

from django.core.files.base import ContentFile
from django.db.models import Q
from ceom.modis.models import Dataset
from ceom.photos.models import Category, Photo
from ceom.modis.models import TimeSeriesJob,  SingleTimeSeriesJob, GeocatterPoint
from ceom.modis.forms import TimeSeriesJobForm
from datetime import datetime, date, timedelta

from functools import reduce
from raster.models import RasterProduct, RasterLayer

#TODO: Are these imports necessary?
#from django.template.context_processors import csrf

import numpy, math
import  os, re, glob, sys
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Need to change to include new celery script
# import process

import csv, json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Celery tasks
from ceom.modis.taskprocessing.tasks import get_modis_raw_data
#from ceom.celeryq.tasks import get_modis_raw_data, latlon2sin
from ceom.modis.taskprocessing.tasks_multi import multiple_site_modis,terminate_task


from celery.result import AsyncResult

from django.conf import settings

#Charting lib
# from chartit import DataPool, Chart
import csv
import uuid
import subprocess



ERROR_NOT_EXIST_MESSAGE = 'Could not retrieve task. It may not exist or may have expired.'
FAILURE_MESSAGE = 'We are sorry, but an error occured while processing the task. Please contact the administrator.'
PENDING_MESSAGE = 'Waiting in queue... (If it takes too long please contact the administrator)'
PROCESSING_MESSAGE = 'Processing...'

def remote_sensing_datasets(request):
    # existing = File.objects.values('dataset').distinct()
    # dataset_list = Dataset.objects.filter(file__dataset_id__isnull=False).order_by("name")
    dataset_list = Dataset.objects.all().order_by("name")
    product_list = Product.objects.all().order_by("name")
    return render(request, 'modis/remote_sensing_datasets.html', context={
        'dataset_list' : dataset_list,
        'product_list' : product_list,
    })

def tilemap(request, dataset_id, year):
    dataset = Dataset.objects.get(name__iexact=dataset_id)
    # Need to replace existing and dataset_list query. It is too slow... use subqueries and group by!!!  
    existing = File.objects.distinct().values('dataset')
    #existing = [mcd43a4,mod09a1,mod09ga,mod09q1,mod11a1,mod11a2,mod11c3,mod12q1,mod13a1,mod13a2,mod13c2,mod13q1,mod14a2,mod15a2,mod17a2,myd11a2,myd11c3,myd14a2]
    dataset_list = Dataset.objects.filter(name__in=existing)
    # dataset_list contains all the information of the product in the existing list above
    year_list = File.objects.filter(dataset=dataset).distinct().order_by('year').values('year')
    #year_list = [2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016]

    good_list = []
    bad_list = []

    def splittiles(n):
        #TODO: THIS FUNCTIONALITY IS GOING TO BE BROKEN UNTIL THIS IS REWRITTEN
        # with_count() WAS A HIGHLY, HIGHLY DANGEROUS METHOD THAT NEEDED TO BE REMOVED IMMEDIATELY

        # for tile in Tile.objects.with_count(dataset_id,year):
        #     if tile.count == n:
        #         good_list.append(tile)
        #     else:
        #         bad_list.append(tile)
        pass
    
    if year == '2000':
        splittiles(40)
    elif year == '2001':
        splittiles(45)
    else:
        splittiles(46)

    return render(request, 'modis/map.html', context={
        'dataset' : dataset_id,
        'dataset_list' : dataset_list,
        'good_list' : good_list,
        'bad_list' : bad_list,
        'year' : year,
        'year_int': int(year),
        'year_list' : year_list,
    })
    
def tile(request, x, y):

    #TODO: Why are there two functions named the same thing?
    def daystoranges( days,day_res):
        l = []
        if len(days) > 0:
            rang = []
            rang.append(days[0])
            prev = days[0]

            for i in range(1, len(days)):
                if days[i]-day_res != prev:
                    l.append(rang)
                    rang = []
                rang.append(days[i])
                prev = days[i]
            l.append(rang)
        for i in range(0,len(l)):
            l[i] = [l[i][0], l[i][-1]]
        return l

    def daysToRanges( days,day_res):
        ranges = []
        for r in daystoranges(days,day_res):
            if r[0] != r[1]:
                ranges.append('-'.join(map(str, r)))
            else:
                ranges.append(str(r[0]))

        return ', '.join(ranges)

    #This function takes sorted array of day numbers with 8 days
    # interval and returns the days that are missing
    def missingdays( days,day_res):
        l = []
        i = 0
        length = len(days)
        for d in range(1, 365, day_res):
            if (i>=length or d != days[i]):
                l.append(d)
            else:
                i=i+1

        return l

    def parsePresentMissing( days,day_res):
        s = daysToRanges(days,day_res)
        m = daysToRanges(missingdays(days,day_res),day_res)
        return s, m

    def getproducts(names,dataset_day_res_dict):
        dic = {}
        result = []
        for name in sorted(names):
            f = name.split('.')
            # MOD09A1.A2000185.h12v01.005.2006292063546.hdf
            if(f[5]=='hdf'):
                product = f[0]
                year = f[1][1:5]
                tile = f[2]
                day = f[1][-3:]
                dic.setdefault(product,{}).setdefault(year, {}).setdefault(tile,[]).append(int(day))

        # Could be improved by removing the expensive sorting by using lists ( O(log n))
        for p in sorted(dic.keys()):
            years = dic[p]
            year_list = []
            for y in sorted(years.keys()):
                tiles = years[y]
                tile_list = []
                for t in sorted(tiles.keys()):
                    days = tiles[t]
                    days.sort()
                    dataset_day_res_dict[p]
                    present, missing = parsePresentMissing(days,dataset_day_res_dict[p])
                    tile_list.append((t, {'ranges': present, 'missing': missing, 'total': len(days)}))
                year_list.append((y, tile_list))
            result.append((p, year_list))
        return result


    import datetime
    tileq = "h%02dv%02d" % (int(x),int(y))
    files_query = File.objects.filter(tile=tileq).values('name').order_by('name')
    dataset_day_res_query = Dataset.objects.all().values('name','day_res')
    dataset_day_res_dict = {d['name']:d['day_res'] for d in dataset_day_res_query}
    files = [ row['name'] for row in files_query]
    files = getproducts(files,dataset_day_res_dict)
    return render(request, 'modis/tile.html', context={
        'tile': tileq,
        'files': files,
        'total': len(files_query),
    })
    
    
def detail(request, product_id):
    try:
        prod = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        raise Http404
    return render(request, 'modis/remote_sensing_datasets.html', context={'prod': prod})


from PIL import Image
from django.conf import settings
from io import BytesIO

    
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
    folder = 'h%02dv%02d' % (ih,iv) 
    return ih,iv,xi,yi,folder

def down(request):
    return HttpResponse("Temporarily offline")

def index(request):
    return render(request, 'modis/overview.html')

@login_required()
def single(request):
    datasets = Dataset.objects.filter(is_global=False).order_by('name')
    years = [y for y in range (2000,date.today().year +1)]
    return render(request, 'modis/single.html', context={
        'datasets':datasets,
        'years':years,
    })

def vimap(request):
    products = RasterProduct.objects.all()

    options = {}

    for product in products:
        prod_dict = {}

        years = RasterLayer.objects.filter(product=product).values_list('year', flat=True).distinct().order_by('year')

        for year in years:
            days = RasterLayer.objects.filter(year=year).values_list('day', flat=True).distinct().order_by('day')
            prod_dict[year] = list(days)
        
        options[product.name] = prod_dict

    options = json.dumps(options)

    return render(request, 'modis/olmap.html', context={
        "mapOptions": options,
    })

def indices_kml(request):
    timespans = []
    for y in range(2002,2003):
        for d in range(1,96,8):
            time = date(y,1,1) + timedelta(d-1)
            timespans.append({'layers':"TOP%2CBOT%2Cocean_mask",
                             'params':"year=%d&day=%d&prod=evi"%(y,d),
                             'begin':time,
                             'end':time+timedelta(d+6) })

    #test = points[0].kml
    return render(request, 'kml/wrap_wms_time.kml', context={'timespans' : timespans, 'host':request.META['HTTP_HOST']}, content_type = "application/vnd.google-earth.kml+xml")


def evi_kml(request):
    timespans = []
    for y in range(2002,2003):
        for d in range(1,96,8):
            time = date(y,1,1) + timedelta(d-1)
            timespans.append({'layers':"TOP%2CBOT%2Cocean_mask",
                             'params':"year=%d&day=%d&prod=evi"%(y,d),
                             'begin':time,
                             'end':time+timedelta(d+6) })

    #test = points[0].kml
    return render(request, 'kml/wrap_wms_time.kml', context={'timespans' : timespans, 'host':request.META['HTTP_HOST']}, content_type="application/vnd.google-earth.kml+xml")


def kml(request, name):
    try:
        styles = targetModel().styles()
    except AttributeError:

        styles = [{'name':'default', 'color':'8800ff00', 'icon':'http://maps.google.com/mapfiles/kml/shapes/info.png'}]

    return render(request, 'kml/main.kml', context= {'styles':styles, 'geometries':objects}, mimetype="application/vnd.google-earth.kml+xml")

TIMESERIES_LOCATION = os.path.join('MODIS','timeseries','single')

@login_required()
def timeseries_single_progress(request, task_id):
    data = {'task_id': task_id}

    try:
        data['found'] = True
        data['job'] = SingleTimeSeriesJob.objects.get(task_id=task_id)
    except Exception as e:
        print(e)
        data['found'] = False
    
    return render(request, 'modis/single_status.html', context=data)


@login_required()
def launch_single_site_timeseries(request, lat, lon, dataset, years, product=None):

    years_formated = [int(year) for year in years.split(',')]
    dataset_freq_in_days = 8
    # try:
    dataset = Dataset.objects.get(name__iexact=dataset)
    dataset_npix = dataset.xdim #2400 for mod09a1
    dataset_freq_in_days = dataset.day_res # 8 for mod09a1
    # except Exception as e:
    #     return HttpResponse("An error occurred. If you did not modify the URL please contact the web administrator")
    lon=float(lon)
    lat = float(lat)
    dataset_npix = int(dataset_npix)
    ih,iv,xi,yi,folder = latlon2sin(lat,lon,dataset,dataset_npix)
    vi=False
    task_id = get_modis_raw_data.delay(settings.MEDIA_ROOT, TIMESERIES_LOCATION,lat,lon,dataset.name,years_formated,dataset_npix,dataset_freq_in_days)     

    job = SingleTimeSeriesJob(lat=lat,lon=lon,user=request.user,years=years,product=dataset,task_id=task_id,col=xi,row=yi,tile=folder)
    job.save()
    return redirect(to='/modis/timeseries/single/t=%s/'%task_id)

def read_from_csv(absolute_path):
    header=None
    data = []
    with open(absolute_path, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            if header is None:
                header = row
            else:
                raw_dict = {}
                for col in range(0,len(header)):
                    raw_dict[header[col]] = row[col]
                data.append(raw_dict)
    return data

def get_task_progress(request,task_id):
    try:
        task_db = SingleTimeSeriesJob.objects.get(task_id=task_id)
        if not task_db.completed:
            task = AsyncResult(str(task_id))
            if task.result is None:
                return JsonResponse({'not_found':True,'message':ERROR_NOT_EXIST_MESSAGE})
            if task.status=="FAILURE":
                return JsonResponse({'failure':True,'message':FAILURE_MESSAGE})
            elif task.status=="STARTED":
                # Task is still running
                data = {
                    'progress':True,
                    'completed':task.result['completed'],
                    'errors': task.result['error'],
                    'total':task.result['total'],
                    'message': PROCESSING_MESSAGE,
                    }
                return JsonResponse(data)
        else:
            return JsonResponse({
                'success':True, 
                'url': task_db.result.url,
                })
    except Exception as e:
        return JsonResponse({'failure':True,'message':'Unhandled exception: %s' % e})

def get_multiple_task_progress(request):
    tasks_ids = request.GET.getlist('task_id_array[]')
    try:
        if not tasks_ids:
            raise Exception('Task List is empty')
        tasks = TimeSeriesJob.objects.filter(Q(user=request.user)&Q(reduce(lambda x, y: x | y, [Q(id=task_id) for task_id in tasks_ids])))
        tasks_dict = [(t.toJSON()) for t in tasks]
        return JsonResponse({'tasks':tasks_dict,'success':True})
    except Exception as e:
        return JsonResponse({'success':False,'message':'Unhandled exception: %s' % e})
    return HttpResponse()

MULTIPLE_TIMESERIES_LOCATION = os.path.join('MODIS','timeseries','multi')

@login_required
def multiple_del(request,del_id):
    tsj = TimeSeriesJob.objects.filter(user=request.user,id=del_id)
    message=None
    if len(tsj)==1:
        # Cancel celery task
        terminate_task(tsj[0].task_id)
        tsj.delete()
    else:
        message="Could not find selected job for user. Please make sure it is valid and it is not being processed (working)."
    return redirect('/modis/timeseries/multiple_add/')

@login_required
def single_del(request,del_id):
    tsj = SingleTimeSeriesJob.objects.filter(user=request.user,id=del_id)
    message=None
    if len(tsj)==1:
        # Cancel celery task
        terminate_task(tsj[0].task_id)
        tsj.delete()
    else:
        message="Could not find selected job for user. Please make sure it is valid and it is not being processed (working)."
    return redirect('/modis/timeseries/single/')

@login_required
def multiple(request):
    user_pending_jobs=TimeSeriesJob.objects.filter(user=request.user,completed=False,working=False,error=False)
    if len(user_pending_jobs)>=2:
        return HttpResponseRedirect('/modis/timeseries/multiple/')
    if request.method == 'POST':
        form = TimeSeriesJobForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save_data(request.user,'')

            csv_folder = MULTIPLE_TIMESERIES_LOCATION
            years = [int(y) for y in form.cleaned_data['years'].split(',')]
            points = job.points.file.name
            dataset = form.cleaned_data['product']

            #TODO: this needs fixed
            task_id = multiple_site_modis.delay(points,csv_folder, MULTIPLE_TIMESERIES_LOCATION, dataset.name,years,dataset.xdim,dataset.day_res)
            job.task_id = str(task_id)
            job.save()
            
            return HttpResponseRedirect('/modis/timeseries/multiple/')
    else:
        form = TimeSeriesJobForm()
        
    #It is the first visit or form had errors
    return render(request, 'modis/multiple.html', context={"title":"Add Multiple Points time series request",'form':form})

def composite(request, year = None, julian_day = None):
    prod='MOD09'
    sat_name="Terra"
    sat_ver = 'C6'
    version = "006"
    year = year
    julian_day = julian_day
    if (year== None or julian_day == None):
        julian_day = int(55)
        year = int(2000)
    next8_day = int(julian_day) + 8
    next8_year = year
    julian_day = int(julian_day)
    if next8_day > 365:
        next8_day = 1
        next8_year=int(year)+1
    previous8_day = int(julian_day) - 8
    previous8_year = year
    if previous8_day < 1:
        previous8_day = 365
        previous8_year=int(year)-1
    return render(request, 'modis/composite.html', context={'julian_day': str(julian_day).zfill(3),
            'year': year,
            'next8_year': next8_year,
            'next8_day': str(next8_day).zfill(3),
            'previous8_year': previous8_year,
            'previous8_day': str(previous8_day).zfill(3),
            'prod': prod,
            'sat_ver': sat_ver,
            'version': version,
            'sat_name': sat_name,
            }
        )


def geocatter(request):
    data = {}
    data['category_list'] = Category.objects.all()

    if request.method == 'POST' and 'category' in request.POST:
        GeocatterPoint.objects.create(
            lat = request.POST['lat'],
            lon = request.POST['lon'],
            category = Category.objects.get(name=request.POST['category'])
        )
        return HttpResponse()
    return render(request, 'modis/geocatter.html', context=data)
    