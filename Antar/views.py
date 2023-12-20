from datetime import timedelta
from datetime import datetime
import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.core import serializers
from Antar.models import Person, Books
from main.models import Book
from authentication.models import UserBook, UserProfile
from Antar.forms import ProductForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User

"""
function untuk kebutuhan flutter App
"""

@csrf_exempt
# meng-update status pesanan buku user
def update_order_status(request):
    if request.method == 'POST':
        try:
            # asumsikan body request mengandung 'new_status'
            data = json.loads(request.body)
            print(data)
            new_status = data['new_status']
            
            # temukan order dengan ID yang diberikan dan perbarui statusnya
            person = Person.objects.get(id=data['delivery_id'])
            person.status_pesanan = new_status  # asumsikan model Order memiliki field 'status'
            person.save()
            
            # kembalikan response sukses
            return JsonResponse({"status": "success"}, status=200)
        except Person.DoesNotExist:
            return JsonResponse({"status": "order_not_found"}, status=404)
        except Exception as e:
            # tangkap exception lainnya dan kembalikan sebagai error
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    else:
        # handle non-POST requests here if needed
        return JsonResponse({"status": "invalid_request"}, status=400)


@csrf_exempt
# membatalkan pesanan buku user
def delete_product_flutter(request, id=None):
    persons = Person.objects.get(pk=id)
    persons.delete()
    return JsonResponse({"status": "success"}, status=200)

@csrf_exempt
# menambahkan pesanan buku user
def add_stock_flutter(request, id=None):
    persons = Person.objects.get(pk=id)
    persons.jumlah_buku_dipesan += 1
    persons.save()
    return JsonResponse({"status": "success"}, status=200)

@csrf_exempt
# mengurangi pesanan buku user  
def sub_stock_flutter(request, id=None):
    persons = Person.objects.get(pk=id)
    if persons.jumlah_buku_dipesan > 1:
        persons.jumlah_buku_dipesan -= 1
        persons.save()
        return JsonResponse({"status": "success"}, status=200)
    else : 
        return JsonResponse({"status": "error"}, status=401)

@csrf_exempt
def show_list_checkout_flutter(request,username):
    user = User.objects.get(username=username)
    userprofile = UserProfile.objects.get(user=user)
    role = userprofile.role
    if role == "A":
        data = Person.objects.all()
    else:
        # asumsikan Anda telah mendapatkan received_username dari request
        # received_username = request.GET.get('username')  # Contoh untuk metode GET
        # Atau untuk POST: received_username = request.POST.get('username')

        try:
            userApp = user
            data = Person.objects.filter(user=userApp)
        except userprofile.DoesNotExist:
            # Handle the case where the User does not exist
            data = []

    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@csrf_exempt
def pesan_buku_flutter(request, idBuku, username):
    print("function pesan buku untuk flutter ke panggil")
    buku=Book.objects.get(pk=idBuku)

    # Hitung total_payment
    harga_per_unit = 5000  # Ganti dengan harga per unit yang sesuai
    ongkos_kirim = 12000
    
    if request.method == 'POST':
        
        data = json.loads(request.body)

        new_person = Person.objects.create(
            user = User.objects.get(username=username),
            nama_lengkap = data["nama_lengkap"],
            nomor_telepon = data["nomor_telepon"],
            alamat_pengiriman = data["alamat_pengiriman"],
            nama_buku_dipesan = buku.title,
            jumlah_buku_dipesan = int(data["jumlah_buku_dipesan"]),
            durasi_peminjaman = int(data["durasi_peminjaman"]),
            total_payment = ongkos_kirim + ( int(data["durasi_peminjaman"]) * harga_per_unit),
            tanggal_pengiriman = datetime.now(),
            waktu_pengiriman= timedelta(hours=2),
            status_pesanan = "Dalam Pengiriman",
        )
        
        new_book = UserBook.objects.create(
            user=UserProfile.objects.get(user=User.objects.get(username=username)), 
            bookID=buku.bookID, 
            title=buku.title, 
            authors=buku.authors, 
            display_authors=buku.display_authors,
            description=buku.description,
            categories=buku.categories,
            thumbnail=buku.thumbnail, 
            feature="A",
        )

        new_book.save()
        new_person.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)


"""
function untuk kebutuhan Django App
"""
# menampilan list-list buku yang akan di pesan user
@login_required(login_url='auth:signin')
def show_list_books(request):
    # Mengambil semua objek buku dari model Book
    books = Book.objects.all()
    userprofile = UserProfile.objects.get(user=request.user)
    role = userprofile.role

    request.session['role_user'] = role
    context={
        'books': books,
        'role': role
    }

    # Mengirimkan data buku ke template untuk ditampilkan
    return render(request, 'home.html', context)

def show_list_books_filter(request):
    # Mengambil semua objek buku dari model Book
    queryBook = request.GET.get('queryBook')
    userprofile = UserProfile.objects.get(user=request.user)
    role = userprofile.role

    # Simpan nilai query dalam sesi
    request.session['book_query'] = queryBook

    books = Book.objects.filter(title=queryBook)
    # Mengirimkan data buku ke template untuk ditampilkan
    return render(request, 'home.html', {'books': books, 'role': role})

def show_list_checkout_all(request):
    userprofile = UserProfile.objects.get(user=request.user)
    role = userprofile.role
    persons = Person.objects.all()
    if persons:
        return render(request, 'checkout.html', {'persons': persons, 'role': role})
    else:
        empty_message = "Belum ada pesanan yang harus di antar."
        return render(request, 'checkout.html', {'empty_message': empty_message, 'role': role})
    
    
def show_list_checkout_filter(request):
    userprofile = UserProfile.objects.get(user=request.user)
    print(userprofile)
    role = userprofile.role
    print(role)
    query = request.GET.get('query')  # Mengambil nilai dari input form

    # Simpan nilai query dalam sesi
    request.session['filter_query'] = query

    persons = Person.objects.filter(nama_buku_dipesan=query)
    if persons:
        return render(request, 'checkout.html', {'persons': persons, 'role': role})
    else:
        empty_message = "Belum ada pesanan yang harus di antar."
        return render(request, 'checkout.html', {'empty_message': empty_message, 'role': role})

# def update_order_status(request, id=None):
#     print("berhasil ke update order status")
#     userprofile = UserProfile.objects.get(user=request.user)
#     role = userprofile.role
#     if role != 'A':
#         return HttpResponseForbidden("Anda tidak memiliki izin untuk melakukan tindakan ini.")
    
#     persons = Person.objects.get(pk=id)
#     print(request.method)
#     if request.method == 'POST':
#         # Periksa apakah status pesanan telah diubah dan lakukan validasi jika diperlukan.
#         status_pesanan = request.POST.get("status_pesanan")
#         persons.status_pesanan = status_pesanan
#         persons.save()
#         print(persons.status_pesanan)
#         return show_detail(request, id)  # Redirect ke halaman konfirmasi atau lainnya
    
#     return show_detail(request, id)
    
def pemesanan(request,id):
    books = Book.objects.get(pk=id)
    form = ProductForm
    context = {
        'id_buku': id,
        'form': form
    }
    return render(request,'pesan.html',context)


def get_product_json(request):
    queryBook = request.session.get('book_query')
    if queryBook:
        books = Book.objects.all().filter(title=queryBook)
    else :
        books = Book.objects.all()
    return HttpResponse(serializers.serialize('json', books))

def get_person_json(request):
    print("tes")
    userprofile = UserProfile.objects.get(user=request.user)
    role = userprofile.role

    query = request.session.get('filter_query')

    if role == "M":
        if query:
            persons = Person.objects.filter(user=request.user).filter(nama_buku_dipesan=query)
        else :
            persons = Person.objects.filter(user=request.user)
    else :
        if query:
            persons = Person.objects.all().filter(nama_buku_dipesan=query)
        else :
            persons = Person.objects.all()

    return HttpResponse(serializers.serialize('json', persons))

def show_detail(request, id=None):
    persons = Person.objects.get(pk=id)
    userprofile = UserProfile.objects.get(user=request.user)
    role = userprofile.role

    context= {
        'nama_lengkap' : persons.nama_lengkap,
        'nomor_telepon' : persons.nomor_telepon,
        'alamat_pengiriman' : persons.alamat_pengiriman,
        'nama_buku_dipesan' : persons.nama_buku_dipesan,
        'jumlah_buku_dipesan' : persons.jumlah_buku_dipesan,
        'durasi_peminjaman' : persons.durasi_peminjaman,
        'total_payment' : persons.total_payment,
        'tanggal_pengiriman' : persons.tanggal_pengiriman,
        'waktu_pengiriman' : persons.waktu_pengiriman,
        'status_pesanan' : persons.status_pesanan,
        'id' : persons.pk,
        'role' : role
    }
    return render(request,'detail.html',context)


# membatalkan pesanan buku user
def delete_product(request, id=None):
    persons = Person.objects.get(pk=id)
    persons.delete()
    return HttpResponseRedirect(reverse('antar:show_list_checkout_all'))

# menambahkan pesanan buku user
def add_stock(request, id=None):
    persons = Person.objects.get(pk=id)
    persons.jumlah_buku_dipesan += 1
    persons.save()
    return HttpResponseRedirect(reverse('antar:show_list_checkout_all'))

# mengurangi pesanan buku user  
def sub_stock(request, id=None):
    persons = Person.objects.get(pk=id)
    if persons.jumlah_buku_dipesan > 1:
        persons.jumlah_buku_dipesan -= 1
        persons.save()
    return HttpResponseRedirect(reverse('antar:show_list_checkout_all'))

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
def pesan_buku_ajax(request, id_buku):
    buku=Book.objects.get(pk=id_buku)
    # person = Person.objects.get(user=request.user)

    if request.method == 'POST':
        nama_lengkap = request.POST.get("nama_lengkap")
        nomor_telepon = request.POST.get("nomor_telepon")
        alamat_pengiriman = request.POST.get("alamat_pengiriman")
        jumlah_buku_dipesan = request.POST.get("jumlah_buku_dipesan")
        durasi_peminjaman = request.POST.get("durasi_peminjaman")
        user=request.user
        # Hitung total_payment
        harga_per_unit = 5000  # Ganti dengan harga per unit yang sesuai
        ongkos_kirim = 12000
        total_payment = ongkos_kirim + (int(durasi_peminjaman) * harga_per_unit)

        new_person = Person(user=user, nama_buku_dipesan=buku.title, nama_lengkap=nama_lengkap, alamat_pengiriman=alamat_pengiriman,total_payment=str(total_payment), 
                            nomor_telepon=nomor_telepon,jumlah_buku_dipesan=jumlah_buku_dipesan,durasi_peminjaman=durasi_peminjaman,
                            status_pesanan="Dalam Pengiriman", waktu_pengiriman = timedelta(hours=2))
        new_books = Books(person=new_person, bookID=buku.bookID, title=buku.title, authors=buku.authors, display_authors=buku.display_authors,
                          description=buku.description, categories=buku.categories, thumbnail=buku.thumbnail)
        new_person.save()
        new_books.save()
        # return HttpResponseRedirect(reverse('antar:show_list_checkout_all'))
        return redirect('antar:show_list_checkout_all')


    return HttpResponseNotFound()
