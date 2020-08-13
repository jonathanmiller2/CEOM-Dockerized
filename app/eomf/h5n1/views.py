from django.template import Context, RequestContext, loader
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from eomf.h5n1.models import Case
# Create your views here.

def index(request):
    t = loader.get_template('h5n1/index.html')
    c = RequestContext(request)
    return HttpResponse(t.render(c))

def kml(request):
    points = Case.objects.all().kml()
    
    return render_to_response('h5n1/base.kml',
        {'points' : points},
        mimetype = "application/vnd.google-earth.kml+xml")
    