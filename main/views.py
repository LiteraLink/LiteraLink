import requests
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from main.models import Book


# Create your views here.

API_KEY = 'AIzaSyBNVos8tjL-pRz01VYJBUeMAX_4Om-aiHU'

def seeding_data():

    # Satu URL berisi 40 buku
    api_urls = [
        f'https://www.googleapis.com/books/v1/volumes?q=random&maxResults=40&startIndex={i * 40}&key={API_KEY}' # Menggunakan startIndex untuk mengambil 40 buku lainnya
        for i in range(3)
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
            thumbnail = book_volume_info.get("imageLinks").get("thumbnail") if book_volume_info.get("imageLinks").get("thumbnail") is not None else "None"
            
            authors = book_volume_info.get("authors")
            if authors is not None:
                author = ', '.join(authors) # Memanipulasi list menjadi string
            else:
                author = "None"

            categories = book_volume_info.get("categories")
            if categories is not None:
                category = ', '.join(categories)
            else:
                category = 'None'

            book = Book(bookID = book_id, title = book_title, authors = author, description = description, thumbnail = thumbnail, categories = category)
            book.save()

    return JsonResponse(items, safe=False)
        

def show_json():
    data = Book.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
