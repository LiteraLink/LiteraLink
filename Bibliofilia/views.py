import datetime
from django.utils import timezone
from django.shortcuts import render
from Bibliofilia.forms import *
from Bibliofilia.models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseNotFound, HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages 
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


@login_required(login_url='auth:signin')
def showForum(request):
    forum = Forum.objects.all()

    context = {
        'name': request.user.username,
        'Forum' : forum,
        # 'total_Forums' : len(Forums),
        # 'last_login': request.COOKIES['last_login'],
    }

    return render(request, "mainforum.html", context)

@login_required(login_url='auth:signin')
def showChildForum(request, forum_id):
    if forum_id is not None:
        try:
            forum = Forum.objects.get(pk=forum_id)
            forum_head_msg = forum.userReview 
            forum_title = forum.BookName
        except Forum.DoesNotExist:
            return HttpResponseNotFound("Forum not found")

        context = {
            'forum_id': forum_id,
            'forum_head_msg': forum_head_msg,
            'name': request.user.username,
            'forum': forum,
            'forum_title':forum_title,
        }
        return render(request, "childforum.html", context)
    else:
         return HttpResponse('Invalid request. Forum ID not provided.')

@login_required(login_url='auth:signin')
def showTest(request):
    context = {
        'name': request.user.username,
        # 'total_Forums' : len(Forums),
        # 'last_login': request.COOKIES['last_login'],
    }

    return render(request, "page1.html", context)

def create_Forum(request):
    form = Forum(request.POST or None)

    if form.is_valid() and request.method == "POST":
        forum = form.save(commit=False)
        forum.user = request.user
        forum.save()
        return HttpResponseRedirect(reverse('main:show_main'))

    context = {'form': form}
    return render(request, "create_Forum.html", context)


def show_json(request):
    data = Forum.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_by_id(request, id):
    data = Forum.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

@csrf_exempt
def add_amount(request, forum_id):
    if request.method == 'POST':
        forum = Forum.objects.get(pk=forum_id) #Mengakses Forum yang ingin dimodifikasi
        forum.user = request.user
        if forum.amount > 0:
            forum.amount += 1
            forum.save()
        return HttpResponse(b"ADDED", status=201)
    return HttpResponseNotFound()

@csrf_exempt
def reduce_amount(request, forum_id):
    if request.method == 'POST':
        forum = Forum.objects.get(pk=forum_id)
        forum.user = request.user
        if forum.amount > 1:
            forum.amount -= 1
            forum.save()
        else:
            forum.delete()
        return HttpResponse(b"REDUCED", status=201)
    return HttpResponseNotFound()

@csrf_exempt
def delete_Forum(request, forum_id):
    if request.method == 'DELETE':
        forum = Forum.objects.get(pk=forum_id, user=request.user)
        forum.user = request.user
        forum.delete()
        return HttpResponse(b"REMOVED", status=201)
    return HttpResponseNotFound()

def get_Forum_json(request):
    forum = Forum.objects.filter(user=request.user)
    forum.user = request.user
    return HttpResponse(serializers.serialize('json', forum))

def get_ForumReply_json(request):
    forum_replies = ForumReply.objects.all()
    serialized_data = serializers.serialize('json', forum_replies)
    
    response = HttpResponse(content=serialized_data, content_type='application/json')
    return response

@csrf_exempt
def add_Forum_ajax(request):
    if request.method == 'POST':
        BookName = request.POST.get("BookName")
        bookPicture = request.POST.get("bookPicture")
        forumsDescription = request.POST.get("forumsDescription")
        userReview = request.POST.get("userReview")    
        user = request.user

        new_product = Forum(BookName=BookName,bookPicture=bookPicture,userReview=userReview,forumsDescription=forumsDescription, user=user)
        
        new_product.save()

        return HttpResponse(b"CREATED", status=201)
    return HttpResponseNotFound()

def add_replies_ajax(request):
    if request.method == 'POST':
        text = request.POST.get("text")
        user = request.user
        forum_id = request.GET.get("forum_id")  # Use request.GET to access query parameters

        # Get the specific Forum instance based on the provided forum_id
        forum = get_object_or_404(Forum, id=forum_id)

        new_reply = ForumReply(text=text, user=user, forum=forum, username=user.username)
        new_reply.save()

        return HttpResponse(b"CREATED", status=201)
    return HttpResponseNotFound()