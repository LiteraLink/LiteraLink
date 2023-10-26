from random import sample
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from DimanaSajaKapanSaja.forms import StationForm
from DimanaSajaKapanSaja.models import Station, StationBook
from authentication.models import UserProfile
from main.models import Book
from django.contrib.auth.decorators import login_required

# Create your views here.

# def distribute_book(request, station_id):
#     station = Station.objects.get(id=station_id)
#     amount = station.rentable
#     books = sample(list(Book.objects.all()), amount)

#     for book in books:
#         station_book = StationBook(
#             station=station,
#             bookID=book.bookID,
#             title=book.title,
#             authors=book.authors,
#             display_authors=book.display_authors,
#             description=book.description,
#             categories=book.categories,
#             thumbnail=book.thumbnail,
#         )
#         station_book.save()

def flush(request):
    books = StationBook.objects.all()
    books.delete()

    response = HttpResponse("flushhhh")
    return response

@login_required(login_url='auth:signin')
def show_station(request):
    station = Station.objects.all()
    # station_book = StationBook.objects.filter(station_id=station.id)

    context = {"stations": station}
    response = render(request, "dimanasajakapansaja_page.html", context)

    return response

def show_station_detail(request, station_id):
    station = Station.objects.get(id=station_id)
    station_book = StationBook.objects.filter(station=station_id)
    member = UserProfile.objects.get(user=request.user)

    context = {
        "station": station,
        "user": member,
        "books": station_book
    }
    response = render(request, "station_detail.html", context)

    return response
    

def add_station(request):
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
            station_book = StationBook(
                station=station,
                bookID=book.bookID,
                title=book.title,
                authors=book.authors,
                display_authors=book.display_authors,
                description=book.description,
                categories=book.categories,
                thumbnail=book.thumbnail,
            )
            station_book.save()

        return HttpResponseRedirect(reverse('dimanasajakapansaja:show_station'))
    
    

    context = {'form': form}
    response = render(request, "add_station.html", context)

    return response

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

def del_station(request, station_id):
    station = Station.objects.filter(id=station_id)
    station.delete()

    response = redirect('dimanasajakapansaja:show_station')
    return response



