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
from ceom.outreach.gisday.models import Booth, Year, Announcement, PersonInGroup, SponsorInYear, ItemInYear, SummaryContent, Volunteer, Survey, Agenda
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
        photos = []
        PROJECT_ROOT = os.path.dirname(__file__)
        dirname = os.path.join(PROJECT_ROOT, '..')
        dirname = os.path.join(dirname, 'media/gisday/' +
                               str(year) + '/photo-gallery/')
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        for filename in os.listdir(dirname):
            # Check that it is an image file

            try:
                im = Image.open(dirname + '/' + filename)
                photos.append(os.path.join(
                    'gisday/' + str(year) + '/photo-gallery/', filename))
            except:
                pass
        return render(request, 'gisday/20XX/photoGallery.html', context={
            'available_years': available_years,
            'gisdate': date,
            'photos': photos
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

np = '''Dear Exhibitor,

Your request for booth has been received and is currently waiting for approval, please contact Melissa Scott for more information about the booth, at mscott@ou.edu

Regards,

The GISday team
'''

fp = '''Dear Exhibitor,

Your request for booth has been received and will be approved dependent upon the payment of $300. Please contact Melissa Scott for more information about the booth at mscott@ou.edu.

Regards,

The GISday team

'''

from django.core.mail import EmailMultiAlternatives


def booth(request, year):
    available_years = Year.objects.filter(hidden=False).order_by('-date')
    if year_available(year):
        form = None
        date = Year.objects.get(date__year=year)
        try:
            content = BoothContent.objects.get(year=date)
        except:
            return render(request, 'gisday/registrationsoon.html', context={'available_years': available_years})
        registration_successful = False
        if registration_enabled(year):

            if request.method == 'POST':
                form = BoothForm(request.POST)
                if form.is_valid():
                    v = form.save(commit=False)
                    v.validated = 'False'
                    v.save()
                    tos = content.registration_recipients.split(';')
                    tos.append(v.email)
                    subject = "GISDay " + str(year) + " Booth registration"

                    from_email = "noreply@ceom.ou.edu"
                    if v.non_profit:
                        message = content.registration_message_non_profit
                    else:
                        message = content.registration_message_profit
                    if not message:
                        message = "Thank you for registering. please contact Melissa Scott for more information about the booth, at mscott@ou.edu"
                    msg = EmailMultiAlternatives(
                        subject, message, from_email, tos)
                    msg.attach_alternative(message, "text/html")
                    msg.send()
                    form = None
                    registration_successful = True
            else:
                form = BoothForm(initial={
                    'year': date
                })
        max_number_of_booths = content.max_booths
        booth = Booth.objects.all().filter(validated=True, year=date)[
            :max_number_of_booths]

        return render(request, "gisday/20XX/booth.html", context={
            'available_years': available_years,
            'gisdate': date,
            "booth": booth,
            "form": form,
            "registration_successful": registration_successful,
            'content': content.content,
            "pyear": year,
        })
    else:
        return render(request, 'gisday/notfound.html', context={'available_years': available_years})


def visitor_registration(request, year):
    available_years = Year.objects.filter(hidden=False).order_by('-date')
    if year_available(year):
        form = None
        registration_successful = False
        date = Year.objects.get(date__year=year)
        try:
            content = VisitorRegistrationContent.objects.get(year=date)
        except:
            return render(request, 'gisday/notfound.html', context={'available_years': available_years})
        if registration_enabled(year):
            if request.method == 'POST':
                form = VisitorForm(request.POST)
                #form.fields['validated'] = True
                if form.is_valid():
                    v = form.save(commit=False)
                    v.validated = 'False'
                    v.save()
                    tos = content.registration_recipients.split(';')
                    tos.append(v.email)
                    subject = "GISDay " + str(year) + " Visitor registration"
                    message = content.registration_message
                    if not message:
                        message = "Thank you for registering for the GISday!"
                    from_email = "noreply@ceom.ou.edu"
                    msg = EmailMultiAlternatives(
                        subject, message, from_email, tos)
                    msg.attach_alternative(message, "text/html")
                    msg.send()

                    form = None
                    registration_successful = True
            else:
                form = VisitorForm(initial={
                    'year': date
                })

        numberOfVisitors = len(Visitor.objects.filter(year=date))

        return render(request, "gisday/20XX/visitor.html", context={
            'available_years': available_years,
            'gisdate': date,
            "numberOfVisitors": numberOfVisitors,
            "form": form,
            "registration_successful": registration_successful,
            "content": content.content,
        })
    else:
        return render(request, 'gisday/notfound.html', context={'available_years': available_years})


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

def boothvalidation(email, email2):
    if(email2 == email):
        return True
    else:
        return False


def boothupdate(request, id, year, email):
    booth = Booth.objects.get(id=id)
    x = boothvalidation(email, booth.email)
    if x:
        pass
    else:
        return HttpResponse("Some thing went wrong! please try again. If problem persists please contact administrator.")
    available_years = Year.objects.filter(hidden=False).order_by('-date')
    if year_available(year):
        form = None
        date = Year.objects.get(date__year=year)
        try:
            content = BoothContent.objects.get(year=date)
        except:
            return render(request, 'gisday/registrationsoon.html', context={'available_years': available_years})
    # available_years = Year.objects.filter(hidden=False).order_by('-date')
    # if year_available(year):
    #     form = None
    #     date = Year.objects.get(date__year=year)
    # f = open('\static\workfile', 'w')  # everytime should be refreshed
    # f.write("Debug file")
    if(request.method == "POST"):
        # //here update the form contents to the model
        # Don't want to do all the validations So how ??
        # return HttpResponse("got into post")
        # form = BoothForm(request.POST)
        # return HttpResponse(json.dumps({'form':request.POST}))
        x = request.POST
        # # f.write(str(form.is_valid()))
        # # f.write(str(form))
        if True:
            # v = form.save(commit=False)
            v = booth
            v.validated = True
            v.comment = x['comment']
            v.last_name = x['last_name']
            v.names = x['names']
            v.city = x['city']
            v.first_name = x['first_name']
            v.zipcode = x['zipcode']
            v.state = x['state']
            v.department = x['department']
            v.email = x['email']
            v.oversized = x['oversized']
            v.phone = x['phone']
            v.institution = x['institution']
            v.permits = x['permits']
            v.tshirt_size_1 = x['tshirt_size_1']
            v.tshirt_size_2 = x['tshirt_size_2']
            v.non_profit = bool(x['non_profit'])
            v.address_1 = x['address_1']
            v.address_2 = x['address_2']
            try:
                v.save()
            except:
                return HttpResponse("Some thing went wrong updating your record! Please try again or contact administrator")

            tos = content.registration_recipients.split(';')
            tos.append(v.email)
            subject = "GISDay " + str(year) + " Booth registration--update successful"

            from_email = "noreply@ceom.ou.edu"
            # return HttpResponse(v.non_profit is True)
            if v.non_profit is True:
                message = "Your exhibitor registration has been successfully updated, thank you for participating in the GIS Day Expo at OU."
            else:
                message = "Your exhibitor registration has been successfully updated, thank you for participating in the GIS Day Expo at OU."
            if not message:
                message = "Thank you for registering. Please contact the administrator."
            msg = EmailMultiAlternatives(subject, message, from_email, tos)
            msg.attach_alternative(message, "text/html")
            msg.send()
            form = None
            registration_successful = True
            # return HttpResponse("got into post and came till here")
            return render(request, "gisday/Booth_update_form.html", context={
                "booth": booth,
                "form": form,
                "registration_successful": registration_successful,
                "pyear": year,
            })
    else:
        form = BoothForm(initial={
            'year': date,
            'institution': booth.institution,
            'non_profit': booth.non_profit,
            'department': booth.department,
            'last_name': booth.last_name,
            'first_name': booth.first_name,
            'address_1': booth.address_1,
            'address_2': booth.address_2,
            'city': booth.city,
            'state': booth.state,
            'zipcode': booth.zipcode,
            'phone': booth.phone,
            'email': booth.email,
            'names': booth.names,
            'permits': booth.permits,
            'oversized': booth.oversized,
            'comment': booth.comment,
            'tshirt_size_1': booth.tshirt_size_1,
            'tshirt_size_2': booth.tshirt_size_2,
        })

        return render(request, 'gisday/Booth_update_form.html', context={'pers': booth, 'form': form, 'get': True})
    return HttpResponse("Some thing went wrong!")


def posterupdate(request, id, year, email):
    poster = Poster.objects.get(id=id)
    x = boothvalidation(email, poster.email)
    if x:
        pass
    else:
        return HttpResponse("Some thing went wrong! please try again. If problem persists please contact administrator.")
    if False:
        # return HttpResponse("I entered this ")
        # poster_contest(request, year, id)
        pass
    else:
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
        # available_years = Year.objects.filter(hidden=False).order_by('-date')
        # if year_available(year):
        #     form = None
        #     date = Year.objects.get(date__year=year)
        # f = open('\static\workfile', 'w')  # everytime should be refreshed
        # f.write("Debug file")
        if(request.method == "POST"):
            # //here update the form contents to the model
            # Don't want to do all the validations So how ??
            # return HttpResponse("got into post")
            # form = BoothForm(request.POST)
            return HttpResponse(json.dumps({'form':request.POST, 'files':request.FILES['preview'].name}))
            x = request.POST
            # # f.write(str(form.is_valid()))
            # Delete this
            # # f.write(str(form))
            if True:
                # v = form.save(commit=False)
                v = poster
                v.validated = True
                v.comment = x['comment']
                v.last_name = x['last_name']
                v.category = PosterCategory.objects.get(id = x['category'])
                v.title = x['title']
                v.abstract = x['abstract']
                v.authors = x['authors']
                v.first_name = x['first_name']
                v.department = x['department']
                v.email = x['email']
                v.institution = x['institution']
                f = request.FILES['preview']
                v.preview = f
                try:
                    v.save()
                except:
                    return HttpResponse("Some thing went wrong updating your record! Please try again or contact administrator")

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
            t = loader.get_template('gisday/Poster_update_form.html')
            c = RequestContext(request, context={'pers': poster, 'form': form, 'get': True})
            return HttpResponse(t.render(c))
        return HttpResponse("Some thing went wrong!")

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



