app_name = ''

from django.urls import path
from . import views

urlpatterns = [
    path('fetch_api_data/', views.seeding_data, name='fetch_api_data'),
    path('show_json/', views.show_json, name='show_json'),
]