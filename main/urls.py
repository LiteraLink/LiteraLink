from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.show_all_books, name="show_main"),
    path('fetch_api_data/', views.seeding_data, name='fetch_api_data'),
    path('show_json/', views.show_json, name='show_json'),
    path('flush/', views.flush, name='flush'),
]