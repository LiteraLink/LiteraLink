from django.forms import ModelForm
from Antar.models import Person
from django import forms

class ProductForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ["nama_lengkap", "nomor_telepon", "alamat_pengiriman", "jumlah_buku_dipesan","durasi_peminjaman"]
        labels = {
            'nama_lengkap' : '',
            'nomor_telepon': '',
            'alamat_pengiriman': '',
            'jumlah_buku_dipesan': '',
            'durasi_peminjaman': ''
        }
        widgets = {
            'nama_lengkap': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Lengkap'}),
            'nomor_telepon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nomor Telepon'}),
            'alamat_pengiriman': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Alamat Pengiriman'}),
            'jumlah_buku_dipesan': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Jumlah Buku'}),
            'durasi_peminjaman': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Durasi Peminjaman (Hari)'})
        }
