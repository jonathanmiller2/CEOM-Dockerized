from django.shortcuts import render

# Create your views here.
# Create your views here.
from django.template import Context, RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from models import Post, Group, Person, GalleryPhoto
from itertools import chain
from operator import attrgetter
from datetime import date

def index(request):
    t = loader.get_template('water/overview.html')
    c = RequestContext(request)
    return HttpResponse(t.render(c))

    
     
    
   
