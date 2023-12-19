from collections import UserDict
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, JsonResponse, HttpResponseForbidden
from django.core import serializers
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from BacaDiTempat.models import Venue, BookVenue
from BacaDiTempat.forms import VenueForm
from main.models import Book
from authentication.models import UserBook, UserProfile
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from random import sample
from django.template.loader import render_to_string
from django.contrib.auth.models import User

@login_required(login_url='auth:signin')
def show_list_venue(request):
    venue = Venue.objects.all()[:1]
    total_venue = Venue.objects.count()
    
    is_admin = False
    user = UserProfile.objects.get(user=request.user)
    if(user.role == 'A'):
        is_admin = True
    
    context = {"venues": venue,
               "total_venue": total_venue,
               "load_button": True,
               "is_admin": is_admin}
    response = render(request, "bacaditempat_main.html", context)

    return response

@login_required(login_url='auth:signin')
def show_venue(request):
    venue = Venue.objects.all()
    member = UserProfile.objects.get(user=request.user)

    context = {
        "venues": venue,
        "user": member,
    }
        
    response = render(request, "bacaditempat_main.html", context)

    return response

@csrf_exempt
def show_detail_books(request, id=None):
    books = Book.objects.get(pk=id)

    context= {
        'bookID':books.bookID,
        'title' :books.title,
        'authors' : books.authors,
        'display_authors' : books.display_authors,
        'description' : books.description,
        'categories' : books.categories,
        'thumbnail' : books.thumbnail
    }
    return render(request,'book_details.html',context)

@csrf_exempt
def show_detail_venue(request, venue_id):
    venue = Venue.objects.get(id=venue_id)
    book_venue = BookVenue.objects.filter(venue=venue_id)
    member = UserProfile.objects.get(user=request.user)
    
    book_available = []
    book_rented = []
    
    for book in book_venue:
        if book.user == None:
            book_available.append(book)
        else:
            book_rented.append(book)

    context = {
        "venue": venue,
        "user": member,
        "books": book_available,
        "book_rented": book_rented,
    }
    response = render(request, "venue_detail.html", context)

    return response

@csrf_exempt
def show_list_status(request, venue_id):
    book_venue = BookVenue.objects.filter(venue=venue_id)
    
    context = {
        "books": book_venue
    }
    
    return render(request, 'bacaditempat_status.html', context)

@login_required(login_url='auth:signin')
@csrf_exempt
def add_venue(request):
    venue_id = 0
    form = VenueForm(request.POST or None, request.FILES or None)

    if request.method == "POST":
        if form.is_valid():
            venue = form.save(commit=False)

            venue.save()
            venue_id = venue.id

            venue = Venue.objects.get(id=venue_id)
            amount = venue.rent_book
            books = sample(list(Book.objects.all()), amount)

            for book in books:
                book_venue = BookVenue(
                    venue=venue,
                    bookID=book.bookID,
                    title=book.title,
                    authors=book.authors,
                    display_authors=book.display_authors,
                    description=book.description,
                    categories=book.categories,
                    thumbnail=book.thumbnail,
                )
                book_venue.save()

            return HttpResponseRedirect(reverse('bacaditempat:show_list_venue'))

    context = {'form': form}
    response = render(request, "add_venue.html", context)

    return response

@csrf_exempt
def edit_venue(request, venue_id):
    user = UserProfile.objects.get(user=request.user)
    if(user.role != 'A'):
        response = HttpResponseForbidden("Access Denied")
        return response
    
    venue = Venue.objects.get(pk = venue_id)

    initial_data = {
        'place_name': venue.place_name,
        'price': venue.price, 
        'address': venue.address,
        'venue_open': venue.venue_open,
        'map_location': venue.map_location,
    }

    form = VenueForm(request.POST or None, initial=initial_data, instance=venue)

    if form.is_valid() and request.method == "POST":
        if 'map_location' in request.FILES:
            print("abc")
            venue.map_location = request.FILES.get("map_location")
        form.save()
        print("def")
        return HttpResponseRedirect(reverse('bacaditempat:show_list_venue'))

    context = {'form': form}
    response = render(request, "edit_venue.html", context)

    return response

@csrf_exempt
def delete_venue(request, venue_id):
    user = UserProfile.objects.get(user=request.user)
    if(user.role != 'A'):
        response = HttpResponseForbidden("Access Denied")
        return response
    
    venue = Venue.objects.filter(id=venue_id)
    venue.delete()

    response = redirect('bacaditempat:show_list_venue')
    return response

@csrf_exempt
def list_books(request):
    # objek buku dari model Book
    books = Book.objects.all()

    # Mengirimkan data buku ke template untuk ditampilkan
    return render(request, 'bacaditempat_main.html', {'books': books})

@csrf_exempt
def show_xml(request):
    data = Book.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Book.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = Book.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Book.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


@csrf_exempt
def rent_book(request, book_id):
    user = UserProfile.objects.get(user=request.user)

    if(user.role != 'M'): # User harus merupakan member untuk meminjam buku
        response = HttpResponseForbidden("Access Denied")
        return response
      
    book_venue = BookVenue.objects.get(pk=book_id)
    book_venue.user = user
    venue_id = book_venue.venue.pk
    venue = Venue.objects.get(pk=venue_id)

    venue.rent_book-=1
    venue.return_book+=1
    
    venue.save()
    book_venue.save()

    response = HttpResponseRedirect(reverse("bacaditempat:show_list_status", args=[venue_id]))
    return response

@csrf_exempt
def return_book(request, book_id):
    user = UserProfile.objects.get(user=request.user)
    
    if(user.role != 'M'): # User harus merupakan member untuk mengembalikan buku
        response = HttpResponseForbidden("Access Denied")
        return response
    
    book_venue = BookVenue.objects.get(pk=book_id)
    
    if book_venue.user == user:
        book_venue.user = None
    
        venue_id = book_venue.venue.pk
        venue = Venue.objects.get(pk=venue_id)

        venue.rent_book+=1
        venue.return_book-=1
    
        venue.save()
        book_venue.save()

    response = HttpResponseRedirect(reverse("bacaditempat:show_list_status", args=[venue_id]))
    return response


@csrf_exempt
def pesan_buku_ajax(request, book_id):
    book = Book.objects.get(bookID=book_id)
    
    if request.method == 'POST':
        person_name = request.POST.get("person_name")
        phone_number = request.POST.get('phone_number')
        user = request.user

        # Mengambil date_use dan date_return dari POST request dan mengubahnya menjadi objek datetime
        date_use_str = request.POST.get("date_use")
        date_return_str = request.POST.get("date_return")

        date_format = "%H:%M"  # Format waktu dalam jam:menit
        date_use = datetime.strptime(date_use_str, date_format).time()  # Mengambil bagian waktunya saja
        date_return = datetime.strptime(date_return_str, date_format).time()

        # Menghitung durasi dalam jam
        duration_hours = (datetime.combine(datetime.today(), date_return) - datetime.combine(datetime.today(), date_use)).seconds / 3600

        # total harga peminjaman per jam
        price_per_hour = 1000 
        total_price = price_per_hour * duration_hours

        # Membuat dan menyimpan entri Venue baru
        venue_booked = Venue(
            person_name=person_name,
            phone_number=phone_number,
            book_name=book.title,
            place_name="Nama Tempat",  # Anda dapat menggantinya sesuai dengan input atau data lainnya
            price=total_price,
            address="Alamat Tempat",  # Anda dapat menggantinya sesuai dengan input atau data lainnya
            venue_open="Jam Buka Tempat",  # Anda dapat menggantinya sesuai dengan input atau data lainnya
            rent_book=1,  # Anda dapat menggantinya sesuai dengan jumlah buku yang dipesan
            date_use=datetime.combine(datetime.today(), date_use),
            date_return=datetime.combine(datetime.today(), date_return)
        )
        venue_booked.save()

        # Menentukan status peminjaman
        if venue_booked.date_return and venue_booked.date_return < datetime.now():
            status = "Dikembalikan"
        else:
            status = "Dipinjam"

        context = {
            'user' : user,
            'person_name' : person_name,
            'phone_number' : phone_number,
            'book_name' : book.title,
            'status' : status
        }

        # Menambahkan notifikasi
        messages.success(request, 'Berhasil Memesan!')

        return render(request, 'bacaditempat_main.html', context)

    # Jika request bukan POST (misalnya GET), Anda dapat mengembalikan respons lain atau mengarahkan ke halaman lain.
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@csrf_exempt
def load_more_venue(request):
    if is_ajax(request):
        offset = int(request.GET['offset'])
        limit = int(request.GET['limit'])
        venues = Venue.objects.all()[offset:offset+limit]
        data = render_to_string(
            'ajax/list-venue.html',
            {'venues': venues}
        )
        return JsonResponse({'data': data})

def is_ajax(request):
    """
    https://stackoverflow.com/questions/63629935
    """
    return (
        request.headers.get('x-requested-with') == 'XMLHttpRequest'
        or request.accepts("application/json")
    )

@csrf_exempt
def create_book_venue(venue, book):
    return BookVenue(
        venue=venue,
        bookID=book.bookID,
        title=book.title,
        authors=book.authors,
        display_authors=book.display_authors,
        description=book.description,
        categories=book.categories,
        thumbnail=book.thumbnail,
    )


@csrf_exempt
def rent_book_flutter(request, book_id):
    if request.method == 'POST':
        data = json.loads(request.body)

        user = UserProfile.objects.get(user__username=data['username'])

        book = BookVenue.objects.get(id=book_id)
        book.user = user
        venue_id = book.venue.id
        venue = Venue.objects.get(id=venue_id)

        venue.rent_book-=1
        venue.return_book+=1

        venue.save()
        book.save()
        # book.delete()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)

@csrf_exempt
def return_book_flutter(request, venue_id, book_id):
    if request.method == 'POST':

        data = json.loads(request.body)
        book = BookVenue.objects.get(id=book_id)
     
        venue = Venue.objects.get(id=venue_id)
        returned_book = BookVenue(
            venue=venue,
            bookID = data["book_id"],
            title = data["title"], 
            authors = data["authors"], 
            display_authors = data["display_authors"], 
            description = data["description"], 
            categories = data["categories"], 
            thumbnail = data["thumbnail"], 
        )

        venue.rent_book+=1
        venue.return_book-=1

        returned_book.save()
        book.delete()
        venue.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)

@csrf_exempt 
def add_venue_flutter(request):
    if request.method == 'POST':
        place_name = request.POST.get("place_name")
        address = request.POST.get("address")
        venue_open = request.POST.get("venue_open")
        rent_book = request.POST.get("rent_book")
        return_book = request.POST.get("return_book")
        # map_location = request.FILES.get("map_location")
        map_location = "images/cafe.jpeg"

        new_venue = Venue(
            place_name=place_name,
            address=address,
            venue_open=venue_open,
            rent_book=rent_book,
            return_book=return_book,
            map_location=map_location
        )
        new_venue.save()

        venue = Venue.objects.get(id=new_venue.id)
        amount = venue.rent_book
        books = sample(list(Book.objects.all()), amount)

        for book in books:
            book_venue = create_book_venue(venue, book)
            book_venue.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=400)
    
@csrf_exempt
def del_venue_flutter(request):
    data = json.loads(request.body)
    venue = Venue.objects.get(id=data["venue_id"])
    venue.delete()

    return JsonResponse({"status": "success"}, status=200)

@csrf_exempt
def edit_venue_flutter(request, venue_id):
    venue = Venue.objects.get(id=venue_id)

    initial_data = {
        'place_name': venue.place_name,
        'address': venue.address,
        'venue_open': venue.venue_open,
        'rent_book': venue.rent_book,
        'return_book': venue.return_book,
        'map_location': venue.map_location,
    }

    form = VenueForm(request.POST or None, initial=initial_data, instance=venue)

    if form.is_valid() and request.method == "POST":
        if 'map_location' in request.FILES:
            venue.map_location = request.FILES.get("map_location")
        form.save()


    return JsonResponse({"status": "success"}, status=200)

@csrf_exempt
def book_distribution_json(request, venue_id):
    book = BookVenue.objects.filter(venue = venue_id)
    return HttpResponse(serializers.serialize("json", book), content_type="application/json")   

@csrf_exempt
def get_product_available(request, venue_id):
    books = BookVenue.objects.filter(venue__id=venue_id, user__isnull=True)
    return HttpResponse(serializers.serialize('json', books))

@csrf_exempt
def get_product_notavailable(request, venue_id):
    books = BookVenue.objects.filter(venue__id=venue_id, user__isnull=False)
    return HttpResponse(serializers.serialize('json', books))

@csrf_exempt
def get_venue_json(request):
    venue = Venue.objects.all()
    response = HttpResponse(serializers.serialize('json', venue))
    return response

@csrf_exempt
def show_venue_json(request):
    venue = Venue.objects.all()
    return HttpResponse(serializers.serialize("json", venue), content_type="application/json")