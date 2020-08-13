from django.contrib.auth.models import User
from django.core import serializers
import json

from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.forms.models import model_to_dict
from eomf.accounts.models import Profile
from eomf.accounts.forms import RegistrationForm, ProfileForm, UserForm
from django.utils.html import escape
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from django.forms import ValidationError

import django

def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/profile/')
    else:
        return HttpResponseRedirect('/accounts/login/')

def logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def mobile_login(request):

    try:
        user = authenticate(username=request.POST['username'], password=request.POST['password'])

        if user is not None:
            login(request, user)
            return HttpResponse("login-success", status=200)
        else: 
            return HttpResponse("login-failed", status=404)

    except Exception as e:
        return HttpResponse('ERROR: ' + str(e), status=500)


def register(request):
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            new_user = user_form.save()
            p = Profile.objects.get(user=new_user)
            profile_form = ProfileForm(request.POST, instance=p)
            profile_form.save()
            
            user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            if user is not None:
                login(request,user)
                
            return HttpResponseRedirect("/accounts/profile/")
    else:
        profile_form = ProfileForm()
        user_form = RegistrationForm()

    return render_to_response("accounts/register.html", {
        'user_form' : user_form, 'profile_form': profile_form
    }, context_instance=RequestContext(request) )


def profile_authed(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user_detail', args=[request.user.username]))
    else:
        return HttpResponseRedirect('/accounts/login/')

def profile(request, username):
    if request.user.is_authenticated():
        u = User.objects.get(username=username)
        p = Profile.objects.get(user=u)

        user_form = UserForm(instance=u)      
        user_form.merge_from_initial()

        return render_to_response('accounts/profile.html',
        {
            'username': u.username,
            'user_f': user_form, 
            'profile': p,
        }, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')

@login_required
def profile_edit(request):
    p = request.user.profile

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=p)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            p = profile_form.save()
            return HttpResponseRedirect(reverse('user_detail', args=[request.user.username]))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=p)
        
    return render_to_response("accounts/edit.html", {
        'user_form' : user_form, 'profile_form': profile_form
    }, context_instance=RequestContext(request) )


def id_from_username(request):

    #This is awful, but it's the only way I can figure out how to do this.
    #We need the primary key (pk) for user, which Django holds in the user object. All of the user objects are in User.objects
    #I can't find what the getter function for retrieving the pk field is, as it's not documented anywhere I've looked.
    #However, it's fairly easy to access if the object is serialized to JSON.
    #As such, we serialize the user to JSON, narrow the JSON object down to just the pk, then deserialize it and return it.


    #if 'username' in request.GET:
    #    username = request.GET.get('username', '')

    #    try:
    #        userdata = serializers.serialize("json", User.objects.filter(username__iexact=username), indent=4)
    #        userdata_in_json = json.loads(userdata)[0]
    #        user_id = json.dumps(userdata_in_json["pk"])
    #        return HttpResponse(user_id)

    #    except User.DoesNotExist:
    #        return HttpResponse('Server couldnt find username: ' + username, status=404)


    #return HttpResponse("Server received request for id_from_username but no username", status=404)
    return HttpResponse("This request is deprecated")