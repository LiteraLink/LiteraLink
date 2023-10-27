from django.forms import ModelForm
from Antar.models import Person

class ProductForm(ModelForm):
    class Meta:
        model = Person
        fields = ["nama_lengkap", "nomor_telepon", "alamat_pengiriman", "jumlah_buku_dipesan","durasi_peminjaman"]