from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'dimanasajakapansaja'

urlpatterns = [
    path('', views.show_station, name="show_station"),
    path('distribute/<int:station_id>/', views.distribute_book, name="distribute"),
    path('flush/', views.flush, name='flush'),
    path('add_station/', views.add_station, name='add_station'),
    path('del_station/<int:station_id>/', views.del_station, name='del_station'),
    path('edit_station/<int:station_id>/', views.edit_station, name='edit_station'),
]