from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import JsonResponse
from raster.models import RasterProduct, RasterLayer

import os, glob, csv, json, math, re
from datetime import datetime, date, timedelta

from ceom.celery import app
from ceom.modis.models import *
from ceom.modis.tasks import *


SINGLE_TIMESERIES_LOCATION = os.path.join('MODIS','timeseries','single')
MULTIPLE_TIMESERIES_INPUT_LOCATION = os.path.join('MODIS','timeseries','multi','input')
MULTIPLE_TIMESERIES_OUTPUT_LOCATION = os.path.join('MODIS','timeseries','multi','output')


def index(request):
    return render(request, 'modis/overview.html')


def remote_sensing_datasets(request):
    return render(request, 'modis/remote_sensing_datasets.html', context={
        'dataset_list' : Dataset.objects.all().order_by("name"),
        'product_list' : Product.objects.all().order_by("name"),
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
        for d in range(range_start + day_res, 365, day_res):
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
    yg = 9.*npix - math.radians(const*lat)
    xg = math.radians(const*lon*math.cos(math.radians(lat))) + 18.*npix

    ih = int(xg/npix)
    iv = int(yg/npix)

    x = xg-ih*npix
    y = yg-iv*npix
 
    xi = int(x)
    yi = int(y)
    return ih,iv,xi,yi


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























@login_required
def single(request):
    if request.method == 'POST':
        ds = Dataset.objects.get(name__iexact=request.POST['dataset'])

        years = request.POST.getlist('years[]')
        lon = float(request.POST['lon'])
        lat = float(request.POST['lat'])

        h, v, x, y = latlon2sin(lat, lon, int(ds.xdim / ds.grid_size)) # TODO: If xdim != ydim, I have no idea how to handle that.

        #Setup task
        task = process_MODIS_single_site.s(settings.MEDIA_ROOT, SINGLE_TIMESERIES_LOCATION, ds.name, ds.location, h, v, x, y, years)    
        task.freeze()

        #Pass id from task to the create statement
        MODISSingleTimeSeriesJob.objects.create(task_id=task.id, dataset=ds, h=h, v=v, x=x, y=y, years=years, user=request.user)
        
        #Start task
        task.delay()
        return redirect('/modis/timeseries/single/t=' + task.id + '/')

    options = {}
    datasets = Dataset.objects.filter(is_global=False).order_by('name')

    for ds in datasets:
        years = glob.glob(os.path.join(ds.location, '[0-9][0-9][0-9][0-9]/'))
        years = sorted([int(y[-5:-1]) for y in years])
        options[str(ds.name)] = years

    return render(request, 'modis/single.html', context={
        "options": json.dumps(options)
    })


@login_required
def single_del(request, task_id):
    if request.method != 'POST':
        return HttpResponse()

    redir = '/modis/timeseries/single/'
    if request.POST['redirect']:
        redir = request.POST['redirect']

    try:
        task = MODISSingleTimeSeriesJob.objects.get(task_id=task_id)
    except MODISSingleTimeSeriesJob.DoesNotExist as e:
        print(e)
        print("Attempted MODIS single-site task delete but task not found")
        return redirect(redir)

    if request.user != task.user and not request.user.is_superuser:
        return redirect(redir)
    
    if task.result and task.result.name:
        os.remove(os.path.join(settings.MEDIA_ROOT, task.result.name))
    
    if task.working:
        app.control.revoke(task.task_id, terminate=True)

    task.delete()

    return redirect(redir)


@login_required
def single_status(request, task_id):
    data = {}
    data['job'] = MODISSingleTimeSeriesJob.objects.get(task_id=task_id)
    data['year_string'] = ", ".join(data['job'].years)

    data['tile'] = 'h' + str(data['job'].h).zfill(2) + 'v' + str(data['job'].v).zfill(2)
    data['pixel'] = '(' + str(data['job'].x) + ', ' + str(data['job'].y) + ")"

    return render(request, 'modis/single_status.html', context=data)


@login_required()
def single_get_progress(request, task_id):
    job = MODISSingleTimeSeriesJob.objects.get(task_id=task_id)

    res = job.result.url if job.result else ""

    return JsonResponse({'working':job.working, 'completed':job.completed, 'errored':job.errored, 'percent_complete':job.percent_complete, 'result':res})

@login_required()
def single_history(request):
    return None














@login_required
def multiple(request):
    return None


@login_required
def multiple_del(request, task_id):
    return None


@login_required
def multiple_status(request, task_id):
    return None


@login_required
def multiple_get_progress(request, task_id):
    return None


def multiple_history(request):
    return None













