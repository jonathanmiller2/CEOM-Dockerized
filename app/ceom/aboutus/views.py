# Create your views here.
from django.template import Context, RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from ceom.aboutus.models import Post, Person, GalleryPhoto
from itertools import chain
from operator import attrgetter
from datetime import date

from ceom.celery import debug_normal_task, debug_shared_task

def news(request):
    debug_shared_task.delay()
    debug_normal_task.delay()

    posts = Post.objects.all().order_by("-date")
    return render(request, 'aboutus/news.html', context={'posts': posts})

def people(request):
    data = {}

    data['people'] = Person.objects.all().order_by('category__order', 'order', 'last_name')
    
    return render(request, 'aboutus/people.html', context=data)

def group_photos(request, selYear = None):
    available_years=GalleryPhoto.objects.all().values_list('year', flat=True).order_by('-year')
    photos= None
    if selYear == None and len(available_years)>0  :
        selYear= available_years[0]
    if selYear:
        photos = GalleryPhoto.objects.all().filter(year=selYear).order_by('-year','order')
    return render(request, 'aboutus/group_photos.html', context={
        'available_years' : available_years,
        'photos': photos,
    })
    
    
     
    
   
