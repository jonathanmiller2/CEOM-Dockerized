# Create your views here.
from django.template import Context, RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from ceom.aboutus.models import Post, Group, Person, GalleryPhoto
from itertools import chain
from operator import attrgetter
from datetime import date

def news(request):
    #~ available_dates = Post.objects.dates('date','year').distinct()
    #~ available_years = []
    #~ for idx,date in enumerate(available_dates):
        #~ available_years.append(date.year)
    #~ if post_year:
        posts = Post.objects.all().order_by("-date")
        return render(request, 'aboutus/news.html', context={'posts': posts})
    #~ elif post_id:
        #~ try:
#~ 
            #~ post = Post.objects.get(id=post_id) 
            #~ posts = Post.objects.all().filter(date__year=post.date__year).order_by("-date")
            #~ #post_year= post.date__year 
            #~ post_year=2013
            #~ #post_year =  posts.values('date__year')[0]   
            #~ return render_to_response('aboutus/news.html', {
                #~ 'posts': posts,
                #~ 'year':post_year,
                #~ 'post_id':None,
                #~ 'available_years':available_years,
                #~ },context_instance=RequestContext(request)
        #~ )
        #~ except:
            #~ return render_to_response('aboutus/notfound.html', {}, context_instance=RequestContext(request))
    #~ else:
        #~ posts = Post.objects.all().order_by("-date")
        #~ post_year = 2013
        #~ return render_to_response('aboutus/news.html', {
            #~ 'posts': posts,
            #~ 'year':post_year,
            #~ 'post_id':None,
            #~ 'available_years':available_years,
            #~ },context_instance=RequestContext(request)
        #~ )

def people(request):
    people = Person.objects.all().order_by('group__order', 'alumni_group__order','order', 'last_name')
    return render(request, 'aboutus/people.html', context={
        'people': people,
        'cu':[1,2,3,4,5,6,7,8,9],
        'alum':[10,11,12,13,14,15,16,17,18,19],
    })

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
    
    
     
    
   
