from django.template import Context, loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.core.files.base import ContentFile
from django.db.models import Q
from celery.result import AsyncResult
from raster.models import RasterProduct, RasterLayer

from ceom.modis.models import Product, Dataset, Tile, MODISMultipleTimeSeriesJob,  MODISSingleTimeSeriesJob
from ceom.photos.models import Category, Photo
from ceom.modis.forms import TimeSeriesJobForm

import os, re, glob, sys, csv, json, uuid, subprocess, numpy, math
from datetime import datetime, date, timedelta
from functools import reduce

from PIL import Image
from io import BytesIO


def index(request):
    return render(request, 'modis/overview.html')


def remote_sensing_datasets(request):
    dataset_list = Dataset.objects.all().order_by("name")
    product_list = Product.objects.all().order_by("name")
    return render(request, 'modis/remote_sensing_datasets.html', context={
        'dataset_list' : dataset_list,
        'product_list' : product_list,
    })


def tilemap(request, dataset_id, year):
    dataset = Dataset.objects.get(name__iexact=dataset_id)

    if dataset.location[-1] != '/':
        loc = dataset.location + '/'
    else:
        loc = dataset.location
    
    year_dirs = list(glob.glob(loc + '[0-9][0-9][0-9][0-9]/'))
    year_list = sorted([int(y[-5:-1]) for y in year_dirs])

    good_list = []
    bad_list = []

    for tile_dir in glob.glob(glob.escape(loc) + str(year) + '/h[0-9][0-9]v[0-9][0-9]/'):
        h = int(tile_dir[-6:-4])
        v = int(tile_dir[-3:-1])
        if len(glob.glob(tile_dir + '*.hdf')) == 46:
            good_list.append({'h': h, 'v':v})
        else:
            bad_list.append({'h': h, 'v':v})

    return render(request, 'modis/tiledatamap.html', context={
        'dataset' : dataset,
        'good_list' : good_list,
        'bad_list' : bad_list,
        'year' : year,
        'year_int': int(year),
        'year_list' : year_list,
    })
    
def tile(request, dataset_id, x, y):
    data = {}
    data['tile_name'] = "h%02dv%02d" % (int(x),int(y))
    data['file_total'] = 0
    data['file_data'] = []

    data['dataset'] = Dataset.objects.get(name__iexact=dataset_id)
    day_res = data['dataset'].day_res

    if data['dataset'].location[-1] != '/':
        loc = data['dataset'].location + '/'
    else:
        loc = data['dataset'].location

    year_dirs = list(glob.glob(glob.escape(loc) + '[0-9][0-9][0-9][0-9]/'))
    year_list = sorted([int(y[-5:-1]) for y in year_dirs])
    
    for y in year_list:
        files_in_year = glob.glob(glob.escape(loc) + str(y) + '/' + data['tile_name'] + '/*.hdf')
        days_present = sorted([int(fname.split('/')[-1].split('.')[1][5:8]) for fname in files_in_year])
        print(files_in_year)
        print(days_present)

        data['file_total'] += len(days_present)
        
        good_ranges = []
        bad_ranges = []

        # Iterate through year, looking for missing ranges of files. 
        currently_good = 1 in days_present
        range_start = 1
        for d in range(9, 365, day_res):
            if d not in days_present and currently_good:
                # Downward edge. End of present range / start of missing range.

                if range_start == d - day_res:
                    good_ranges.append(str(range_start))
                else:
                    good_ranges.append(str(range_start) + '-' + str(d - day_res))
                range_start = d
                currently_good = False

            elif d in days_present and not currently_good:
                # Upward edge. Start of present range / end of missing range.

                if range_start == d - day_res:
                    bad_ranges.append(str(range_start))
                else:
                    bad_ranges.append(str(range_start) + '-' + str(d - day_res))
                range_start = d
                currently_good = True

        # Handle final range
        if currently_good:
            if range_start == 365:
                good_ranges.append(str(365))
            else:
                good_ranges.append(str(range_start) + '-365')
        else:
            if range_start == 365:
                bad_ranges.append(str(365))
            else:
                bad_ranges.append(str(range_start) + '-365')

        data['file_data'].append((y, {
            'present': ','.join(good_ranges),
            'absent': ','.join(bad_ranges),
            'total': len(days_present)
        }))

    return render(request, 'modis/tile.html', context=data)

    
def latlon2sin(lat, lon, npix=2400.0):

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

    return render(request, 'modis/vimap.html', context={
        "mapOptions": options,
    })




@login_required()
def single_progress(request, task_id):
    data = {'task_id': task_id}

    try:
        data['found'] = True
        data['job'] = MODISSingleTimeSeriesJob.objects.get(task_id=task_id)
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

    job = MODISSingleTimeSeriesJob(lat=lat,lon=lon,user=request.user,years=years,product=dataset,task_id=task_id,col=xi,row=yi,tile=folder)
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

def get_single_task_progress(request,task_id):
    try:
        task_db = MODISSingleTimeSeriesJob.objects.get(task_id=task_id)
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

def get_multiple_task_progress(request, task_id):
    job = MODISMultipleTimeSeriesJob.objects.get(task_id=task_id)
    
    res = job.result.url if job.result else ""

    return JsonResponse({'working':job.working, 'completed':job.completed, 'errored':job.error, 'total_sites':job.total_sites, 'progress':job.progress, 'result':res})

MULTIPLE_TIMESERIES_LOCATION = os.path.join('modis','timeseries','multi')

@login_required
def multiple_del(request,del_id):
    tsj = MODISMultipleTimeSeriesJob.objects.filter(task_id=del_id)
    message=None
    if len(tsj)==1:
        # Cancel celery task
        terminate_task(tsj[0].task_id)
        tsj.delete()
    else:
        message="Could not find selected job for user. Please make sure it is valid and it is not being processed (working)."
    return redirect('/modis/timeseries/multiple/')

@login_required
def single_del(request,del_id):
    tsj = MODISSingleTimeSeriesJob.objects.filter(user=request.user,id=del_id)
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
    user_pending_jobs=MODISMultipleTimeSeriesJob.objects.filter(user=request.user,completed=False,working=False,error=False)
    if len(user_pending_jobs)>=2:
        return HttpResponseRedirect('/modis/timeseries/multiple/')
    if request.method == 'POST':
        form = TimeSeriesJobForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save_data(request.user,'')

            years = [int(y) for y in form.cleaned_data['years'].split(',')]
            points = job.points.file.name
            dataset = form.cleaned_data['product']

            task_id = multiple_site_modis.delay(points, settings.MEDIA_ROOT, MULTIPLE_TIMESERIES_LOCATION, dataset.name,years,dataset.xdim,dataset.day_res)
            job.task_id = str(task_id)
            job.save()
            
            return redirect('/modis/timeseries/multiple/t=' + str(task_id) + '/')
    else:
        form = TimeSeriesJobForm()
        
    #It is the first visit or form had errors
    return render(request, 'modis/multiple.html', context={"title":"Add Multiple Points time series request",'form':form})

@login_required
def multiple_progress(request, task_id):
    data = {}
    data['job'] = MODISMultipleTimeSeriesJob.objects.get(task_id=task_id)
    
    data['input_path'] = data['job'].points.url if data['job'].points else ""
    data['result_path'] = data['job'].result.url if data['job'].result else ""

    return render(request, 'modis/multiple_status.html', context=data)

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


