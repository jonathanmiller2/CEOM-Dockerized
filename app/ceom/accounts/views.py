from django.contrib.auth.models import User
from django.core import serializers
import json

from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.forms.models import model_to_dict
from ceom.accounts.models import Profile
from ceom.accounts.forms import RegistrationForm, ProfileForm, UserForm, CustomLoginForm
from django.utils.html import escape
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import validate_email
from django.forms import ValidationError
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/accounts/profile/')
    else:
        return HttpResponseRedirect('/accounts/login/')
        
def login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")


    form = CustomLoginForm()
    return render(request, template_name="accounts/login.html", context={"form":form})

@csrf_exempt
def mobile_logout(request):
    logout(request)
    return JsonResponse({}, status=200)

@csrf_exempt
def mobile_login(request):
    try:
        user = authenticate(username=request.POST['username'], password=request.POST['password'])

        if user is not None:
            auth_login(request, user)
            return HttpResponse("login-success", status=200)
        else: 
            return HttpResponse("login-failed", status=401)

    except Exception as e:
        return HttpResponse('ERROR: ' + str(e), status=500)

@csrf_exempt
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
                auth_login(request,user)
                
            return HttpResponseRedirect("/accounts/profile/")
    else:
        profile_form = ProfileForm()
        user_form = RegistrationForm()

    return render(request, "accounts/register.html", context={
        'user_form' : user_form, 
        'profile_form': profile_form
    })

@csrf_exempt
def mobile_register(request):
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']

    if request.method != 'POST':
        return JsonResponse({'status':'bad-request'}, status=501)
    
    if User.objects.filter(username=username).exists():
        return JsonResponse({'status':'username-taken'}, status=400)

    if User.objects.filter(email=email).exists():
        return JsonResponse({'status':'email-taken'}, status=400)

    try:
        validate_email(email)
    except ValidationError as e:
        return JsonResponse({'status':'email-invalid'}, status=400)
    
    user = User.objects.create_user(username, email, password)
    authenticated_user = authenticate(username=username, password=password)

    if authenticated_user is not None:
        return JsonResponse({'status':'success'}, status=200)

    return JsonResponse({'status':'unknown'}, status=500)


def profile_authed(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user_detail', args=[request.user.username]))
    else:
        return HttpResponseRedirect('/accounts/login/')

def profile(request, username):
    if request.user.is_authenticated:
        u = User.objects.get(username=username)
        p = Profile.objects.get(user=u)

        user_form = UserForm(instance=u)      
        user_form.merge_from_initial()

        return render(request, 'accounts/profile.html', context={
            'username': u.username,
            'user_f': user_form, 
            'profile': p,
        })
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
        
    return render(request, "accounts/edit.html", context={
        'user_form' : user_form, 
        'profile_form': profile_form
    })