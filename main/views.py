from django.shortcuts import render
import requests
from django.http import JsonResponse

from main.models import Book


# Create your views here.

def seeding_data(request):
    external_api_url = 'https://www.googleapis.com/books/v1/volumes?q=random&maxResults=40&key=AIzaSyBNVos8tjL-pRz01VYJBUeMAX_4Om-aiHU'

    try:
        response = requests.get(external_api_url)
        data = response.json()  
        items = data.get('items')

        books = []

        for item in items:
            book = item
            print(item.get("id"))
            print(item.get("volumeInfo").get("title"))
            print(item.get("volumeInfo").get("authors"))
            print(item.get("volumeInfo").get("description"))
            print(item.get("volumeInfo").get("imageLinks").get("thumbnail"))
            print(item.get("volumeInfo").get("categories"))
            # Extract the relevant data from the 'item' dictionary
            # book_data = {
            #     'kind': item.get('kind', ''),
            #     'id': item.get('id', ''),
            #     'etag': item.get('etag', ''),
            #     'selfLink': item.get('selfLink', ''),
            #     # Add other fields here as needed
            # }

        #     for book in book_data:
        #         id = book[id]
        #         Book(id = id);
        #     # Create a Book model instance and append it to the 'books' list
        #     book_instance = Book(**book_data)
        #     print(book_instance)
        #     books.append(book_instance)

        # print(books)
        return JsonResponse(items, safe=False)

    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)})