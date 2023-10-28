from django.urls import path
from . import views

app_name = 'bacaditempat'

urlpatterns = [
    path('', views.show_list_venue, name="show_list_venue"),
    path('venue/<int:venue_id>/', views.show_detail_venue, name="show_detail_venue"),
    path('status/', views.show_list_status, name="show_list_status"),
    path('add_venue/', views.add_venue, name="add_venue"),
    path('edit_venue/<int:venue_id>/', views.edit_venue, name="edit_venue"),
    path('del_venue/<int:venue_id>/', views.del_venue, name="del_venue"),
    path('books/', views.list_books, name="list_books"),
    path('get-product/', views.get_product_json, name='get_product_json'),
    path('xml/', views.show_xml, name='show_xml'), 
    path('json/', views.show_json, name='show_json'), 
    path('xml/<int:id>/', views.show_xml_by_id, name='show_xml_by_id'), 
    path('json/<int:id>/', views.show_json_by_id, name='show_json_by_id'),
    path('pemesanan/<int:id>/', views.pemesanan, name="pemesanan"),
    path('add_book/<int:id>/', views.add_book, name="add_book"),
    path('sub_book/<int:id>/', views.sub_book, name="sub_book"),
    path('pesan_buku_ajax/<int:book_id>/', views.pesan_buku_ajax, name="pesan_buku_ajax"),
]
