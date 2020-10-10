from django.template import Context, RequestContext, loader
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from eomf.h5n1.models import Case
# Create your views here.

def index(request):
    return render(request, 'h5n1/index.html')

def kml(request):
    points = Case.objects.all().kml()
    return render(request, 'h5n1/base.kml', context={'points' : points}, mimetype = "application/vnd.google-earth.kml+xml")
    