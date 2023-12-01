from random import sample
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from DimanaSajaKapanSaja.forms import StationForm
from DimanaSajaKapanSaja.models import Station, StationBook
from authentication.models import UserBook, UserProfile
from main.models import Book
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

def create_station_book(station, book):
    return StationBook(
        station=station,
        bookID=book.bookID,
        title=book.title,
        authors=book.authors,
        display_authors=book.display_authors,
        description=book.description,
        categories=book.categories,
        thumbnail=book.thumbnail,
    )


@login_required(login_url='auth:signin')
def show_station(request):
    station = Station.objects.all()
    member = UserProfile.objects.get(user=request.user)

    context = {
        "stations": station,
        "user": member,
    }
        
    response = render(request, "dimanasajakapansaja_page.html", context)

    return response

@login_required(login_url='auth:signin')
def show_station_detail(request, station_id, QUERY=None):
    category_set = set()
    station = Station.objects.get(id=station_id)
    books = StationBook.objects.filter(station=station_id)

    for book in books:
        categories = book.categories
        category_splitted = [category.strip() for category in categories.split(',')]

        if(len(category_splitted)>1):
            for category in category_splitted:
                category_set.add(category)
        else:
            category_set.add(category_splitted[0])

    category_list = list(category_set)
    category_list.insert(0, "All")

    if QUERY == None or QUERY == "All":
        station_book = StationBook.objects.filter(station=station_id)
    else:
        station_book = StationBook.objects.filter(station=station_id).filter(categories=QUERY)

    member = UserProfile.objects.get(user=request.user)
    rented_book = UserBook.objects.filter(feature="DSKS").filter(user=member)

    context = {
        "station": station,
        "user": member,
        "books": station_book,
        "rented_books": rented_book,
        "categories": category_list
    }
    response = render(request, "station_detail.html", context)

    return response

@login_required(login_url='auth:signin')
@csrf_exempt
def add_station_ajax(request):
    station_id = 0
    user = UserProfile.objects.get(user=request.user)
    if(user.role != 'A'):
        response = HttpResponseForbidden("Access Denied")
        return response
    
    if request.method == 'POST':
        name = request.POST.get("name")
        address = request.POST.get("address")
        opening_hours = request.POST.get("opening_hours")
        rentable = request.POST.get("rentable")
        returnable = request.POST.get("returnable")
        map_location = request.FILES.get("map_location")

        station = Station(name=name, address=address, opening_hours=opening_hours, rentable=rentable, returnable=returnable, map_location=map_location)
        station.save()
        station_id = station.id

        station = Station.objects.get(id=station_id)
        amount = station.rentable
        books = sample(list(Book.objects.all()), amount)

        for book in books:
            station_book = create_station_book(station, book)
            station_book.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()

@login_required(login_url='auth:signin')
@csrf_exempt
def get_station_json(request):
    station = Station.objects.all()
    response = HttpResponse(serializers.serialize('json', station))
    return response
    
@login_required(login_url='auth:signin')
@csrf_exempt
def add_station(request):
    user = UserProfile.objects.get(user=request.user)
    if(user.role != 'A'):
        response = HttpResponseForbidden("Access Denied")
        return response
    station_id = 0

    form = StationForm(request.POST, request.FILES)

    if form.is_valid() and request.method == "POST":
        station = form.save(commit=False)
        station.save()
        station_id = station.id

        station = Station.objects.get(id=station_id)
        amount = station.rentable
        books = sample(list(Book.objects.all()), amount)

        for book in books:
            station_book = create_station_book(station, book)
            station_book.save()

        return HttpResponseRedirect(reverse('dimanasajakapansaja:show_station'))

    context = {'form': form}
    response = render(request, "add_station.html", context)

    return response

@login_required(login_url='auth:signin')
@csrf_exempt
def edit_station(request, station_id):
    user = UserProfile.objects.get(user=request.user)
    if(user.role != 'A'):
        response = HttpResponseForbidden("Access Denied")
        return response
    
    station = Station.objects.get(pk = station_id)

    initial_data = {
        'name': station.name,
        'address': station.address,
        'opening_hours': station.opening_hours,
        'rentable': station.rentable,
        'returnable': station.returnable,
        'map_location': station.map_location,
    }

    form = StationForm(request.POST or None, initial=initial_data, instance=station)

    if form.is_valid() and request.method == "POST":
        if 'map_location' in request.FILES:
            print("abc")
            station.map_location = request.FILES.get("map_location")
        form.save()
        print("def")
        return HttpResponseRedirect(reverse('dimanasajakapansaja:show_station'))

    context = {'form': form}
    response = render(request, "edit_station.html", context)
    return response

@login_required(login_url='auth:signin')
@csrf_exempt
def del_station(request, station_id):
    user = UserProfile.objects.get(user=request.user)
    if(user.role != 'A'):
        response = HttpResponseForbidden("Access Denied")
        return response
    
    station = Station.objects.filter(id=station_id)
    station.delete()

    response = redirect('dimanasajakapansaja:show_station')
    return response

@login_required(login_url='auth:signin')
@csrf_exempt
def rent_book(request, book_id):
    user = UserProfile.objects.get(user=request.user)
    book = StationBook.objects.get(id=book_id)
    station_id = book.station.pk
    station = Station.objects.get(id=station_id)
    rented_book = UserBook(
        user=user, 
        bookID=book.bookID, 
        title=book.title, 
        authors=book.authors, 
        display_authors=book.display_authors, 
        description=book.description, 
        categories=book.categories, 
        thumbnail=book.thumbnail, 
        feature="DSKS"
    )

    station.rentable-=1
    station.returnable+=1
    
    station.save()
    rented_book.save()
    book.delete()
    
    response = HttpResponseRedirect(reverse("dimanasajakapansaja:detail", args=[station_id]))
    return response

@login_required(login_url='auth:signin')
@csrf_exempt
def return_book(request, station_id ,book_id):
    user = UserProfile.objects.get(user=request.user)
    if(user.role != 'M'):
        response = HttpResponseForbidden("Access Denied")
        return response
    
    book = UserBook.objects.get(id=book_id)
    station = Station.objects.get(id=station_id)
    returned_book = create_station_book(station, book)

    station.rentable+=1
    station.returnable-=1
    
    station.save()
    returned_book.save()
    book.delete()

    response = HttpResponseRedirect(reverse("dimanasajakapansaja:detail", args=[station_id]))
    return response

@login_required(login_url='auth:signin')
@csrf_exempt
def get_category(request, station_id):

    QUERY = request.GET.get('query')

    return show_station_detail(request, station_id ,QUERY)

def show_detail_book(request, book_title):
    books = Book.objects.get(title=book_title)

    context= {
        'bookID':books.bookID,
        'title' :books.title,
        'authors' : books.authors,
        'display_authors' : books.display_authors,
        'description' : books.description,
        'categories' : books.categories,
        'thumbnail' : books.thumbnail
    }
    return render(request,'detailBooks.html',context)

def flush(request):
    books = StationBook.objects.all()
    books.delete()

    response = HttpResponse("flushhhh")
    return response

