#TODO: Are these imports necessary
from django.template import Context, RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.forms.utils import ErrorList
from django.core.mail import send_mail
from django.template.base import VariableDoesNotExist
from django.db import IntegrityError

from ceom.outreach.gisday.forms import VisitorForm, BoothForm, PhotoForm, PosterForm
from PIL import Image
from django.views.generic.edit import UpdateView
from ceom.outreach.gisday.models import *
import os
import sys
import json

#   AUX FUNCTIONS
def year_available(year):
    try:
        gisdays = Year.objects.get(date__year=year)
    except:
        return False
    return True


def registration_enabled(year):
    try:
        gisdays = Year.objects.get(date__year=year)
        return not gisdays.registration_closed
    except:
        return False
    return False
# VIEWS


def gallery_2012(request):
    available_years = Year.objects.filter(hidden=False).order_by('-date')
    photos = []
    PROJECT_ROOT = os.path.dirname(__file__)
    dirname = os.path.join(PROJECT_ROOT, '..')
    dirname = os.path.join(dirname, 'media/gisday/2012/photo-gallery/')
    for filename in os.listdir(dirname):
        # Check that it is an image file

        try:
            im = Image.open(dirname + '/' + filename)
            photos.append(os.path.join(
                '/media/gisday/2012/photo-gallery/', filename))
        except:
            pass
    return render(request, 'gisday/2012/gallery.html', context={'available_years': available_years, 'photos': photos})


def gallery(request, year):
    available_years = Year.objects.filter(hidden=False).order_by('-date')
    if year_available(year):
        date = Year.objects.get(date__year=year)
        photos = PhotoGallery.objects.all().filter(year=date)
        return render(request, 'gisday/20XX/photoGallery.html', context={
            'available_years': available_years,
            'gisdate': date,
            'photos': photos,
        })
    else:
        return render(request, 'gisday/notfound.html', context={'available_years': available_years})


def images(request, year):
    available_years = Year.objects.filter(hidden=False).order_by('-date')
    if year_available(year):
        date = Year.objects.get(date__year=year)
        photos = GisDayPhoto.objects.all().filter(year=date)
        return render(request, 'gisday/20XX/imageGallery.html', context={
            'available_years': available_years,
            'gisdate': date,
            'photos': photos,
        })
    else:
        return render(request, 'gisday/notfound.html', context={'available_years': available_years})


def sponsors(request, year):
    available_years = Year.objects.filter(hidden=False).order_by('-date')
    if year_available(year):
        date = Year.objects.get(date__year=year)
        sponsors = SponsorInYear.objects.filter(year=date).order_by(
            '-category__min_inversion', 'sponsor__name')
        items = ItemInYear.objects.filter(year=date).order_by('-value')
        try:
            content = SponsorsContent.objects.get(year=date).content
        except:
            content = "Contents is empty, please contact the administrator"
        return render(request, 'gisday/20XX/sponsors.html', context={
            'available_years': available_years,
            'gisdate': date,
            'sponsors': sponsors,
            'items': items,
            'content': content,
        })
    else:
        return render(request, 'gisday/notfound.html', context={'available_years': available_years})


photoMessage = '''
    Congratulations!

        You have successfully registered for GIS day 2013 Photo contest!

        If you have further questions please contact Mr. Jonah Duckles at
        jduckles@ou.edu.
'''


def photo_contest(request, year):
    available_years = Year.objects.filter(hidden=False).order_by('-date')
    if year_available(year):
        date = Year.objects.get(date__year=year)
        try:
            content = PhotoContestContent.objects.get(year=date)
            if date.photo_contest_hidden:
                raise "content is hidden!"
        except:
            return render(request, 'gisday/notfound.html', context={'available_years': available_years})
        form = None
        need_login = False
        already_registered = False

        if request.user.is_authenticated():
            if len(PhotoContestParticipant.objects.filter(user=request.user)) == 0:
                if request.method == 'POST' and registration_enabled == True and registration_enabled(year):
                    form = PhotoForm(request.POST)
                    if form.is_valid():
                        data = getValidatedPhotoContestCopy(request, form)
                        model = data.save()
                        tos = [model.email, "jduckles@ou.edu", "gisday@ou.edu"]
                        subject = "GISDay 2013 Photo Contest registration"
                        r = send_mail(subject, photoMessage,
                                      'noreply@ceom.ou.edu', tos)
                        form = None
                        already_registered = True
                else:
                    form = PhotoForm(initial={
                        'first_name': request.user.first_name,
                        'last_name': request.user.last_name,
                        'email': request.user.email,
                        'verifyemail': request.user.email,
                    })
            else:
                already_registered = True
        else:
            need_login = True
        form = None
        return render(request, 'gisday/20XX/photoContest.html', context={
            'available_years': available_years,
            'gisdate': date,
            "need_login": need_login,
            "already_registered": already_registered,
            "form": form,
            "content": content.content,
        })
    else:
        return render(request, 'gisday/notfound.html', context={'available_years': available_years})


def getValidatedPhotoContestCopy(request, form):
    data = PhotoContestParticipant()
    data.user = request.user
    data.first_name = form.cleaned_data['first_name']
    data.last_name = form.cleaned_data['last_name']
    data.email = form.cleaned_data['email']
    data.comment = form.cleaned_data['comment']
    data.validated = False
    return data

postMessage = '''
    Congratulations!

        You have successfully registered for GIS day Poster Contest.
        If you have further questions please contact Mr. Keith A.Brewster at
        kbrewster@ou.edu.
'''


def poster_contest(request, year):
    available_years = Year.objects.filter(hidden=False).order_by('-date')
    registration_successful = False
    # return HttpResponse("I was here!!")
    if year_available(year):
        form = None
        date = Year.objects.get(date__year=year)
        try:
            content = PosterContestContent.objects.get(year=date)
            if date.poster_contest_hidden:
                raise "content is hidden!"
        except:
            return render(request, 'gisday/notfound.html', context={'available_years': available_years})
        if registration_enabled(year):
            if request.method == 'POST':
                # return HttpResponse("I was here!!")
                form = PosterForm(request.POST, request.FILES)
                if form.is_valid():
                    v = form.save(commit=False)
                    # if id!=None:
                    #     v.id = id
                    # else:
                    #     pass
                    v.validated = 'False'
                    v.save()
                    tos = content.registration_recipients.split(';')
                    tos.append(v.email)
                    subject = "GISDay " + \
                        str(year) + " Poster Contest registration"
                    message = content.registration_message
                    if not message:
                        message = "Thank you for registering for the Poster contest!"
                    from_email = "noreply@ceom.ou.edu"
                    msg = EmailMultiAlternatives(
                        subject, message, from_email, tos)
                    msg.attach_alternative(message, "text/html")
                    msg.send()
                    form = None
                    registration_successful = True
            else:
                form = PosterForm(initial={
                    'year': date,
                })

        posters = Poster.objects.all().filter(
            validated=True, year=date).order_by('category', "created")[:200]

        return render(request, "gisday/20XX/posterContest.html", context={
            'available_years': available_years,
            'gisdate': date,
            "posters": posters,
            "form": form,
            "registration_successful": registration_successful,
            "content": content.content,
            "pyear": year,
        })
    else:
        return render(request, 'gisday/notfound.html', context={'available_years': available_years})

from django.core.mail import EmailMultiAlternatives


def booth(request, year):
    data = {}

    if not year_available(year):
        return render(request, 'gisday/notfound.html')

    data['gisdate'] = Year.objects.get(date__year=year)
    data['registration_successful'] = False
    data['pyear'] = year
    data['available_years'] = Year.objects.filter(hidden=False).order_by('-date')
    
    try:
        content = BoothContent.objects.get(year=data['gisdate'])
        data['content'] = content.content
        max_number_of_booths = content.max_booths
    except:
        data['content'] = ''
        max_number_of_booths = 1000

    data['booth_list'] = Booth.objects.all().filter(validated=True, year=data['gisdate'])[:max_number_of_booths]


    if not registration_enabled(year):
        data['error_code'] = 'registration_disabled'
        return render(request, "gisday/20XX/booth.html", context=data)

    if request.method == 'POST':
        data['previous_responses'] = request.POST

        if request.POST['email'] != request.POST['verify_email']:
            data['error_code'] = "email-mismatch"
            return render(request, "gisday/20XX/booth.html", context=data)
        
        try:
            v = Booth.objects.create(
                year=data['gisdate'],
                non_profit=request.POST['institution_type'],
                institution=request.POST['institution'],
                department=request.POST['department'],
                first_name=request.POST['firstname'],
                last_name=request.POST['lastname'],
                address_1=request.POST['address1'],
                address_2=request.POST['address2'],
                city=request.POST['city'],
                state=request.POST['state'],
                zipcode=request.POST['zipcode'],
                phone=request.POST['phone'],
                email=request.POST['email'],
                names=request.POST['additional_attendees'],
                permits=request.POST['parking_permits'],
                oversized=request.POST['oversized'],
                tshirt_size_1=request.POST['tshirt1'],
                tshirt_size_2=request.POST['tshirt2'],
                comment=request.POST['comments'],
                validated=False
            )
        except IntegrityError:
            data['error_code'] = "duplicate"
            return render(request, "gisday/20XX/booth.html", context=data)

        #TODO: Figure out how to send emails from inside docker  
        #tos = content.registration_recipients.split(';')
        #tos.append(v.email)
        #subject = "GISDay " + str(year) + " Booth registration"

        #from_email = "noreply@ceom.ou.edu"
        #if v.non_profit:
        #    message = content.registration_message_non_profit
        #else:
        #    message = content.registration_message_profit
        #if not message:
        #    message = "Thank you for registering. please contact Melissa Scott for more information about the booth, at mscott@ou.edu"
        #msg = EmailMultiAlternatives(
        #    subject, message, from_email, tos)
        #msg.attach_alternative(message, "text/html")
        #msg.send()

        data['registration_successful'] = True
    
    
    return render(request, "gisday/20XX/booth.html", context=data)



def visitor_registration(request, year):
    data = {}

    if not year_available(year):
        return render(request, 'gisday/notfound.html')


    data['gisdate'] = Year.objects.get(date__year=year)
    data['registration_successful'] = False
    data['available_years'] = Year.objects.filter(hidden=False).order_by('-date')

    try:
        content = VisitorRegistrationContent.objects.get(year=date)
        data['content'] = content.content
    except:
        data['content'] = ''


    if not registration_enabled(year):
        data['error_code'] = 'registration_disabled'
        return render(request, "gisday/20XX/visitor.html", context=data)


    if request.method == 'POST':
        data['previous_responses'] = request.POST
        
        if request.POST['email'] != request.POST['verify_email']:
            data['error_code'] = "email-mismatch"
            return render(request, "gisday/20XX/visitor.html", context=data)

        try:
            vis = Visitor.objects.create(
                year=data['gisdate'],
                first_name=request.POST['firstname'],
                last_name=request.POST['lastname'],
                email=request.POST['email'],
                institution=request.POST['institution'],
                comment=request.POST['comments'],
                validated=False
            )
        except IntegrityError:
            data['error_code'] = "duplicate"
            return render(request, "gisday/20XX/visitor.html", context=data)

        #TODO: Figure out how to send emails from inside docker  
        #tos = content.registration_recipients.split(';')
        #tos.append(v.email)
        #subject = "GISDay " + str(year) + " Booth registration"

        #from_email = "noreply@ceom.ou.edu"
        #if v.non_profit:
        #    message = content.registration_message_non_profit
        #else:
        #    message = content.registration_message_profit
        #if not message:
        #    message = "Thank you for registering. please contact Melissa Scott for more information about the booth, at mscott@ou.edu"
        #msg = EmailMultiAlternatives(
        #    subject, message, from_email, tos)
        #msg.attach_alternative(message, "text/html")
        #msg.send()

        data['registration_successful'] = True

    return render(request, "gisday/20XX/visitor.html", context=data)


def about_us(request, year):
    available_years = Year.objects.filter(hidden=False).order_by('-date')
    if year_available(year):
        date = Year.objects.get(date__year=year)
        people = PersonInGroup.objects.filter(year=date).order_by(
            'group__order', 'person__last_name')
        try:
            content = CommitteeContent.objects.get(year=date).content
        except:
            content = "No content in database. Please contact administrator to fix this"
        return render(request, 'gisday/20XX/aboutus.html', context={
            'available_years': available_years,
            'gisdate': date,
            'people': people,
            'content': content,
        })
    else:
        return render(request, 'gisday/notfound.html', context={'available_years': available_years})


def summary(request, year):
    available_years = Year.objects.filter(hidden=False).order_by('-date')
    if year_available(year):
        date = Year.objects.get(date__year=year)
        try:
            content = SummaryContent.objects.get(year=date)
            if date.summary_hidden:
                raise "content is hidden!"
        except:
            return render(request, 'gisday/notfound.html', context={'available_years': available_years})
        return render(request, 'gisday/20XX/summary.html', context={
            'available_years': available_years,
            'gisdate': date,
            'content': content.content,
        })
    else:
        return render(request, 'gisday/notfound.html', context={'available_years': available_years})


def agenda(request, year):
    available_years = Year.objects.filter(hidden=False).order_by('-date')
    if year_available(year):
        date = Year.objects.get(date__year=year)
        agenda_entries_by_date = Agenda.objects.filter(
            year=date).order_by("time_ini")
        date = Year.objects.get(date__year=year)
        has_speaker = False
        for item in agenda_entries_by_date:
            if item.speaker:
                has_speaker = True
                break
        return render(request, 'gisday/20XX/agenda.html', context={
            'available_years': available_years,
            'gisdate': date,
            'agenda_by_date': agenda_entries_by_date,
            'has_speaker': has_speaker,
        })
    else:
        return render(request, 'gisday/notfound.html', context={'available_years': available_years})


def announcements(request, year, position=None):
    available_years = Year.objects.filter(hidden=False).order_by('-date')
    if year_available(year):
        date = Year.objects.get(date__year=year)
        announcements = Announcement.objects.filter(year=date).order_by('position')
        if (not position):
            position = len(announcements) - 1
        position = max(min(int(position), len(announcements) - 1), 0)

        return render(request, 'gisday/20XX/announcements.html', context={
            'available_years': available_years,
            'gisdate': date,
            'announcements': announcements,
            'position': position,
        })
    else:
        return render(request, 'gisday/notfound.html', context={'available_years': available_years})


def logistics(request, year, name=None):
    available_years = Year.objects.filter(hidden=False).order_by('-date')
    if year_available(year):
        date = Year.objects.get(date__year=year)
        return render(request, 'gisday/20XX/logistics.html', context={
            'available_years': available_years,
            'gisdate': date,
        })
    else:
        return render(request, 'gisday/notfound.html', context={'available_years': available_years})


def overview(request):
    available_years = Year.objects.filter(hidden=False).order_by('-date')
    try:
        content = OverviewContent.objects.all()[0].content
    except:
        content = 'Error: content is missing in the database for overview.'
        return render(request, 'gisday/overview.html', context={
            'available_years': available_years,
            'content': content,
            'images': images,
        })


def year2012(request):
    available_years = Year.objects.filter(hidden=False).order_by('-date')
    return render(request, 'gisday/2012/2012.html', context={
        'available_years': available_years,
    })


def survey(request, year):
    available_years = Year.objects.filter(hidden=False).order_by('-date')
    if year_available(year):
        date = Year.objects.get(date__year=year)
        if not date.survey_open:
            return render(request, 'gisday/notfound.html', context={'available_years': available_years})
        try:
            content = SurveyContents.objects.get(year=date).content
        except:
            content = '<p>Please help us in reporting to our federals sponsors (USGS, NASA, NSF EPSCoR) by completing this survey. Your participation will help ensure continued funding and improve GIS Day in future years. Your responses are anonymous and not linked to any identifiable information such as email address.</p>'
        if request.method == "POST":
            if request.POST.get('participate_again') == 'on':
                participate_again = True
            else:
                participate_again = False
    
            survey = Survey.objects.create(
                year=date,
                institution=request.POST['institution'],
                other_institution=request.POST['other_institution'],
                position=request.POST['position'],
                other_position=request.POST['other_position'],
                highest_degree=request.POST['highest_degree'],
                gender=request.POST['gender'],
                ethnicity=request.POST['ethnicity'],
                citizenship=request.POST['citizenship'],
                race=request.POST['race'],
                other_race=request.POST['other_race'],
                disability=request.POST['disability'],
                other_disability=request.POST['other_disability'],
                parents_degree=request.POST['parents_degree'],
                participate_again=participate_again,
                role=request.POST['role'],
                other_role=request.POST['other_role'],
                beneficial_aspects=request.POST['beneficial_aspects'],
                comments_and_suggestions=request.POST['comments_and_suggestions'],
            )
            return render(request, 'gisday/20XX/survey.html', context={
                'available_years': available_years,
                'year': date,
                'gisdate': date,
                'form_done': True,
                'registration_successful': True,
                'content': content,
                'form': survey
            })
        return render(request, 'gisday/20XX/survey.html', context={
                'available_years': available_years,
                'gisdate': date,
                'content': content,
        })
    else:
        return render(request, 'gisday/notfound.html', context={'available_years': available_years})


# def demographic_survey(request, year):
#     available_years = Year.objects.filter(hidden=False).order_by('-date')
#     if year_available(year):
#         date = Year.objects.get(date__year=year)
#         if not date.survey_open:
#             return render(request, 'gisday/notfound.html', context={'available_years': available_years})
#         if request.method == "POST":
#             survey = DemographicSurvey.objects.create(
#                 year=date,
#                 institution=request.POST['institution'],
#                 other_institution=request.POST['other_institution'],
#                 position=request.POST['position'],
#                 other_position=request.POST['other_position'],
#                 highest_degree=request.POST['highest_degree'],
#                 gender=request.POST['gender'],
#                 ethnicity=request.POST['ethnicity'],
#                 citizenship=request.POST['citizenship'],
#                 race=request.POST['race'],
#                 other_race=request.POST['other_race'],
#                 disability=request.POST['disability'],
#                 other_disability=request.POST['other_disability'],
#             )
#         return render(request, 'gisday/20XX/demographic_survey.html', context={
#             'available_years': available_years,
#             'year': date,
#             'gisdate': date,
#             'form_done': True,
#             'registration_successful': True,
#             'form': survey,
#         })
#     else:
#         return render(request, 'gisday/notfound.html', context={'available_years': available_years})


def boothupdate(request, year):
    data = {}

    id = request.GET['id']
    email = request.GET['email']
    date = Year.objects.get(date__year=year)
    booth = Booth.objects.get(id=id)
    data['registration_successful'] = False
    Year.objects.filter(hidden=False).order_by('-date')

    try:
        content = BoothContent.objects.get(year=date)
        data['content'] = content.content
    except:
        data['content'] = ''
    
    if not year_available(year):
        return render(request, 'gisday/registrationsoon.html')

    if request.method == 'POST':
        data['previous_responses'] = request.POST

        if request.POST['email'] != request.POST['verify_email']:
            data['error_code'] = "email-mismatch"
            return render(request, "gisday/Booth_update_form.html", context=data)

        try:
            booth.year=date
            booth.non_profit=request.POST['institution_type']
            booth.institution=request.POST['institution']
            booth.department=request.POST['department']
            booth.first_name=request.POST['firstname']
            booth.last_name=request.POST['lastname']
            booth.address_1=request.POST['address1']
            booth.address_2=request.POST['address2']
            booth.city=request.POST['city']
            booth.state=request.POST['state']
            booth.zipcode=request.POST['zipcode']
            booth.phone=request.POST['phone']
            booth.email=request.POST['email']
            booth.names=request.POST['additional_attendees']
            booth.permits=request.POST['parking_permits']
            booth.oversized=request.POST['oversized']
            booth.tshirt_size_1=request.POST['tshirt1']
            booth.tshirt_size_2=request.POST['tshirt2']
            booth.comment=request.POST['comments']
            booth.save()

        except IntegrityError:
            data['error_code'] = "duplicate"
            return render(request, "gisday/20XX/booth.html", context=data)

        data['registration_successful'] = True

    else:
        data['previous_responses'] = {
            'institution_type':str(booth.non_profit),
            'institution':booth.institution,
            'department':booth.department,
            'firstname':booth.first_name,
            'lastname':booth.last_name,
            'address1':booth.address_1,
            'address2':booth.address_2,
            'city':booth.city,
            'state':booth.state,
            'zipcode':booth.zipcode,
            'phone':booth.phone,
            'email':booth.email,
            'verify_email':booth.email,
            'additional_attendees':booth.names,
            'parking_permits':booth.permits,
            'oversized':str(booth.oversized),
            'tshirt1':booth.tshirt_size_1,
            'tshirt2':booth.tshirt_size_2,
            'comments':booth.comment
        }
        
    return render(request, "gisday/Booth_update_form.html", context=data)
    
    # TODO: Figure out how to send emails from inside docker
    # tos = content.registration_recipients.split(';')
    # tos.append(v.email)
    # subject = "GISDay " + str(year) + " Booth registration--update successful"

    # from_email = "noreply@ceom.ou.edu"
    
    # message = "Your exhibitor registration has been successfully updated, thank you for participating in the GIS Day Expo at OU."

    # msg = EmailMultiAlternatives(subject, message, from_email, tos)
    # msg.attach_alternative(message, "text/html")
    # msg.send()


def posterupdate(request, id, year, email):
    poster = Poster.objects.get(id=id)
    if email != poster.email:
        return HttpResponse("Some thing went wrong! please try again. If problem persists please contact administrator.")

    available_years = Year.objects.filter(hidden=False).order_by('-date')
    registration_successful = False
    if year_available(year):
        form = None
        date = Year.objects.get(date__year=year)
        try:
            content = PosterContestContent.objects.get(year=date)
            if date.poster_contest_hidden:
                raise "content is hidden!"
        except:
            return render(request, 'gisday/notfound.html', context={'available_years': available_years})

    if(request.method == "POST"):
        return HttpResponse(json.dumps({'form':request.POST, 'files':request.FILES['preview'].name}))
    

    form = PosterForm(initial={
        'year': date,
        'validated' : True,
        'comment' : poster.comment,
        'last_name' : poster.last_name,
        'category' : poster.category,
        'title' : poster.title,
        'abstract' : poster.abstract,
        'authors' : poster.authors,
        'first_name' : poster.first_name,
        'department' : poster.department,
        'email' : poster.email,
        'institution' : poster.institution,
    })
    return render(request, 'gisday/Poster_update_form.html', context={'pers': poster, 'form': form, 'get': True})

def volunteer(request, year):
    available_years = Year.objects.filter(hidden=False).order_by('-date')
  
    if request.method == 'POST':
        yearObject = Year.objects.get(date__year=year)
        v_info = request.POST['lname']+','+request.POST['fname']+','+request.POST['prole']+','+request.POST['lunch']+','+request.POST['TShirtSize']
        volunteer = Volunteer.objects.create(
            year=yearObject,
            last_name=request.POST['lname'],
            first_name=request.POST['fname'],
            prole=request.POST['prole'],
            lunch=request.POST['lunch'],
            TShirtSize=request.POST['TShirtSize'],
        )

        return render(request, 'gisday/20XX/Thanks.html', {'available_years': available_years,'data':v_info})

    all_volunteers = list(Volunteer.objects.values())

    return render(request, 'gisday/20XX/volunteer.html', {'available_years': available_years,'data':all_volunteers})



