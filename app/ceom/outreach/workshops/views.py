from django.template import Context, RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from ceom.outreach.workshops.models import *
from ceom.outreach.gisday.models import Year
from django.db.models import Count
from datetime import datetime
from ceom.outreach.workshops.models import Workshop,WorkshopRegistration
from django.db import IntegrityError
from django.core.mail import EmailMultiAlternatives
import json, csv


def overview(request):
    available_years = Year.objects.filter(hidden=False).order_by('-date')
    return render(request, 'workshops/overview.html', context={
         'available_years': available_years,
    })

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
    available_years = Year.objects.filter(hidden=False).order_by('-date')
    years = get_workshop_count_yearly(min_date=datetime.now())
    workshops = Workshop.objects.filter(date_end__gte=datetime.now()).order_by('-date_start')
    categories = WorkshopClass.objects.all()
    return render(request, 'workshops/workshop_list_current.html', context={
         'available_years': available_years,
         'years': years,
         'workshops':workshops,
         'total_workshops':  workshops.count,
         'categories': categories,
        }, 
    )
def workshop_past(request):
    available_years = Year.objects.filter(hidden=False).order_by('-date')
    years = get_workshop_count_yearly(max_date=datetime.now())
    workshops = Workshop.objects.filter(date_end__lt=datetime.now()).order_by('-date_end')
    categories = WorkshopClass.objects.all()
    return render(request, 'workshops/workshop_list_past.html', context={
         'available_years': available_years,
         'years': years,
         'workshops':workshops,
         'total_workshops': workshops.count,
         'categories': categories,
        }
    )

def workshop_list_by_year_past(request,year):
    available_years = Year.objects.filter(hidden=False).order_by('-date')
    years = get_workshop_count_yearly(max_date=datetime.now())
    workshops = Workshop.objects.filter(date_start__year=year,date_end__lt=datetime.now()).order_by('-date_start')
    categories = WorkshopClass.objects.all()
    return render(request, 'workshops/workshop_list_past.html', context={
         'available_years': available_years,
         'years': years,
         'workshops': workshops,
         'year_selected': year,
         'total_workshops': Workshop.objects.filter(date_end__lt=datetime.now()).count,
         'categories': categories,
        }, 
    )

def workshop_list_by_year_current(request,year):
    available_years = Year.objects.filter(hidden=False).order_by('-date')
    years = get_workshop_count_yearly(min_date=datetime.now())
    workshops = Workshop.objects.filter(date_start__year=year,date_end__gte=datetime.now()).order_by('-date_start')
    categories = WorkshopClass.objects.all()
    return render(request, 'workshops/workshop_list_current.html', context={
         'available_years': available_years,
         'years': years,
         'workshops': workshops,
         'year_selected': year,
         'total_workshops':  Workshop.objects.filter(date_end__gte=datetime.now()).count,
         'categories': categories,
        }
    )

def workshop(request, workshop_id):
    available_years = Year.objects.filter(hidden=False).order_by('-date')
    try:
        workshop = Workshop.objects.get(id = workshop_id)
    except:
        return render(request, 'workshops/not_found.html')
    validated_registrations = WorkshopRegistration.objects.filter(workshop=workshop,validated=True).order_by('last_name')
    awaiting_validation_registrations =  WorkshopRegistration.objects.filter(workshop=workshop,validated=False)
    sponsors = SponsorInWorkshop.objects.filter(workshop=workshop)
    num_presentations = len(Presentation.objects.filter(workshop=workshop))
    num_photos = len(WorkshopPhoto.objects.filter(workshop=workshop))
    return render(request, 'workshops/workshop.html', context={
         'available_years': available_years,
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
    data = {}
    available_years = Year.objects.filter(hidden=False).order_by('-date')
    try:
        workshop = Workshop.objects.get(id=workshop_id)
    except:
        return render(request, 'workshops/not_found.html')

    if not workshop.registration_open:
        return render(request, 'workshops/not_found.html')

    #TODO: If we're passing the whole workshop, why do we need to pass the individual parts of the workshop?
    data['available_years'] = available_years
    data['workshop'] = workshop
    data['title'] = workshop.name
    data['content'] = workshop.content
    data['workshop_reg'] = workshop
    data['validated_registrations'] = WorkshopRegistration.objects.filter(workshop=workshop,validated=True).order_by('created')
    data['awaiting_validation_registrations'] =  WorkshopRegistration.objects.filter(workshop=workshop,validated=False)
    data['sponsors'] = SponsorInWorkshop.objects.filter(workshop=workshop)
    data['num_presentations'] = len(Presentation.objects.filter(workshop=workshop))
    data['num_photos'] = len(WorkshopPhoto.objects.filter(workshop=workshop))
    data['show_registration'] = False

    if request.method == 'POST':
        if request.POST['email'] != request.POST['verify_email']:
            data['error'] = 'email-mismatch'
            return render(request, 'workshops/registration.html', context=data)

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
                phone=request.POST['phone'], 
            )
        except IntegrityError as error:
            data['error'] = 'duplicate-account'
            return render(request, 'workshops/registration.html', context=data)

    return render(request, 'workshops/registration.html', context=data)

def presentations(request, workshop_id):
    available_years = Year.objects.filter(hidden=False).order_by('-date')
    try:
        workshop = Workshop.objects.get(id = workshop_id)
    except:
        return render(request, 'workshops/not_found.html', {})
    sponsors = SponsorInWorkshop.objects.filter(workshop=workshop)
    presentations = Presentation.objects.filter(workshop=workshop).order_by('-time_ini')
    num_photos = len(WorkshopPhoto.objects.filter(workshop=workshop))
    return render(request, 'workshops/workshop_presentations.html', context={
         'available_years': available_years,
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
    available_years = Year.objects.filter(hidden=False).order_by('-date')
    try:
        workshop = Workshop.objects.get(id = workshop_id)
    except:
        return render(request, 'workshops/not_found.html', {})
    sponsors = SponsorInWorkshop.objects.filter(workshop=workshop)
    presentations = len(Presentation.objects.filter(workshop=workshop))
    photos = WorkshopPhoto.objects.filter(workshop=workshop).order_by("priority")
    return render(request, 'workshops/photos.html', context={
         'available_years': available_years,
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

def registration_list(request, workshop_id):
    if not request.user.is_staff:
        return render(request, 'workshops/not_found.html', {})

    try:
        workshop = Workshop.objects.get(id = workshop_id)
        registrations = WorkshopRegistration.objects.filter(workshop=workshop,validated=True).order_by('last_name')
    except:
        return render(request, 'workshops/not_found.html', {})


    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="workshop_registrations.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(['First Name', 'Last Name', 'Position', 'Institution', 'Address', 'Email', 'Phone', 'Area of Expertise', 'Created', 'Modified', 'Validated'])

    output = []

    for registration in registrations:
        output.append([registration.first_name, registration.last_name, registration.position, registration.institution, registration.address, registration.email, registration.phone, registration.area_of_expertise, registration.created, registration.modified, registration.validated])
    
    writer.writerows(output)

    return response