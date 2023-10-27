from datetime import timedelta
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import redirect, render
from django.urls import reverse
from django.core import serializers
from Antar.models import Person, Books
from main.models import Book
from django.views.decorators.csrf import csrf_exempt

# menampilan list-list buku yang akan di pesan user
def show_list_books(request):
    # Mengambil semua objek buku dari model Book
    books = Book.objects.all()

    # Mengirimkan data buku ke template untuk ditampilkan
    return render(request, 'home.html', {'books': books})

def show_list_checkout(request):
    persons = Person.objects.all()
    return render(request, 'checkout.html', {'persons': persons})

def pemesanan(request,id):
    books = Book.objects.get(pk=id)
    return render(request,'pesan.html',{'books': books})


def get_product_json(request):
    books = Book.objects.all()
    return HttpResponse(serializers.serialize('json', books))

# membatalkan pesanan buku user
def delete_product_ajax(request, id):
    product = Book.objects.get(pk= id)
    product.delete()
    return HttpResponseRedirect(reverse('main:show_main'))

# menambahkan pesanan buku user
def add_stock(request, id = None):
    product = Book.objects.get(pk=id)
    product.jumlah_buku_dipesan += 1
    product.save()
    return HttpResponseRedirect(reverse('main:show_main'))

# mengurangi pesanan buku user  
def sub_stock(request, id = None):
    product = Book.objects.get(pk=id)
    if product.jumlah_buku_dipesan > 1:
        product.jumlah_buku_dipesan -= 1
        product.save()
    return HttpResponseRedirect(reverse('main:show_main'))

def show_xml(request):
    data = Book.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Book.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = Book.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Book.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@csrf_exempt
def pesan_buku_ajax(request, book_id):
    buku = Book.objects.get(id=book_id)
    if request.method == 'POST':
        nama_lengkap = request.POST.get("nama_lengkap")
        nomor_telepon = request.POST.get("nomor_telepon")
        alamat_pengiriman = request.POST.get("alamat_pengiriman")
        jumlah_buku_dipesan = request.POST.get("jumlah_buku_dipesan")
        durasi_peminjaman = request.POST.get("durasi_peminjaman")
        user = request.user

        # Hitung total_payment
        harga_per_unit = 5000  # Ganti dengan harga per unit yang sesuai
        ongkos_kirim = 12000
        total_payment = ongkos_kirim + (int(durasi_peminjaman) * harga_per_unit)

        new_product = Person(buku_dipesan=buku, nama_lengkap=nama_lengkap, alamat_pengiriman=alamat_pengiriman,total_payment=total_payment, 
                            nomor_telepon=nomor_telepon,jumlah_buku_dipesan=jumlah_buku_dipesan,durasi_peminjaman=durasi_peminjaman,
                            status_pesanan="Dalam Pengiriman", waktu_pengiriman = timedelta(hours=2), user=user)
        new_product.save()

        context = {
            'user': user,  # Jika Anda ingin menampilkan informasi pengguna
            'nama_lengkap': nama_lengkap,
            'nomor_telepon': nomor_telepon,
            'alamat_pengiriman': alamat_pengiriman,
            'nama_buku_dipesan': buku.title,
            'jumlah_buku_dipesan': jumlah_buku_dipesan,
            'status_pesanan': "Dalam Pengiriman",  # Jika Anda ingin menampilkan status pesanan
            'waktu_pengiriman' : "2 Jam"
        }

        # Kemudian, render tampilan HTML dengan konteks
        return render(request, 'checkout.html', context)


    return HttpResponseNotFound()