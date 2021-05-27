from django.template import Context, RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from ceom.outreach.workshops.models import *
from django.db.models import Count
from datetime import datetime
from ceom.outreach.workshops.models import Workshop,WorkshopRegistration
from django.db import IntegrityError
# from ceom.outreach.workshops.forms import WorkshopRegistrationForm
from django.core.mail import EmailMultiAlternatives
import json


def overview(request):
    return render(request, 'workshops/overview.html')

def get_workshop_count_yearly(max_date=None,min_date=None):
    workshops = None
    if max_date:
        workshops = Workshop.objects.extra({'year':"extract(year from date_start)"}).filter(date_end__lt=max_date)
    elif min_date:
        workshops = Workshop.objects.extra({'year':"extract(year from date_start)"}).filter(date_end__gte=min_date)
    else:
        workshops = Workshop.objects.extra({'year':"extract(year from date_start)"})

    if workshops:
        return workshops.values("year").annotate(count=Count('id')).order_by('-year')
    else:
        return None
def workshop_current(request):
    years = get_workshop_count_yearly(min_date=datetime.now())
    workshops = Workshop.objects.filter(date_end__gte=datetime.now()).order_by('-date_start')
    categories = WorkshopClass.objects.all()
    return render(request, 'workshops/workshop_list_current.html', context={
         'years': years,
         'workshops':workshops,
         'total_workshops':  workshops.count,
         'categories': categories,
        }, 
    )
def workshop_past(request):
    years = get_workshop_count_yearly(max_date=datetime.now())
    workshops = Workshop.objects.filter(date_end__lt=datetime.now()).order_by('-date_end')
    categories = WorkshopClass.objects.all()
    return render(request, 'workshops/workshop_list_past.html', context={
         'years': years,
         'workshops':workshops,
         'total_workshops': workshops.count,
         'categories': categories,
        }
    )

def workshop_list_by_year_past(request,year):
    years = get_workshop_count_yearly(max_date=datetime.now())
    workshops = Workshop.objects.filter(date_start__year=year,date_end__lt=datetime.now()).order_by('-date_start')
    categories = WorkshopClass.objects.all()
    return render(request, 'workshops/workshop_list_past.html', context={
         'years': years,
         'workshops': workshops,
         'year_selected': year,
         'total_workshops': Workshop.objects.filter(date_end__lt=datetime.now()).count,
         'categories': categories,
        }, 
    )

def workshop_list_by_year_current(request,year):
    years = get_workshop_count_yearly(min_date=datetime.now())
    workshops = Workshop.objects.filter(date_start__year=year,date_end__gte=datetime.now()).order_by('-date_start')
    categories = WorkshopClass.objects.all()
    return render(request, 'workshops/workshop_list_current.html', context={
         'years': years,
         'workshops': workshops,
         'year_selected': year,
         'total_workshops':  Workshop.objects.filter(date_end__gte=datetime.now()).count,
         'categories': categories,
        }
    )

def workshop(request, workshop_id):
    try:
        workshop = Workshop.objects.get(id = workshop_id)
    except:
        return render(request, 'workshops/not_found.html')
    validated_registrations = WorkshopRegistration.objects.filter(workshop=workshop,validated=True).order_by('created')
    awaiting_validation_registrations =  WorkshopRegistration.objects.filter(workshop=workshop,validated=False)
    sponsors = SponsorInWorkshop.objects.filter(workshop=workshop)
    num_presentations = len(Presentation.objects.filter(workshop=workshop))
    num_photos = len(WorkshopPhoto.objects.filter(workshop=workshop))
    return render(request, 'workshops/workshop.html', context={
         'title':workshop.name,
         'content': workshop.content,
         'registration_enabled': workshop.registration_open,
         'workshop':workshop,
         'validated_registrations':validated_registrations,
         'awaiting_validation_registrations':awaiting_validation_registrations,
         'sponsors':sponsors,
         'show_registration':True,
         'num_presentations':num_presentations,
         'num_photos':num_photos,
        }
    )

def workshop_registration(request, workshop_id):
    try:
        workshop = Workshop.objects.get(id=workshop_id)
    except:
        return render(request, 'workshops/not_found.html')

    if not workshop.registration_open:
        return render(request, 'workshops/not_found.html')

    validated_registrations = WorkshopRegistration.objects.filter(workshop=workshop,validated=True).order_by('created')
    awaiting_validation_registrations =  WorkshopRegistration.objects.filter(workshop=workshop,validated=False)
    sponsors = SponsorInWorkshop.objects.filter(workshop=workshop)
    num_presentations = len(Presentation.objects.filter(workshop=workshop))
    num_photos = len(WorkshopPhoto.objects.filter(workshop=workshop))

    if request.method == 'POST':
        if request.POST['email'] == request.POST['verify_email']:
            try:
                registration = WorkshopRegistration.objects.create(
                    workshop=workshop,
                    first_name=request.POST['first_name'], 
                    last_name=request.POST['last_name'], 
                    institution=request.POST['institution'], 
                    position=request.POST['position'], 
                    address=request.POST['address'], 
                    area_of_expertise=request.POST['area_of_expertise'], 
                    email=request.POST['email'], 
                    verify_email=request.POST['verify_email'], 
                    phone=request.POST['phone'], 
                    validated=False
                )
            except IntegrityError as error:
                error='Duplicate Account'
                # return HttpResponse("ERROR: Same account already exists!")
                return render(request, 'workshops/registration.html', context={
                    'title':workshop.name,
                    'error':error,
                    'content': workshop.content,
                    'workshop_reg':workshop,
                    'validated_registrations':validated_registrations,
                    'awaiting_validation_registrations':awaiting_validation_registrations,
                    'workshop':workshop,
                    'sponsors':sponsors,
                    'show_registration':False,
                    'num_presentations':num_presentations,
                    'num_photos':num_photos,
                    },  
                )
        else: 
            error='Email-mismatch'
            #return HttpResponse("ERROR: Email mismatch")
            return render(request, 'workshops/registration.html', context={
                'title':workshop.name,
                'error':error,
                'content': workshop.content,
                'workshop_reg':workshop,
                'validated_registrations':validated_registrations,
                'awaiting_validation_registrations':awaiting_validation_registrations,
                'workshop':workshop,
                'sponsors':sponsors,
                'show_registration':False,
                'num_presentations':num_presentations,
                'num_photos':num_photos,
                },  
            )

    return render(request, 'workshops/registration.html', context={
         'title':workshop.name,
         'content': workshop.content,
         'workshop_reg':workshop,
         'validated_registrations':validated_registrations,
         'awaiting_validation_registrations':awaiting_validation_registrations,
         'workshop':workshop,
         'sponsors':sponsors,
         'show_registration':False,
         'num_presentations':num_presentations,
         'num_photos':num_photos,
        },  
    )

def presentations(request, workshop_id):
    try:
        workshop = Workshop.objects.get(id = workshop_id)
    except:
        return render(request, 'workshops/not_found.html', {})
    sponsors = SponsorInWorkshop.objects.filter(workshop=workshop)
    presentations = Presentation.objects.filter(workshop=workshop)
    num_photos = len(WorkshopPhoto.objects.filter(workshop=workshop))
    return render(request, 'workshops/workshop_presentations.html', context={
         'title':workshop.name,
         'content': workshop.content,
         'workshop':workshop,
         'sponsors':sponsors,
         'show_registration':True,
         'presentations':presentations,
         'num_presentations':len(presentations),
         'num_photos':num_photos,
        }, 
        
    )

def photos(request, workshop_id):
    try:
        workshop = Workshop.objects.get(id = workshop_id)
    except:
        return render(request, 'workshops/not_found.html', {})
    sponsors = SponsorInWorkshop.objects.filter(workshop=workshop)
    presentations = len(Presentation.objects.filter(workshop=workshop))
    photos = WorkshopPhoto.objects.filter(workshop=workshop).order_by("priority")
    return render(request, 'workshops/photos.html', context={
         'title':workshop.name,
         'content': workshop.content,
         'workshop':workshop,
         'sponsors':sponsors,
         'show_registration':True,
         'num_presentations':presentations,
         'num_photos':len(photos),
         'photos':photos,
        }, 
        
    )