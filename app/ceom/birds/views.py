from django.template import Context, loader
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from ceom.birds.models import DuckTrack, DuckTrackLine
# Create your views here.

def index(request):
    return render(request, 'birds/index.html')

def kml(request):
    points = DuckTrack.objects.all().kml()
    #test = points[0].kml
    return render(request, 'birds/base.kml', context={'points' : points}, mimetype="application/vnd.google-earth.kml+xml")
    
