import json
from django.db.models import Count
from django.utils import timezone
from django.shortcuts import render
from Bibliofilia.forms import BibliofiliaForm
from Bibliofilia.models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseForbidden, HttpResponseNotFound, HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages 
from django.views.decorators.csrf import csrf_exempt
from authentication.models import UserProfile, UserBook
from main.models import Book


@login_required(login_url='auth:signin')
def showForum(request):
    forum = Forum.objects.all()
    member = UserProfile.objects.get(user=request.user)
    context = {
        'name': request.user.username,
        'forum': forum,
        'member': member,
    }

    return render(request, "mainforum.html", context)

@login_required(login_url='auth:signin')
def showChildForum(request, forum_id):
    if forum_id is not None:
        try:
            forum = Forum.objects.get(pk=forum_id)
            forum_head_msg = forum.userReview 
            forum_title = forum.BookName
            member = UserProfile.objects.get(user=request.user)
        except Forum.DoesNotExist:
            return HttpResponseNotFound("Forum not found")

        context = {
            'forum_id': forum_id,
            'forum_head_msg': forum_head_msg,
            'name': request.user.username,
            'forum': forum,
            'forum_title':forum_title,
            'member': member,
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
def delete_Forum(request, forum_id):
    user = UserProfile.objects.get(user=request.user)
    if(user.role != 'A'):
        response = HttpResponseForbidden("Access Denied")
        return response
    
    if request.method == 'DELETE':
        forum = Forum.objects.get(pk=forum_id)
        forum.user = request.user
        forum.delete()
        return HttpResponse(b"REMOVED", status=201)
    return HttpResponseNotFound()


@csrf_exempt
def delete_Replies(request, reply_id):
    user = UserProfile.objects.get(user=request.user)
    print(request.user.username, user.role)
    if(user.role != 'A'):
        response = HttpResponseForbidden("Access Denied")
        return response

    if request.method == 'DELETE':
        try:
            # Retrieve the ForumReply
            forumReplies = ForumReply.objects.get(pk=reply_id)
            
            # Retrieve the related Forum
            forum = forumReplies.forum
            
            # Ensure that the user is the owner of the ForumReply
            if user.role == 'A':
                # Decrement the repliesTotal field of the related Forum
                if forum.repliesTotal > 0:
                    forum.repliesTotal -= 1
                    forum.save()  # Save the Forum object to update repliesTotal
                # Delete the ForumReply
                forumReplies.delete()
                return HttpResponse(b"REMOVED", status=201)
            else:
                return HttpResponse(b"Unauthorized", status=401)
        except ForumReply.DoesNotExist:
            return HttpResponseNotFound("ForumReply not found")
    return HttpResponseNotFound()


def get_Forum_json(request):
    forum = Forum.objects.all()
    # forum.user = request.user
    return HttpResponse(serializers.serialize('json', forum), content_type='application/json')

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

        new_product = Forum(
            BookName=BookName,
            bookPicture=bookPicture,
            userReview=userReview,
            forumsDescription=forumsDescription,
            repliesTotal=0, 
            user=user, 
            username=user.username)
        
        new_product.save()

        return HttpResponse(b"CREATED", status=201)
    return HttpResponseNotFound()

@csrf_exempt 
def add_replies_ajax(request):
    if request.method == 'POST':
        text = request.POST.get("text")
        user = request.user
        forum_id = request.GET.get("forum_id")
        forumMain = Forum.objects.get(pk=forum_id)
        forumMain.repliesTotal += 1
        forumMain.save()

        forum = get_object_or_404(Forum, id=forum_id)

        new_reply = ForumReply(text=text, user=user, forum=forum, username=user.username)
        new_reply.save()

        # Return the updated repliesTotal value in the response
        response_data = {
            'repliesTotal': forumMain.repliesTotal
        }

        return JsonResponse(response_data, status=201)
    return HttpResponseNotFound()

#Below is function for flutter

@csrf_exempt
def add_Forum_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        user = User.objects.get(username=data['username'])
        # user = UserProfile.objects.get(user=user)
        print("TEST")
        new_product = Forum(
            BookName=data['bookname'],
            bookPicture='',
            userReview=data['userReview'],
            forumsDescription=data['forumsDescription'],
            repliesTotal=0, 
            user=user, 
            username=data['username']
        )
        
        new_product.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)
    
@csrf_exempt
def add_BookForum_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        user = User.objects.get(username=data['username'])
        Userprofile = UserProfile.objects.get(user=user)

        selectedBook = Book.objects.get(id=data["book_id"])

        new_product = Forum(
            userbook = selectedBook,
            BookName = selectedBook.title,
            bookPicture = selectedBook.thumbnail,
            userReview= data['userReview'],
            forumsDescription= data['forumsDescription'],
            repliesTotal=0, 
            user=user, 
            username=data['username']
        )
        # print(new_product[bookNam])
        print("TEST")
        new_product.save()

        # new_product.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)    

@csrf_exempt    
def add_replies_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        userDjango = User.objects.get(username=data['username'])
        user = UserProfile.objects.get(user=userDjango.id)
        forum_id = data['forum_id']
        forumMain = Forum.objects.get(pk=data['forum_id'])
        forumMain.repliesTotal += 1
        forumMain.save()

        forum = get_object_or_404(Forum, id=forum_id)

        new_reply = ForumReply(
            text = data['text'],
            user=userDjango, 
            forum=forum, 
            username=data['username'],

        )
        new_reply.save()

        # Return the updated repliesTotal value in the response
        response_data = {
            'status' : 'success',
            'repliesTotal': forumMain.repliesTotal
        }

        return JsonResponse(response_data, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)
    
@csrf_exempt
def delete_Forum_Flutter(request):
    data = json.loads(request.body)
    user = User.objects.get(username=data['username']).id
    user = UserProfile.objects.get(user=user)
    if user.role != 'A':
        return JsonResponse({'error': 'Access Denied'}, status=403)

    if request.method == 'DELETE':
        try:
            forum = Forum.objects.get(pk=data['forum_id'])
            forum.delete()
            return JsonResponse({'message': 'REMOVED'}, status=204)
        except Forum.DoesNotExist:
            return JsonResponse({'error': 'Forum not found'}, status=404)

    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
def delete_Replies_Flutter(request):
    data = json.loads(request.body)
    reply_id = data['reply_id']
    try:
        forumReplies = ForumReply.objects.get(pk=reply_id)

        # if user.role == 'A':
        forum = forumReplies.forum
        if forum.repliesTotal > 0:
            forum.repliesTotal -= 1
            forum.save()
        forumReplies.delete()
        return JsonResponse({'message': 'REMOVED'}, status=204)
        # else:
        #     return JsonResponse({'error': 'Unauthorized'}, status=401)
    except ForumReply.DoesNotExist:
        return JsonResponse({'error': 'ForumReply not found'}, status=404)


def get_ForumReply_json_flutter(request, forum_id):
    forum_replies = ForumReply.objects.filter(forum=forum_id)
    serialized_data = serializers.serialize('json', forum_replies)
    
    response = HttpResponse(content=serialized_data, content_type='application/json')
    return response


def get_ForumReplyHead_json_flutter(request, forum_id):
    forum_replies = Forum.objects.filter(id=forum_id)
    serialized_data = serializers.serialize('json', forum_replies)
    
    response = HttpResponse(content=serialized_data, content_type='application/json')
    return response

def get_Book_flutter(request, forum_id):
    Book = UserBook.objects.filter(id=forum_id)
    serialized_data = serializers.serialize('json', Book)
    
    response = HttpResponse(content=serialized_data, content_type='application/json')
    return response