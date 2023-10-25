from django.shortcuts import render, redirect
from django.urls import reverse
import requests
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from main.models import Book

# Create your views here.

API_KEY = 'AIzaSyBNVos8tjL-pRz01VYJBUeMAX_4Om-aiHU'

def show_all_books(request):
    books = Book.objects.all()

    context = {"books": books}

    return render(request, "main.html", context)


def seeding_data(request):

    # Satu URL berisi 40 buku
    api_urls = [
        f'https://www.googleapis.com/books/v1/volumes?q=top+books&maxResults=40&startIndex={i * 40}&key={API_KEY}' # Menggunakan startIndex untuk mengambil 40 buku lainnya
        for i in range(25)
    ]

    for url in api_urls:
        response = requests.get(url)
        data = response.json()  
        items = data.get('items')

        for item in items:
            book_volume_info = item.get("volumeInfo") # Mengambil data dari list volume info

            book_id = item.get("id") if item.get("id") is not None else "None"
            book_title = book_volume_info.get("title") if book_volume_info.get("title") is not None else "None"
            description = book_volume_info.get("description") if book_volume_info.get("description") is not None else "None"
            thumbnail = book_volume_info.get("imageLinks", {}).get("thumbnail", "None")

            
            authors = book_volume_info.get("authors")
            if authors is not None:
                author = ', '.join(authors) # Memanipulasi list menjadi string
                author_list = author.split(', ')
                display_author = ', '.join(author_list[:2]) # Menyimpan dua author saja 
            else:
                author = "None"

            categories = book_volume_info.get("categories")
            if categories is not None:
                category = ', '.join(categories)
            else:
                category = 'None'

            if book_title=="None" or author=="None" or categories=="None" or thumbnail=="None":
                continue

            book = Book(bookID = book_id, title = book_title, authors = author, display_authors = display_author, description = description, thumbnail = thumbnail, categories = category)
            book.save()

    return JsonResponse(items, safe=False)

def flush(request):
    books = Book.objects.all()
    books.delete()

    return HttpResponse("flush")

def show_json(request):
    data = Book.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


