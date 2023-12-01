from django.urls import path
from . import views

app_name = 'bacaditempat'

urlpatterns = [
    path('', views.show_list_venue, name="show_list_venue"),
    path('venue/<int:venue_id>/', views.show_detail_venue, name="show_detail_venue"),
    path('status/<int:venue_id>/', views.show_list_status, name="show_list_status"),
    path('add_venue/', views.add_venue, name="add_venue"),
    path('edit_venue/<int:venue_id>/', views.edit_venue, name="edit_venue"),
    path('delete_venue/<int:venue_id>/', views.delete_venue, name="delete_venue"),
    path('books/', views.list_books, name="list_books"),
    path('get-product/', views.get_product_json, name='get_product_json'),
    path('xml/', views.show_xml, name='show_xml'), 
    path('json/', views.show_json, name='show_json'), 
    path('xml/<int:id>/', views.show_xml_by_id, name='show_xml_by_id'), 
    path('json/<int:id>/', views.show_json_by_id, name='show_json_by_id'),
    path('pemesanan/<int:id>/', views.pemesanan, name="pemesanan"),
    path('add_book/<int:id>/', views.add_book, name="add_book"),
    path('sub_book/<int:id>/', views.sub_book, name="sub_book"),
    path('bacaditempat/pesan_buku_ajax/<int:book_id>/', views.pesan_buku_ajax, name="pesan_buku_ajax"),
    path('rent_book/<int:book_id>/', views.rent_book, name='rent_book'),
    path('return_book/<int:book_id>/', views.return_book, name='return_book'),
    path('get-venue/', views.get_venue_json, name='get_venue_json'),
    path('ajax/rent_book/<int:book_id>/', views.pesan_buku_ajax, name='ajax_rent_book'),
    path('load-more-venue/', views.load_more_venue, name='load-more-venue'),
    path('show-detail-books/<int:id>', views.show_detail_books, name='show_detail_books'),
]
