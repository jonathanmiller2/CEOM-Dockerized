from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import os, csv
from datetime import datetime

from ceom.celery import app
from ceom.tropomi.models import *
from ceom.tropomi.tasks import *

SINGLE_TIMESERIES_LOCATION = os.path.join('TROPOMI','timeseries','single')
MULTIPLE_TIMESERIES_INPUT_LOCATION = os.path.join('TROPOMI','timeseries','multi','input')
MULTIPLE_TIMESERIES_OUTPUT_LOCATION = os.path.join('TROPOMI','timeseries','multi','output')


def index(request):
    return render(request, 'tropomi/index.html')


@login_required
def single(request):
    data = {}
    data['years'] = TROPOMIYearFile.objects.all().values_list('year', flat=True)

    if request.method == 'POST':
        requested_years = request.POST.getlist('years[]')
        x = request.POST['x']
        y = request.POST['y']

        #Setup task
        task = process_TROPOMI_single_site.s(settings.MEDIA_ROOT, SINGLE_TIMESERIES_LOCATION, x, y, requested_years)    
        task.freeze()

        #Pass id from task to the create statement
        TROPOMISingleTimeSeriesJob.objects.create(task_id=task.id, pixelx=x, pixely=y, years=requested_years, user=request.user)
        
        #Start task
        task.delay()
        return redirect('/tropomi/timeseries/single/t=' + task.id + '/')

    return render(request, 'tropomi/single.html', context=data)

@login_required
def single_del(request, task_id):
    if request.method != 'POST':
        return HttpResponse()

    redir = '/tropomi/timeseries/single/'
    if request.POST['redirect']:
        redir = request.POST['redirect']

    try:
        task = TROPOMISingleTimeSeriesJob.objects.get(task_id=task_id)
    except TROPOMISingleTimeSeriesJob.DoesNotExist as e:
        print(e)
        print("Attempted TROPOMI single-site task delete but task not found")
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
    data['task'] = TROPOMISingleTimeSeriesJob.objects.get(task_id=task_id)
    data['year_string'] = ", ".join(data['task'].years)
    
    if data['task'].result:
        data['result_path'] = os.path.join(settings.MEDIA_URL, data['task'].result.name)

    return render(request, 'tropomi/single_status.html', context=data)

@login_required
def single_get_progress(request, task_id):
    task = TROPOMISingleTimeSeriesJob.objects.get(task_id=task_id)

    if task.result:
        result_location = os.path.join(settings.MEDIA_URL, task.result.name)
    else:
        result_location = ""

    return JsonResponse({'working':task.working, 'completed':task.completed, 'errored':task.errored, 'percent_complete':task.percent_complete, 'result':result_location})


@login_required
def single_history(request):
    user_tasks = TROPOMISingleTimeSeriesJob.objects.filter(user=request.user).order_by('-created')
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
    return render(request, 'tropomi/single_history.html', context={
        "jobs": jobs,
        'paginator': paginator,
        'page_range': page_range,
        })





@login_required
def multiple(request):
    data = {}
    data['years'] = TROPOMIYearFile.objects.all().values_list('year', flat=True)

    if request.method == 'POST':
        requested_years = request.POST.getlist('years')

        if 'inputfile' not in request.FILES:
            data['error'] = "Please select an input file"
            return render(request, 'tropomi/multiple.html', context=data)

        if len(requested_years) == 0:
            data['error'] = "Please select the desired years for the dataset"
            return render(request, 'tropomi/multiple.html', context=data)

        input_file = request.FILES['inputfile']

        #Verify file
        MAX_BLANK_ROWS=100
        MAX_SITES_PER_FILE=100
        try:
            dialect = csv.Sniffer().sniff(input_file.read(1024).decode('utf-8'))
            input_file.seek(0, 0)
        except csv.Error:
            data['error'] = 'Not a valid CSV file'
            return render(request, 'tropomi/multiple.html', context=data)

        reader = csv.reader(input_file.read().decode('utf-8').splitlines(), dialect, delimiter=',')
        i=1
        blank_rows=0
        for y_index, row in enumerate(reader):
            if i > MAX_SITES_PER_FILE:
                data['error'] = "The limit of sites per request is "+ str(MAX_SITES_PER_FILE)+". Please split the file in smaller chunks."
                return render(request, 'tropomi/multiple.html', context=data)
            if not ''.join(str(x) for x in row):
                blank_rows+=1
                if blank_rows>= MAX_BLANK_ROWS:
                    data['error'] = 'Too many blank rows in file. Please delete them'
                    return render(request, 'tropomi/multiple.html', context=data)
                continue
            if len(row) != 3:
                data['error'] = "Format error at line " + str(i) + ": More/less than three columns detected. " + str(row)
                return render(request, 'tropomi/multiple.html', context=data)
            try:
                a = float(row[1])
                a = float(row[2])
            except Exception:
                data['error'] = "Format error at line " + str(i) + ": latitude and longitude must be in number format eg: 12.1234. " + str(row)
                return render(request, 'tropomi/multiple.html', context=data)
            i+=1
        #File verified

        full_input_dir = os.path.join(settings.MEDIA_ROOT, MULTIPLE_TIMESERIES_INPUT_LOCATION)
        if not os.path.exists(full_input_dir):
            os.makedirs(full_input_dir)

        filename = 'TROPOMI_Input_uid' + str(request.user.id) + "_" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".csv"
        rel_input_file_location = os.path.join(MULTIPLE_TIMESERIES_INPUT_LOCATION, filename)

        with open(os.path.join(settings.MEDIA_ROOT, rel_input_file_location), 'wb+') as destination:
            for chunk in input_file.chunks():
                destination.write(chunk)

        #Setup task
        task = process_TROPOMI_multiple_site.s(settings.MEDIA_ROOT, MULTIPLE_TIMESERIES_OUTPUT_LOCATION, rel_input_file_location, requested_years)    
        task.freeze()

        #Pass id from task to the create statement
        obj = TROPOMIMultipleTimeSeriesJob.objects.create(task_id=task.id, years=requested_years, user=request.user)
        obj.points.name = rel_input_file_location
        obj.save()
        
        #Start task
        task.delay()
        return redirect('/tropomi/timeseries/multiple/t=' + task.id + '/')


    return render(request, 'tropomi/multiple.html', context=data)

@login_required
def multiple_del(request, task_id):
    if request.method != 'POST':
        return HttpResponse()

    redir = '/tropomi/timeseries/multiple/'
    if request.POST['redirect']:
        redir = request.POST['redirect']

    try:
        task = TROPOMIMultipleTimeSeriesJob.objects.get(task_id=task_id)
    except TROPOMIMultipleTimeSeriesJob.DoesNotExist as e:
        print(e)
        print("Attempted TROPOMI multiple-site task delete but task not found")
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
def multiple_status(request, task_id):
    data = {}
    print(task_id)
    data['task'] = TROPOMIMultipleTimeSeriesJob.objects.get(task_id=task_id)
    data['year_string'] = ", ".join(data['task'].years)
    
    if data['task'].points:
        data['input_path'] = os.path.join(settings.MEDIA_URL, data['task'].points.name)

    if data['task'].result:
        data['result_path'] = os.path.join(settings.MEDIA_URL, data['task'].result.name)

    return render(request, 'tropomi/multiple_status.html', context=data)

@login_required
def multiple_get_progress(request, task_id):
    pass

@login_required
def multiple_history(request):
    return render(request, 'tropomi/multiple_history.html')
