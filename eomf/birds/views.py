from django.template import Context, loader
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from models import DuckTrack, DuckTrackLine
# Create your views here.

def index(request):
    t = loader.get_template('birds/index.html')
    c = Context()
    return HttpResponse(t.render(c))

def kml(request):
    points = DuckTrack.objects.all().kml()
    #test = points[0].kml
    return render_to_response('birds/base.kml',{'points' : points},
        mimetype = "application/vnd.google-earth.kml+xml")
    
