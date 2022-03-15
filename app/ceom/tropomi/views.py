from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import os

from ceom.celery import app
from ceom.tropomi.models import *
from ceom.tropomi.tasks import *

SINGLE_TIMESERIES_LOCATION = os.path.join('TROPOMI','timeseries','single')
MULTIPLE_TIMESERIES_LOCATION = os.path.join('TROPOMI','timeseries','multi')


def index(request):
    return render(request, 'tropomi/index.html')


@login_required
def single(request):
    data = {}
    data['years'] = TROPOMIYearFile.objects.all().values_list('year', flat=True)

    return render(request, 'tropomi/single.html', context=data)

@login_required
def single_del(request, task_id):
    # Make sure the owner is the one deleting the task! (or admin)
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
        if data['task'].result.name[0] == '/':
            data['result_path'] = data['task'].result.name
        else:
            data['result_path'] = '/' + data['task'].result.name

    return render(request, 'tropomi/single_status.html', context=data)

@login_required
def single_start(request):
    if request.method == 'POST':
        years = request.POST.getlist('years[]')
        x = request.POST['x']
        y = request.POST['y']

        #Setup task
        task = process_TROPOMI_single_site.s(settings.MEDIA_ROOT, SINGLE_TIMESERIES_LOCATION, x, y, years)    
        task.freeze()

        #Pass id from task to the create statement
        TROPOMISingleTimeSeriesJob.objects.create(task_id=task.id, pixelx=x, pixely=y, years=years, user=request.user)
        
        #Start task
        task.delay()
        return redirect('/tropomi/timeseries/single/t=' + task.id + '/')

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
    return render(request, 'tropomi/multiple.html')

@login_required
def multiple_del(request, task_id):
    # Make sure the owner is the one deleting the task! (or admin)
    pass

@login_required
def multiple_status(request, task_id):
    pass

@login_required
def multiple_start(request):
    pass

@login_required
def multiple_get_progress(request, task_id):
    pass

@login_required
def multiple_history(request):
    return render(request, 'tropomi/multiple_history.html')
