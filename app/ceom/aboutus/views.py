# Create your views here.
from django.template import Context, RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from ceom.aboutus.models import Post, Person, GalleryPhoto, Publication
from itertools import chain
from operator import attrgetter
from datetime import date

def news(request):
    posts = Post.objects.all().order_by("-date")
    return render(request, 'aboutus/news.html', context={'posts': posts})

def people(request):
    data = {}

    data['people'] = Person.objects.all().order_by('category__order', 'order', 'last_name')
    
    return render(request, 'aboutus/people.html', context=data)

#def index(request):
#    pubs = Publication.objects.all().order_by('-date')
    #pubs.reverse()

#    if 'type' in request.GET:
#        pubs = pubs.filter(pubtype=str(request.GET['type']))

#    years = dict()
#    for pub in pubs:
#        if pub.year:
#            year = pub.year
#        else:
#            year = pub.date.year

#        year_list = years.get(year, [])
#        year_list.append(pub)
#        years[year] = year_list

#    print(years)

#    return render(request, 'publications/section_list.html', context={'section_list': years})

def publications(request):
    print("Hi:)")
    pubs = Publication.objects.all().order_by('-date')

    if 'type' in request.GET:
        pubs = pubs.filter(pubtype=str(request.GET['type']))

    years = dict()
    for pub in pubs:
        if pub.year:
            year = pub.year
        else:
            year = pub.date.year

        year_list = years.get(year, [])
        year_list.append(pub)
        years[year] = year_list

    print(years)
    print(pubs)
        
    return render(request, 'aboutus/section_list.html', context={'section_list': years})


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
    
    
     
    
   
