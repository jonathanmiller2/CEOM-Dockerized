from django.template import Context, RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.core.files.base import ContentFile
from ceom.modis.inventory.models import Dataset
from ceom.photos.models import Category, Photo
from ceom.modis.visualization.models import TimeSeriesJob,  SingleTimeSeriesJob, GeocatterPoint
from ceom.modis.visualization.forms import ProductSelect, TimeSeriesJobForm
from datetime import datetime, date, timedelta

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

## testing the new celery task for collection-6 data
from ceom.celeryq.tasks_c6 import get_modis_raw_data_c6, latlon2sin

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

def manual(request):
    return render(request, 'visualization/manual.html')

def olmap(request):
    form = ProductSelect()
    products = ['EVI', 'LSWI', 'NDSI', 'NDVI', 'NDWI', 'SNOW']
    days = list(range(1, 362, 8))
    years = list(range(2000, datetime.now().year+1))
    return render(request, 'visualization/olmap.html', context={
        "product_form":form,
        "products": products,
        "days": days,
        "years": years,
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

## TEMP FOR COLLECTION-6 DATASET
@login_required()
def launch_single_site_timeseries_c6(request, lat, lon, dataset, years, product=None):
    years_formated = [int(year) for year in years.split(',')]
    dataset_freq_in_days = 8
    try:
        dataset = Dataset.objects.get(name=dataset)
        dataset_npix = dataset.xdim #2400 for mod09a1
        dataset_freq_in_days = dataset.day_res # 8 for mod09a1
    except Exception as e:
        return HttpResponse("An error occurred. If you did not modify the URL please contact the web administrator")

    csv_folder = TIMESERIES_LOCATION
    lon=float(lon)
    lat = float(lat)
    dataset_npix = int(dataset_npix)
    ih,iv,xi,yi,folder = latlon2sin(lat,lon,dataset,dataset_npix)
    

    vi=False
    media_timeseries = os.path.join(settings.MEDIA_URL,'visualization','timeseries','single')
    task_id = get_modis_raw_data_c6.delay(csv_folder,media_timeseries,lat,lon,dataset.name,years_formated,dataset_npix,dataset_freq_in_days)

    job = SingleTimeSeriesJob(lat=lat,lon=lon,user=request.user,years=years,product=dataset,task_id=task_id,col=xi,row=yi,tile=folder)
    job.save()
    return redirect(to='/visualization/timeseries/single/t=%s'%task_id)

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
    print("IH:",ih,"IV:", iv,"XI:", xi,"YI:", yi,"FOLDER:", folder)
    vi=False
    print("TIME",TIMESERIES_LOCATION)
    task_id = get_modis_raw_data.delay(TIMESERIES_LOCATION,lat,lon,dataset.name,years_formated,dataset_npix,dataset_freq_in_days)     

    print("toast 231")

    job = SingleTimeSeriesJob(lat=lat,lon=lon,user=request.user,years=years,product=dataset,task_id=task_id,col=xi,row=yi,tile=folder)

    print("toast 235")

    job.save()

    print("toast 239")

    return redirect(to='/modis/visualization/timeseries/single/t=%s/'%task_id)

# This page will host all single timeseries from a user
@login_required()
def timeseries_single_history(request):
    user_tasks = SingleTimeSeriesJob.objects.filter(user=request.user).order_by('-created')
    paginator = Paginator(user_tasks, 25) # Show 25 jobs per page

    page = request.GET.get('page')
    try:
        jobs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        jobs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        jobs = paginator.page(paginator.num_pages)
    return render(request, 'visualization/single_timeseries_history.html', context={"jobs": jobs})

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

def get_multiple_task_progress(request,tasks_ids):
    try:
        if not tasks_ids:
            raise Exception('Task List is empty')
        tasks = TimeSeriesJob.objects.filter(Q(user=request.user)&Q(reduce(lambda x, y: x | y, [Q(id__contains=task_id) for task_id in tasks_ids])))
        tasks_dict = [(t.toJSON()) for t in tasks]
        return JsonResponse({'tasks':tasks_dict,'success':True})
    except Exception as e:
        return JsonResponse({'success':False,'message':'Unhandled exception: %s' % e})


def timeseries_single_chart(request,task_id):
    # # absolute_path = '/webapps/ceom_admin/ceom-prod/ceom/media/visualization/timeseries/single/a00ad01b-397c-432b-adc7-d88194b47477.csv'
    # # data = read_from_csv(absolute_path)
    # # query=None
    # # for row in data:
    # #     for key, value in data.items():
    # #         if query is None:
    # #             query = Q(**{key + "__icontains" : value})
    # #         else:
    # #             query |= Q(**{key + "__icontains" : value})
    # # rainpivotdata = \
    # #     DataPool(
    # #        series=
    # #         [{'options': {
    # #            'source': query},
    # #           'terms': [
    # #             'Date',
    # #             'GF_NDVI',
    # #             'GF_EVI']}
    # #          ])

    # # #Step 2: Create the PivotChart object
    # # rainpivcht = \
    # #     Chart(
    # #         datasource = rainpivotdata,
    # #         series_options =
    # #             [{'options':{
    # #               'type': 'line',
    # #               'stacking': False},
    # #             'terms':{
    # #               'Date': [
    # #                 'GF_NDVI',
    # #                 'GF_EVI']
    # #               }}],
    # #         chart_options =
    # #           {'title': {
    # #                'text': 'Weather Data of Boston and Houston'},
    # #            'xAxis': {
    # #                 'title': {
    # #                    'text': 'Month number'}}})

    # # #Step 3: Send the PivotChart object to the template.
    # t = loader.get_template('visualization/single_site_timeseries_chart.html')
    # c = RequestContext(request, {})
    # return HttpResponse(t.render(c))
    # return render_to_response({'rainpivchart': rainpivcht})
    return HttpResponse('Under construction')

def csv_content(request, lat, lon, modis, years, product=None):
    # ds = Dataset.objects.filter(name=modis)[0]
    # response = HttpResponse(process.ascii(lat, lon, modis, years, ',',npix=int(ds.xdim)))
    # response["Content-Disposition"]= "attachment"
    # return response
    response = HttpResponse('Under construction')
    return response

def csv_products(request, lat, lon, modis, years, product=None):
    # ds = Dataset.objects.filter(name=modis)[0]
    # raw_csv = process.ascii(lat, lon, modis, years, ',',npix=int(ds.xdim))
    # products_csv = process.csv_add_products(raw_csv)
    # filename = modis+'_prod_'+years+"_lat_"+str(lat)+"_lon_"+str(lon)
    # response = HttpResponse(content_type='text/csv')
    # response['Content-Disposition'] = 'attachment; filename="'+filename+'.csv"'
    # my_writer = csv.writer(response)
    # lines = str.splitlines(products_csv)

    # for line in lines:
    #     data_to_write = str.split(line,',')
    #     my_writer.writerow(data_to_write)
    response = HttpResponse('Under construction')
    return response

def csv_products_graphs(request, lat, lon, modis, years, product=None):
    # ds = Dataset.objects.filter(name=modis)[0]
    # raw_csv = process.ascii(lat, lon, modis, years, ',',npix=int(ds.xdim))
    # products_csv = process.csv_add_products(raw_csv)
    # filename = modis+'_prod_'+years+"_lat_"+str(lat)+"_lon_"+str(lon)
    # response = HttpResponse(content_type='text/csv')
    # response['Content-Disposition'] = 'attachment; filename="'+filename+'.csv"'
    # my_writer = csv.writer(response)
    
    # lines = str.splitlines(products_csv)
    # lines = map(lambda x: str.split(x,','),lines)
    # for line in lines:
    #     data_to_write=[]
    #     for i in xrange(0,len(line)):
    #         if 'Date' in lines[0][i] or 'GF_' in line[i]:
    #             data_to_write.append(line[i])
    #         elif 'GF_' in lines[0][i]:
    #             value = float(line[i])
    #             value = max(value,float(-1.0))
    #             value = min(value,float(1.0))
    #             data_to_write.append(value)
    #     my_writer.writerow(data_to_write)
    response = HttpResponse('Under construction')
    return response

def graphlist(request, lat, lon, modis, years, product=None):
    # year_r = years.split(',')
    # year = year_r[0]

    # ds = Dataset.objects.filter(name=modis)[0]
    # npix = int(ds.xdim)

    # ih, iv, xi, yi, folder = process.latlon2sin(float(lat), float(lon),modis,npix)
    # files = glob.glob("/data/vol01/modis/%s/%s/%s/*.hdf" % (modis, year, folder))
    # if len(files) > 0:
    #     files.sort()
    #     f = nio.open_file(files[0])
    #     keys = f.variables.keys()
    #     keys.reverse()
    #     f.close()

    #     t = loader.get_template('visualization/graph.html')
    #     c = RequestContext(request, {"lat": lat,
    #                  "lon": lon,
    #                  "modis": modis,
    #                  "tile": folder,
    #                  "row": yi,
    #                  "col": xi,
    #                  "years": years,
    #                  "keys": keys,
    #                 })

    #     return HttpResponse(t.render(c))
    # else:
    #     t = loader.get_template('base.html')
    #     c = RequestContext(request, {'content_raw': "Data not found"})
    #     return HttpResponse(t.render(c))
    response = HttpResponse('Under construction')
    return response

def graphlist_js(request, lat, lon, modis, years, product=None):
    # year_r = years.split(',')
    # year = year_r[0]

    # ds = Dataset.objects.filter(name=modis)[0]
    # npix = int(ds.xdim)

    # ih, iv, xi, yi, folder = process.latlon2sin(float(lat), float(lon),modis,npix)
    # files = glob.glob("/data/vol01/modis/%s/%s/%s/*.hdf" % (modis, year, folder))
    # if len(files) > 0:
    #     files.sort()
    #     f = nio.open_file(files[0])
    #     keys = f.variables.keys()
    #     keys.reverse()
    #     f.close()

    #     visibility = str(map(lambda x: "refl_b" in x, keys)+[False])

    #     t = loader.get_template('visualization/graph-js.html')
    #     c = RequestContext(request, {"lat": lat,
    #                  "lon": lon,
    #                  "modis": modis,
    #                  "tile": folder,
    #                  "row": yi,
    #                  "col": xi,
    #                  "years": years,
    #                  "keys": keys,
    #                  "visibility": visibility })

    #     return HttpResponse(t.render(c))
    # else:
    #     t = loader.get_template('base.html')
    #     c = RequestContext(request, {'content_raw': "Data not found"})
    #     return HttpResponse(t.render(c))
    response = HttpResponse('Under construction')
    return response

def graphlist_js_prod(request, lat, lon, modis, years, product=None):
    # ds = Dataset.objects.filter(name=modis)[0]
    # npix = int(ds.xdim)
    # ih, iv, xi, yi, folder = process.latlon2sin(float(lat), float(lon),modis,npix)
    # keys = ["Date","Surface_reflectance_for_band_1","Surface_reflectance_for_band_2","Surface_reflectance_for_band_3","Surface_reflectance_for_band_4","Surface_reflectance_for_band_5","Surface_reflectance_for_band_6","Surface_reflectance_for_band_7","Surface_reflectance_500m_quality_control_flags","Solar_zenith","View_zenith","Relative_azimuth","Surface_reflectance_500m_state_flags","Surface_reflectance_day_of_year","actual_date","red","nir1","blue","green","nir2","swir1","swir2","NDVI","EVI","LSWI","NDSI","NDWI1200","sur_refl_state_500m","MOD35 cloud","cloud shadow","land/water flag","aerosol quantity","cirrus detected","internal cloud algorithm flag","internal fire algorithm flag","MOD35 snow/ice flag","Pixel is adjacent to cloud","BRDF correction performed","internal snow algorithm flag","Gap_fill_applied","GF_NDVI","GF_EVI","GF_LSWI","GF_NDSI","GF_NDWI1200"]
    # visibility = str(map(lambda x: "GF_" in x, keys))
    # t = loader.get_template('visualization/graph-js2.html')
    # c = RequestContext(request, {"lat": lat,
    #                 "lon": lon,
    #                 "modis": modis,
    #                 "tile": folder,
    #                 "row": yi,
    #                 "col": xi,
    #                 "years": years,
    #                 "keys": keys,
    #                 "visibility": visibility,})

    # return HttpResponse(t.render(c))
    response = HttpResponse('Under construction')
    return response
    
def graph(request, lat, lon, modis, years, band, product=None):

    # from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    # from matplotlib.figure import Figure
    # from matplotlib.dates import DateFormatter
    # from matplotlib.ticker import FixedLocator

    # ds = Dataset.objects.filter(name=modis)[0]
    # npix = int(ds.xdim)
    # year_r = years.split(',')
    # ih, iv, xi, yi, folder = process.latlon2sin(float(lat), float(lon), modis, npix)
    # values = {}

    # #Collect data from HDF files, by date
    # for year in year_r:
    #     flist = glob.glob("/data/vol01/modis/%s/%s/%s/*.hdf" % (modis, year, folder))
    #     if len(flist) > 0:
    #         flist.sort()
    #         r = re.compile(".*A(?P<year>\d{4})(?P<day>\d{3}).*")

    #         x=[]
    #         y=[]

    #         for fn in flist:
    #             m = r.match(fn)
    #             if m is not None:
    #                 x.append(int(m.group('day')))
    #                 fh = nio.open_file(fn)
    #                 y.append(int(fh.variables[band][yi][xi]))
    #                 fh.close()

    #         values[int(year)] = {'x':x,'y':y}


    # if len(values) > 0:
    #         fig=Figure(figsize=(9,5), edgecolor='w', facecolor='w')
    #         ax=fig.add_subplot(111, title="Band: "+band)
    #         ax.set_xlabel("day")
    #         if (band[-3:-1] == 'b0'):
    #             ax.set_ylabel("reflectance")

    #         for year in sorted(values.keys()):
    #             ax.plot(values[year]['x'], values[year]['y'],'o-',label=str(year))

    #         ax.legend(loc='best')
    #         ax.set_xlim([1,361])
    #         ax.xaxis.set_major_locator(FixedLocator(range(1,362,8)))
    #         for tick in ax.xaxis.get_major_ticks():
    #             tick.label1.set(rotation=90, fontsize=10)
    #         ax.grid(b=True)
    #         #ax.set(edgecolor='w')
    #         canvas=FigureCanvas(fig)
    #         response=HttpResponse(content_type='image/png')
    #         canvas.print_png(response)
    #         return response
    # else:
    #     t = loader.get_template('base.html')
    #     c = RequestContext(request, {'content_raw': "Data not found"})
    #     return HttpResponse(t.render(c))
    response = HttpResponse('Under construction')
    return response

MULTIPLE_TIMESERIES_LOCATION = os.path.join(settings.MEDIA_ROOT,'visualization','timeseries','multi')

@login_required
def multiple(request):
    user_tasks = TimeSeriesJob.objects.filter(user=request.user).order_by('-timestamp')
    paginator = Paginator(user_tasks, 25) # Show 25 jobs per page

    page = request.GET.get('page')
    try:
        jobs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        jobs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        jobs = paginator.page(paginator.num_pages)
    task_in_progress = any([job.working for job in jobs])
    return render(request, 'visualization/multiple.html', context={"task_in_progress":task_in_progress, 'jobs':jobs})
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
        message="You can only have a maximum of two pending jobs in the queue. Please wait at least for the first to finish or cancel any of them."
        user_timeseries = TimeSeriesJob.objects.filter(user=request.user).order_by('-timestamp')
        return render(request, 'visualization/multiple.html', context={"title":"Multiple Points Time Series Tool", 'timeseries':user_timeseries,"message":message})
   
    if request.method == 'POST':
        form = TimeSeriesJobForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save_data(request.user,'')

            csv_folder = MULTIPLE_TIMESERIES_LOCATION
            media_timeseries = os.path.join(settings.MEDIA_URL,'visualization','timeseries','multi')
            years = [int(y) for y in form.cleaned_data['years'].split(',')]
            points = job.points.file.name
            dataset = form.cleaned_data['product']

            task_id = multiple_site_modis.delay(points,csv_folder,media_timeseries,dataset.name,years,dataset.xdim,dataset.day_res)
            job.task_id = task_id
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