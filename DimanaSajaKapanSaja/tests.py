from django.test import TestCase, Client
from django.urls import reverse
from DimanaSajaKapanSaja.models import Station, StationBook
from authentication.models import UserBook, UserProfile
from django.contrib.auth.models import User

class StationTestCase(TestCase):

    def setUp(self):
        # Setup test data
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.profile = UserProfile.objects.create(user=self.user, role='M')
        self.station = Station.objects.create(name='Station1', address='Address1', opening_hours='9-5', rentable=5, returnable=5, map_location="images/MOI_5PDpC5Q.png")
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

# ... dan seterusnya untuk fungsi lainnya
