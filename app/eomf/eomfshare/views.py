# Create your views here.
from django.contrib.sites.models import Site
from django.http import HttpResponse
from django.utils.encoding import force_text
from django.core.mail import send_mail
import eomf.eomfshare.models
from django.views.decorators.csrf import csrf_exempt
from django.template import Context, RequestContext, loader, Template
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.urls import reverse
from eomf.feedback.models import Feedback

import json
import eomf.eomfshare.forms

def upload_form_view(request):
	t = loader.get_template('eomfshare/base.html')
	c = RequestContext(request,{'test':True})
	return HttpResponse(t.render(c))


@csrf_exempt
def success_upload(request):
	t = loader.get_template('eomfshare/base.html')
	form = forms.UploadFileForm(request.POST, request.FILES)
	c = RequestContext(request,{'success':True})
	if form.is_valid():
		v = form.save(commit=False)
		#v['url'] = url
		#v['site'] = Site.objects.get_current()
		v.save()
		# send_mail('Eomf-Dev: User-Feedback','Details:'+'\n'+'URl: '+str(form.cleaned_data['url'])+'\n'+'email:'+str(form.cleaned_data['email'])+'\n'+'subject:'+str(form.cleaned_data['subject'])+'\n'+'text:'+str(form.cleaned_data['text'])+'\n'+'site_id:'+str(form.cleaned_data['site']), 'admin@eomf-dev.ou.edu', ['bhargavreddy.bolla@ou.edu','bhargavreddy.bolla@gmail.com','Xibei.Jia-1@ou.edu'], fail_silently=True)
		return HttpResponse("Successly Uploaded")
	return HttpResponse(json.dumps({'form':form.is_valid(),'request_post':request.POST}))