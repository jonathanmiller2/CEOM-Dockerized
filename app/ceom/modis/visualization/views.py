from django.template import Context, RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.core.files.base import ContentFile
from django.db.models import Q
from ceom.modis.inventory.models import Dataset
from ceom.photos.models import Category, Photo
from ceom.modis.visualization.models import TimeSeriesJob,  SingleTimeSeriesJob, GeocatterPoint
from ceom.modis.visualization.forms import TimeSeriesJobForm
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
from ceom.celeryq.tasks import get_modis_raw_data
#from ceom.celeryq.tasks import get_modis_raw_data, latlon2sin
from ceom.celeryq.tasks_multi import multiple_site_modis,terminate_task


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
    return render(request, 'visualization/overview.html')

@login_required()
def gmap(request):
    datasets = Dataset.objects.filter(is_global=False).order_by('name')
    years = [y for y in range (2000,date.today().year +1)]
    return render(request, 'visualization/gmap.html', context={
        'datasets':datasets,
        'years':years,
    })

@login_required()
def gmap1(request, lat, lon):
    lon = float(lon)
    lat = float(lat)
    datasets = Dataset.objects.filter(is_global=False).order_by('name')
    years = [y for y in range (2000,date.today().year +1)]

    return render(request, 'visualization/gmap.html', context={
        'datasets':datasets,
        'years':years,
        'lonRedirect':lon,
        'latRedirect':lat,
        'photoRedirect':True,
    })

@login_required()
def tropomi(request):
    datasets = Dataset.objects.filter(is_global=False).order_by('name')
    years = [y for y in range (2000, date.today().year + 1)]
    return render(request, 'visualization/tropomi.html', context={
        'datasets':datasets,
        'years':years,
    })

@login_required()
def tropomi1(request, lat, lon):
    lon = float(lon)
    lat = float(lat)
    datasets = Dataset.objects.filter(is_global=False).order_by('name')
    years = [y for y in range (2000,date.today().year +1)]

    return render(request, 'visualization/tropomi.html', context={
        'datasets':datasets,
        'years':years,
        'lonRedirect':lon,
        'latRedirect':lat,
        'photoRedirect':True,
    })


def manual(request):
    return render(request, 'visualization/manual.html')

def olmap(request):
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

    return render(request, 'visualization/olmap.html', context={
        "mapOptions": options,
    })

def gemap(request):
    # ds = Datainfo.objects.all().order_by('label')
    ds = None
    return render(request, 'visualization/gemap.html', context={
        'content': "This is a map",
        'datasets': ds,
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

TIMESERIES_LOCATION = os.path.join('media','visualization','timeseries','single')

@login_required()
def timeseries_single_progress(request, task_id):

    t = loader.get_template('visualization/single_site_timeseries.html')
    try:
        task_db = SingleTimeSeriesJob.objects.get(task_id=task_id)
        if task_db.user != request.user:
            raise Exception('User does not own the task')

        filepath = str(task_db.result)
        if filepath and filepath[0] != '/':
            filepath = '/' + filepath
        
        c = {"job_id":task_db.id,
            "task_id":task_id,
            "found":True,
            "completed": task_db.completed,
            "lat":task_db.lat,
            "lon":task_db.lon,
            "dataset":task_db.product,
            'row':task_db.row,
            'col':task_db.col,
            'tile':task_db.tile,
            'years':task_db.years,
            'file': filepath}
    except Exception as e:
        c = {"task_id":task_id,"found":False}
    
    return render(request, 'visualization/single_site_timeseries.html', context=c)


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
    task_id = get_modis_raw_data.delay(TIMESERIES_LOCATION,lat,lon,dataset.name,years_formated,dataset_npix,dataset_freq_in_days)     

    job = SingleTimeSeriesJob(lat=lat,lon=lon,user=request.user,years=years,product=dataset,task_id=task_id,col=xi,row=yi,tile=folder)
    job.save()
    return redirect(to='/modis/visualization/timeseries/single/t=%s/'%task_id)

# This page will host all single timeseries from a user
@login_required()
def timeseries_single_history(request):
    user_tasks = SingleTimeSeriesJob.objects.filter(user=request.user).order_by('-created')
    paginator = Paginator(user_tasks, 25) # Show 25 jobs per page

    page = request.GET.get('page',1)
    if page != "all":
        try:
            jobs = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            jobs = paginator.page(int(page))
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            jobs = paginator.page(paginator.num_pages)

        page = int(page)
        page_range = sorted(list(set(range(page-4,page+4)).intersection(set(paginator.page_range))))
    else:
        paginator = None
        page_range = list(range(10))
    return render(request, 'visualization/single_timeseries_history.html', context={
        "jobs": jobs,
        'paginator': paginator,
        'page_range': page_range,
        })

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
            url = str(task_db.result)
            if url and url[0] != '/':
                url = '/' + url

            return JsonResponse({
                'success':True, 
                'url': url,
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

MULTIPLE_TIMESERIES_LOCATION = os.path.join(settings.MEDIA_ROOT,'visualization','timeseries','multi')

@login_required
def multiple(request):
    user_tasks = TimeSeriesJob.objects.filter(user=request.user).order_by('-timestamp')
    too_many_tasks = False
    if len(user_tasks)>=2:
        too_many_tasks = True
    paginator = Paginator(user_tasks, 25) # Show 25 jobs per page

    page = request.GET.get('page',1)
    if page != "all":
        try:
            jobs = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            jobs = paginator.page(int(page))
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            jobs = paginator.page(paginator.num_pages)
        page = int(page)
        page_range = sorted(list(set(range(page-4,page+4)).intersection(set(paginator.page_range))))
    else:
        paginator = None
        page_range = list(range(10))
    task_in_progress = any([job.working for job in jobs])
    
    return render(request, 'visualization/multiple.html', context={
        "task_in_progress":task_in_progress,
        'jobs':jobs, 
        'paginator': paginator,
        "too_many_tasks":too_many_tasks,
        'page_range': page_range    
    })
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
    return redirect('/visualization/multiple/')

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
    return redirect('/visualization/timeseries/single/')

@login_required
def multiple_add(request):
    user_pending_jobs=TimeSeriesJob.objects.filter(user=request.user,completed=False,working=False,error=False)
    if len(user_pending_jobs)>=2:
        return HttpResponseRedirect('/visualization/multiple/')
    if request.method == 'POST':
        form = TimeSeriesJobForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save_data(request.user,'')

            csv_folder = MULTIPLE_TIMESERIES_LOCATION
            media_timeseries = os.path.join('visualization','timeseries','multi')
            years = [int(y) for y in form.cleaned_data['years'].split(',')]
            points = job.points.file.name
            dataset = form.cleaned_data['product']

            task_id = multiple_site_modis.delay(points,csv_folder,media_timeseries,dataset.name,years,dataset.xdim,dataset.day_res)
            job.task_id = str(task_id)
            job.save()
            
            return HttpResponseRedirect('/visualization/multiple/')
    else:
        form = TimeSeriesJobForm()
    #It is the first visit or form had errors
    return render(request, 'visualization/multiple_add.html', context={"title":"Add Multiple Points time series request",'form':form})

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
    return render(request, 'visualization/composite.html', context={'julian_day': str(julian_day).zfill(3),
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
        
    return render(request, 'visualization/geocatter.html', context=data)