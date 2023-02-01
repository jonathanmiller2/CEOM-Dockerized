# Create your views here.
from django.template import Context, RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from ceom.aboutus.models import Post, Person, GalleryPhoto, Publication
from django.contrib.auth.models import User
from ceom.photos.models import Photo
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

def publications(request):
    pubs = Publication.objects.all().order_by('-date')

    if request.GET:
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

def user_stats(request):
    data = {}
    request_list = request.GET.getlist('p')
    type = request_list[0]
    if len(request_list) == 1:
        year_min = 2007
        year_max = date.today().year
    else: 
        year_min = int(request_list[1]) 
        year_max = int(request_list[2])  
    data['x_values'] = list(range(year_min, year_max+1))
    data['year_range'] = range(2007, date.today().year+1)
    data['type'] = type
    
    y_values = []
    if type == 'new':
        for year in range(year_min, year_max+1):
            y_values.append(User.objects.filter(date_joined__year=year).count())
    elif type == 'cum':
        for year in range(year_min, year_max+1):
            y_values.append(User.objects.filter(date_joined__year__lte=year).count())
    elif type == 'month':
        for month in range(1,13):
            data_by_month = []
            for year in range(year_min, year_max+1):
                data_by_month.append(User.objects.filter(date_joined__month = month, date_joined__year = year).count())
            y_values.append(data_by_month)
    
    data['y_values'] = y_values
    return render(request, 'aboutus/user_chart.html', context=data)


def photo_stats(request):
    data = {}
    request_list = request.GET.getlist('p')
    type = request_list[0]
    if len(request_list) == 1:
        year_min = 2007
        year_max = date.today().year
    else: 
        year_min = int(request_list[1]) 
        year_max = int(request_list[2])  
    data['x_values'] = list(range(year_min, year_max+1))
    data['year_range'] = range(2007, date.today().year+1)
    data['type'] = type
    
    y_values = []
    if type == 'cum':
        for year in range(year_min, year_max+1):
            y_values.append(Photo.objects.filter(uploaddate__year__lte=year).count())
    elif type == 'month':
        for month in range(1,13):
            data_by_month = []
            for year in range(year_min, year_max+1):
                data_by_month.append(Photo.objects.filter(uploaddate__month = month, uploaddate__year = year).count())
            y_values.append(data_by_month)
    
    data['y_values'] = y_values
    return render(request, 'aboutus/photo_chart.html', context=data)
