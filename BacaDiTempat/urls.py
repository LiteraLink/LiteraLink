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
    path('xml/', views.show_xml, name='show_xml'), 
    path('json/', views.show_json, name='show_json'), 
    path('xml/<int:id>/', views.show_xml_by_id, name='show_xml_by_id'), 
    path('json/<int:id>/', views.show_json_by_id, name='show_json_by_id'),
    path('bacaditempat/pesan_buku_ajax/<int:book_id>/', views.pesan_buku_ajax, name="pesan_buku_ajax"),
    path('rent_book/<int:book_id>/', views.rent_book, name='rent_book'),
    path('return_book/<int:book_id>/', views.return_book, name='return_book'),
    path('ajax/rent_book/<int:book_id>/', views.pesan_buku_ajax, name='ajax_rent_book'),
    path('load-more-venue/', views.load_more_venue, name='load-more-venue'),
    path('show-detail-books/<int:id>', views.show_detail_books, name='show_detail_books'),
    path('rent_book_flutter/<int:book_id>/', views.rent_book_flutter, name='rent_book_flutter'),
    path('return_book_flutter/<int:venue_id>/<int:book_id>/', views.return_book_flutter, name='return_book_flutter'),
    path('add_venue_flutter/', views.add_venue_flutter, name="add_venue_flutter"),
    path('del_venue_flutter/', views.del_venue_flutter, name="del_venue_flutter"),
    path('edit_venue_flutter/<int:venue_id>/', views.edit_venue_flutter, name='edit_venue_flutter'),
    path('get-product-available/<int:venue_id>/', views.get_product_available, name='get_product_available'),
    path('get-product-notavailable/<int:venue_id>/', views.get_product_notavailable, name='get_product_notavailable'),
    path('get-venue/', views.get_venue_json, name='get_venue_json'),
    path('venue-json/', views.show_venue_json, name='show_venue_json'),
    path('venue-book-json/<int:venue_id>/', views.book_distribution_json, name='venue_book'),
    path('show_book_json/<str:book_id>/', views.show_book_json, name="show_book_json")
]
