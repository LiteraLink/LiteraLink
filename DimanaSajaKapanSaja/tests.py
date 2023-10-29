from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.test import TestCase, Client
from django.urls import reverse
from DimanaSajaKapanSaja.models import Station, StationBook
from DimanaSajaKapanSaja.views import create_station_book
from authentication.models import UserBook, UserProfile
from django.contrib.auth.models import User
from main.models import Book


class StationTestCase(TestCase):

    def setUp(self):
        # Setup test data
        self.user = User.objects.create_user(username='martin', password='123mmt123')
        self.profile = UserProfile.objects.create(user=self.user, role='M', full_name="Martin Tarigan", email="martinmtarigan7@gmail.com")
        self.station = Station.objects.create(name='Station1', address='Address1', opening_hours='9-5', rentable=5, returnable=5, map_location="images/MOI_5PDpC5Q.png")
        self.station1 = Station.objects.create(name='Station1', address='Address1', opening_hours='9-5', rentable=5, returnable=5, map_location="images/MOI_5PDpC5Q.png")
        self.station2 = Station.objects.create(name='Station2', address='Address1', opening_hours='9-5', rentable=5, returnable=5, map_location="images/MOI_5PDpC5Q.png")
        self.book = Book.objects.create(bookID='1', title='Top Secret', authors='Soledad Romero', display_authors='Soledad Romero', description="abc", categories="Fiction", thumbnail="http://books.google.com/books/content?id=CNkDAAAAMBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api")
        self.station_book = StationBook.objects.create(station=self.station, bookID='1', title='Top Secret', authors='Soledad Romero', display_authors='Soledad Romero', description="abc", categories="Fiction", thumbnail="http://books.google.com/books/content?id=CNkDAAAAMBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api")
        self.user_book = UserBook(user=self.profile, bookID='1', title='Top Secret', authors='Soledad Romero', display_authors='Soledad Romero', description="abc", categories="Fiction", thumbnail="http://books.google.com/books/content?id=CNkDAAAAMBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api", feature="DSKS")
        self.client = Client()

    def test_show_station(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('dimanasajakapansaja:show_station'))
        self.assertEqual(response.status_code, 200)

    def test_show_station_detail(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('dimanasajakapansaja:detail', args=[self.station.id]))
        self.assertEqual(response.status_code, 200)

    def test_add_station_ajax_not_admin(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('dimanasajakapansaja:add_station_ajax'), {})
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_get_station_json(self):
        response = self.client.get(reverse('dimanasajakapansaja:get_station_json'))
        self.assertEqual(response.status_code, 200)

    def test_del_station_not_admin(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('dimanasajakapansaja:del_station', args=[self.station.id]))
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_create_station_book(self):
        result = create_station_book(self.station, self.book)
        self.assertEqual(result.title, 'TestBook')
        self.assertEqual(result.authors, 'TestAuthor')

    def test_show_station(self):
        self.client.login(username='test', password='testpass')
        response = self.client.get(reverse('dimanasajakapansaja:show_station'))
        self.assertEqual(response.status_code, 200)

    def test_show_station_detail(self):
        self.client.login(username='test', password='testpass')
        response = self.client.get(reverse('dimanasajakapansaja:show_station_detail', args=[self.station.id]))
        self.assertEqual(response.status_code, 200)

    def test_add_station_ajax(self):
        self.client.login(username='test', password='testpass')
        response = self.client.post(reverse('dimanasajakapansaja:add_station_ajax'), {
            'name': 'new_station',
            'address': 'new_address'
        })
        self.assertEqual(response.status_code, 201)

    def test_get_station_json(self):
        self.client.login(username='test', password='testpass')
        response = self.client.get(reverse('dimanasajakapansaja:get_station_json'))
        self.assertEqual(response.status_code, 200)

    def test_add_station(self):
        self.client.login(username='test', password='testpass')
        response = self.client.post(reverse('dimanasajakapansaja:add_station'), {
            'name': 'new_station',
            'address': 'new_address'
        })
        self.assertEqual(response.status_code, 302)

    def test_show_detail_book(self):
        book = Book.objects.create(
            bookID='test_id',
            title='test_title',
            authors='test_authors',
            display_authors='test_display_authors',
            description='test_description',
            categories='test_categories',
            thumbnail='test_thumbnail'
        )
        
        response = self.client.get(reverse('dimanasajakapansaja:show_detail_books', args=[book.title]))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test_title')
        self.assertContains(response, 'test_authors')
        self.assertContains(response, 'test_display_authors')
        self.assertContains(response, 'test_description')
        self.assertContains(response, 'test_categories')
        self.assertContains(response, 'test_thumbnail')

    def test_add_station_by_admin(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(reverse('dimanasajakapansaja:add_station'), {
            'name': 'TestStation',
            'address': 'TestAddress',
            'opening_hours': '9-5',
            'rentable': 5,
            'returnable': 5,
            'map_location': 'images/MOI_5PDpC5Q.png'
        })
        self.assertEqual(response.status_code, HttpResponseRedirect.status_code)
        self.assertTrue(Station.objects.filter(name='TestStation').exists())

    def test_add_station_by_member(self):
        self.client.login(username='member', password='memberpass')
        response = self.client.post(reverse('dimanasajakapansaja:add_station'), {
            'name': 'TestStation',
            'address': 'TestAddress',
            'opening_hours': '9-5',
            'rentable': 5,
            'returnable': 5,
            'map_location': 'images/MOI_5PDpC5Q.png'
        })
        self.assertEqual(response.status_code, HttpResponseForbidden.status_code)
        self.assertFalse(Station.objects.filter(name='TestStation').exists())

    def test_add_station_invalid_form(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(reverse('dimanasajakapansaja:add_station'), {})
        self.assertNotEqual(response.status_code, HttpResponseRedirect.status_code)
        self.assertFalse(Station.objects.filter(name='TestStation').exists())

    def test_show_station(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('dimanasajakapansaja:show_station'))
        self.assertContains(response, 'Station1')
        self.assertContains(response, 'Station2')
    


