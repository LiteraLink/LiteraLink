from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Person, Books
from main.models import Book
from authentication.models import UserProfile

class YourAppTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.userprofile = UserProfile.objects.create(user=self.user, role='A')  # Ganti 'A' dengan peran yang sesuai
        self.book = Book.objects.create(title='Book Title', authors='Author Name', description='Book Description')
        self.person = Person.objects.create(user=self.user, nama_buku_dipesan='Book Title', jumlah_buku_dipesan=1)

    def test_show_list_books(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('antar:show_list_books'))  # Ganti 'show_list_books' dengan nama URL yang sesuai
        self.assertEqual(response.status_code, 200)  # Pastikan respons memiliki status kode 200

    def test_show_list_books_filter(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('antar:show_list_books_filter'), {'queryBook': 'Book Title'})  # Ganti 'show_list_books_filter' dengan nama URL yang sesuai
        self.assertEqual(response.status_code, 200)  # Pastikan respons memiliki status kode 200

    def test_show_list_checkout_all(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('antar:show_list_checkout_all'))  # Ganti 'show_list_checkout_all' dengan nama URL yang sesuai
        self.assertEqual(response.status_code, 200)  # Pastikan respons memiliki status kode 200

    def test_show_list_checkout_filter(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('antar:show_list_checkout_filter'), {'query': 'Book Title'})  # Ganti 'show_list_checkout_filter' dengan nama URL yang sesuai
        self.assertEqual(response.status_code, 200)  # Pastikan respons memiliki status kode 200

    def test_update_order_status(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('antar:update_order_status', args=[self.person.pk]), {'status_pesanan': 'Dikirim'})  # Ganti 'update_order_status' dengan nama URL yang sesuai
        self.assertEqual(response.status_code, 200)  # Pastikan respons memiliki status kode 200
        updated_person = Person.objects.get(pk=self.person.pk)
        self.assertEqual(updated_person.status_pesanan, 'Dikirim')  # Pastikan status pesanan diperbarui sesuai dengan yang diharapkan

    # Tambahkan lebih banyak tes sesuai kebutuhan
