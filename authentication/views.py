import datetime
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from authentication.forms import SignUpForm
from authentication.models import UserProfile
from django.contrib.auth.decorators import login_required

# Create your views here.

def signup(request):
    form = SignUpForm()

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_profile = UserProfile(user=user, full_name=user.full_name, email=user.email, role=user.role)
            user_profile.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('auth:signin')
    context = {'form':form}
    response = render(request, 'signup.html', context)
    return response

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main")) 
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.info(request, 'Sorry, incorrect username or password. Please try again.')
    context = {}
    response = render(request, 'signin.html', context)
    return response
    
def signout(request):
    logout(request)
    response = redirect('auth:signin')
    return response

@login_required(login_url='auth:signin')
def show_profile(request):
    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'profile.html', {'profil':profile})