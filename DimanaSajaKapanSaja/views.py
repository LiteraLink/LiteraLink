from random import sample
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from DimanaSajaKapanSaja.forms import StationForm
from DimanaSajaKapanSaja.models import Station, StationBook
from main.models import Book
from django.contrib.auth.decorators import login_required

# Create your views here.

def distribute_book(request, station_id):

    #TODO: Distribusi buku ke semua station
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

    return HttpResponse("halo")

def flush(request):
    books = Station.objects.all()
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

def add_station(request):
    form = StationForm(request.POST, request.FILES)

    if form.is_valid() and request.method == "POST":
        station = form.save(commit=False)
        station.save()
        return HttpResponseRedirect(reverse('dimanasajakapansaja:show_station'))

    context = {'form': form}
    response = render(request, "add_station.html", context)
    return response

def edit_station(request, station_id):
    station = Station.objects.get(pk = station_id)

    initial_data = {
        'name': station.name,
        'address': station.address,
        'opening_hours': station.opening_hours,
        'rentable': station.rentable,
        'returnable': station.returnable,
        'map_location': station.map_location
    }

    form = StationForm(request.POST or None, initial=initial_data, instance=station)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('dimanasajakapansaja:show_station'))

    context = {'form': form}
    response = render(request, "edit_station.html", context)
    return response

def del_station(request, station_id):
    station = Station.objects.filter(id=station_id)
    station.delete()

    response = redirect('dimanasajakapansaja:show_station')
    return response


