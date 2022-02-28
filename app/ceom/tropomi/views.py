from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required
import os

SINGLE_TIMESERIES_LOCATION = os.path.join(settings.MEDIA_ROOT,'TROPOMI','timeseries','single')
MULTIPLE_TIMESERIES_LOCATION = os.path.join(settings.MEDIA_ROOT,'TROPOMI','timeseries','multi')


def index(request):
    return render(request, 'tropomi/index.html')


@login_required
def single(request):
    pass

@login_required
def single_del(request, task_id):
    pass

@login_required
def single_status(request, task_id):
    pass

@login_required
def single_start(request):
    pass

@login_required
def single_get_progress(request, task_id):
    pass

@login_required
def single_history(request):
    pass





@login_required
def multiple(request):
    pass

@login_required
def multiple_del(request, task_id):
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
    pass
