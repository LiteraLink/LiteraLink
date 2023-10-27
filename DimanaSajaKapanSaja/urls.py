from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'dimanasajakapansaja'

urlpatterns = [
    path('', views.show_station, name="show_station"),
    path('flush/', views.flush, name='flush'),
    path('add_station/', views.add_station, name='add_station'),
    path('del_station/<int:station_id>/', views.del_station, name='del_station'),
    path('edit_station/<int:station_id>/', views.edit_station, name='edit_station'),
    path('detail/<int:station_id>/', views.show_station_detail, name='detail'),
    path('rent_book/<int:book_id>/', views.rent_book, name='rent_book'),
    path('return_book/<int:station_id>/<int:book_id>/', views.return_book, name='return_book'),
]