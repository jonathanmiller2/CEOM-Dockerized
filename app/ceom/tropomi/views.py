from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
import os

from ceom.tropomi.models import *
from ceom.tropomi.tasks import *

SINGLE_TIMESERIES_LOCATION = os.path.join(settings.MEDIA_ROOT,'TROPOMI','timeseries','single')
MULTIPLE_TIMESERIES_LOCATION = os.path.join(settings.MEDIA_ROOT,'TROPOMI','timeseries','multi')


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
    pass

@login_required
def single_status(request, task_id):
    data = {}
    data['task'] = TROPOMISingleTimeSeriesJob.objects.get(task_id=task_id)
    data['year_string'] = ", ".join(data['task'].years)

    return render(request, 'tropomi/single_status.html', context=data)

@login_required
def single_start(request):
    if request.method == 'POST':
        years = request.POST.getlist('years[]')
        x = request.POST['x']
        y = request.POST['y']

        #Start task
        task = process_TROPOMI_single_site.delay(SINGLE_TIMESERIES_LOCATION, x, y, years)    

        #Pass id from starting task to the create statement
        TROPOMISingleTimeSeriesJob.objects.create(task_id=task.id, pixelx=x, pixely=y, years=years, user=request.user)
        print(task.id)
        return redirect('/tropomi/timeseries/single/t=' + task.id + '/')

    pass

@login_required
def single_get_progress(request, task_id):
    pass

@login_required
def single_history(request):
    return render(request, 'tropomi/single_history.html')





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
