from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Person(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nama_lengkap = models.CharField(max_length=255)
    nomor_telepon = models.CharField(max_length=255)
    alamat_pengiriman = models.TextField()
    nama_buku_dipesan = models.CharField(max_length=100)
    jumlah_buku_dipesan = models.IntegerField()
    durasi_peminjaman = models.IntegerField()
    total_payment = models.CharField(max_length=255)
    tanggal_pengiriman = models.DateField(auto_now_add=True)
    waktu_pengiriman= models.DurationField()
    status_pesanan = models.CharField(max_length=20)

class Books(models.Model):
    person = models.ForeignKey(Person, on_delete = models.CASCADE)
    bookID = models.CharField(max_length = 255)
    title = models.CharField(max_length = 255)
    authors = models.CharField(max_length = 255)
    display_authors = models.CharField(max_length = 255)
    description = models.TextField()
    categories = models.CharField(max_length = 255)
    thumbnail = models.TextField()