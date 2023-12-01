from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'antar'

urlpatterns = [
    path('', views.show_list_books, name="show_list_books"),
    path('antar-buku-ajax/<int:id_buku>', views.pesan_buku_ajax, name="pesan_buku_ajax"),
    path('delete-product-ajax/<int:id>', views.delete_product_ajax, name='delete_product_ajax'),
    path('add_stock/<int:id>/', views.add_stock, name='add_stock'),
    path('sub_stock/<int:id>/', views.sub_stock, name='sub_stock'),
    path('get-product/', views.get_product_json, name='get_product_json'),
    path('pemesanan-buku/<int:id>', views.pemesanan, name='pemesanan'),
    path('show-list-checkout-all/', views.show_list_checkout_all, name='show_list_checkout_all'),
    path('get-person/', views.get_person_json, name='get_person_json'),
    path('fiter-pemesanan-buku/', views.show_list_checkout_filter, name='show_list_checkout_filter'),
    path('filter-buku/', views.show_list_books_filter, name='show_list_books_filter'),
    path('show-detail/<int:id>', views.show_detail, name='show_detail'),
    path('update-order-status/<int:id>', views.update_order_status, name='update_order_status')
]