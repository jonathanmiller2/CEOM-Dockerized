# Create your views here.
from django.contrib.sites.models import Site
from django.http import HttpResponse
from django.utils.encoding import force_text
from django.core.mail import send_mail
import eomf.feedback.models
from django.views.decorators.csrf import csrf_exempt
from django.template import Context, RequestContext, loader, Template
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.urls import reverse
from eomf.feedback.models import Feedback, Task_status

import json
import eomf.feedback.forms

#lets see if this works--bitbucket test

def sanitize(errors):
    dct = dict((str(k),list(force_unicode(a) for a in v)) for k,v in errors.items())
    return dct

@csrf_exempt
def handle_ajax(request, url):
    #return HttpResponse(json.dumps({'form':request.POST, 'files':url}))
    if not request.POST:
        return HttpResponse(json.dumps({'error':'no post recieved'}))
    else:
        post = {}
        '''for k in request.POST:
            post[k] = request.POST[k]
           ''' 
        #post = forms.FeedbackForm(request.POST)
        '''post['email'] = request.POST.get('email')
        post['Priority'] = request.POST.get('Priority')
        post['subject'] = request.POST.get('subject')
        post['text'] = request.POST.get('text')
        post['Photo'] = request.POST.get('Photo')'''
        #post['url'] = url
        #post['site'] = Site.objects.get_current()
        #files = request.POST[files]
        #post['site_id'] = 7
        form = forms.FeedbackForm(data=request.POST, files=request.FILES)
        #form.cleaned_data['url'] = GetEmailString()
        #form.fields["Email"].initial = GetEmailString()
        #form.fields["url"].initial = url
        #form.fields["site"].initial = Site.objects.get_current()
        '''data1 = request.POST
        data1['url'] = url
        data1['site'] = Site.objects.get_current()'''
        #form = forms.FeedbackForm(data=request.POST, files=request.FILES)
        #form['url'] = url
        #form['site'] = Site.objects.get_current()
        '''v = form.save(commit=False)
        v['url'] = url
        v['site'] = Site.objects.get_current()
        form = v'''
        if form.is_valid():
            v = form.save(commit=False)
            #v['url'] = url
            #v['site'] = Site.objects.get_current()
            v.save()
            xq = Task_status(feedback_track = Feedback.objects.get(id=v.id))
            xq.save()#created new tracking_object for feedback_object
            send_mail('Eomf-Dev: User-Feedback', 'Form_id: '+str(v.id)+'\n'+'Details:'+'\n'+'URl: '+str(form.cleaned_data['url'])+'\n'+'email:'+str(form.cleaned_data['email'])+'\n'+'subject:'+str(form.cleaned_data['subject'])+'\n'+'text:'+str(form.cleaned_data['text'])+'\n'+'site_id:'+str(form.cleaned_data['site']), 'admin@eomf-dev.ou.edu', ['bhargavreddy.bolla@ou.edu','bhargavreddy.bolla@gmail.com','Xibei.Jia-1@ou.edu'], fail_silently=True)
            return HttpResponse(json.dumps({'success_bro':True}))
        else:            
            return HttpResponse(json.dumps({'errors':sanitize(form.errors)}))

#This view is to show all the feedbacks that are available.
def feedback_details(request):
    t = loader.get_template('feedback/base.html')
    #set_user = User.objects.raw('select auth_user.id,auth_user.date_joined from auth_user')
    #count, build_cat = getnumusers(set_user)
    feedback_total = Feedback.objects.order_by('id');
    status = Task_status.objects.order_by('id');
    c = RequestContext(request,{'feedback':feedback_total,'status':status})
    return HttpResponse(t.render(c))


def comment_page(request, id):
    t = loader.get_template('feedback/comment.html')
    feedback = Feedback.objects.get(id=id)
    comments = feedback.comment.all()
    c = RequestContext(request,{'comments':comments, 'feed':feedback})
    return HttpResponse(t.render(c))
