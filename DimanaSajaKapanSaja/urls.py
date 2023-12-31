from django.urls import path
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
    path('get-station/', views.get_station_json, name='get_station_json'),
    path('add-station-ajax/', views.add_station_ajax, name='add_station_ajax'),
    path('search/<int:station_id>/', views.get_category, name='search'),
    path('show-detail-book/<str:book_title>/', views.show_detail_book, name='show_detail_books'),
    path('station-json/', views.show_station_json, name='show_station_json'),
    path('station-book-json/<int:station_id>/', views.book_distribution_json, name='station_book'),
    path('rent_book_flutter/<int:book_id>/', views.rent_book_flutter, name='rent_book_flutter'),
    path('return_book_flutter/<int:station_id>/<int:book_id>/', views.return_book_flutter, name='return_book_flutter'),
    path('user_book_json/<str:username>/', views.user_book_json, name='user_book_json'),
    path('add_station_flutter/', views.add_station_flutter, name="add_station_flutter"),
    path('del_station_flutter/', views.del_station_flutter, name="del_station_flutter"),
    path('edit_station_flutter/<int:station_id>/', views.edit_station_flutter, name='edit_station_flutter')
]