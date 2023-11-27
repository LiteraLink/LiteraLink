import datetime
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib import messages
from authentication.forms import SignUpForm
from authentication.models import UserBook, UserProfile
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from django.core import serializers
from django.contrib.auth.models import User

# Create your views here.
@csrf_exempt
def signup(request):
    print(request.POST) #debug
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(user.username)
            user_profile = UserProfile(user=user, full_name=user.full_name, email=user.email, role=user.role)
            user_profile.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('auth:signin')
    context = {'form':form}
    response = render(request, 'signup.html', context)
    return response

@csrf_exempt
def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main")) 
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.info(request, 'Sorry, incorrect username or password. Please try again.')
    context = {}
    response = render(request, 'signin.html', context)
    return response

@csrf_exempt
def signout(request):
    auth_logout(request)
    response = redirect('auth:signin')
    return response

@csrf_exempt
@login_required(login_url='auth:signin')
def show_profile(request):
    profile = UserProfile.objects.filter(user=request.user).first()
    return render(request, 'profile.html', {'profil':profile})

# Flutter Auth Integration Function
@csrf_exempt
def signin_flutter(request):
    print(request.body) #debug
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    user_profile = UserProfile.objects.filter(user=user).first()
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            # Status login sukses.
            return JsonResponse({
                "status": True,
                "message": "Successfully Signed Up!",
                "username": user.username,
                "full_name": user_profile.full_name,
                "email": user_profile.email,
                "role": user_profile.role
            }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Login gagal, akun dinonaktifkan."
            }, status=401)

    else:
        return JsonResponse({
            "status": False,
            "message": "Login gagal, periksa kembali email atau kata sandi."
        }, status=401)
    
@csrf_exempt
def signout_flutter(request):
    username = request.user.username

    try:
        auth_logout(request)
        return JsonResponse({
            "username": username,
            "status": True,
            "message": "Logout berhasil!"
        }, status=200)
    except:
        return JsonResponse({
        "status": False,
        "message": "Logout gagal."
        }, status=401)
    
@csrf_exempt
def signup_flutter(request):
    print(request.POST) #debug
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_profile = UserProfile(user=user, full_name=user.full_name, email=user.email, role=user.role)
            user_profile.save()
            return JsonResponse({
                "status": True,
                "message": "Successfully Signed Up!",
            }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Failed to Sign Up, Account Disabled."
            }, status=401)
    else:
         return JsonResponse({
            "status": False,
            "message": "Failed to Sign Up, check your username/password."
        }, status=401)
    
@csrf_exempt
def show_all_profile(request):
    data = User.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def filter_user(request):
    abc = []
    data = User.objects.get(username="marcelinoa").id
    data = UserProfile.objects.get(user_id=data).id
    data = UserBook.objects.filter(user_id=data)
    for d in data:
        abc.append(d.title)
    return HttpResponse(abc)