from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'antar'

urlpatterns = [
    path('', views.show_list_books, name="show_list_books"),
    path('show-list-checkout/', views.show_list_checkout, name="show_list_checkout"),
    path('antar-buku-ajax', views.pesan_buku_ajax, name="pesan_buku_ajax"),
    path('delete_product_ajax/<int:id>', views.delete_product_ajax, name='delete_product_ajax'),
    path('add_stock/<int:id>/', views.add_stock, name='add_stock'),
    path('sub_stock/<int:id>/', views.sub_stock, name='sub_stock'),
    path('get-product/', views.get_product_json, name='get_product_json'),
    path('pemesanan-buku/<int:id>', views.pemesanan, name='pemesanan')
]