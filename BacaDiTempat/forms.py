from django.forms import ModelForm
from BacaDiTempat.models import Venue

class VenueForm(ModelForm):
    class Meta:
        model = Venue
        fields = ["place_name", "price", "address", "venue_open", "rent_book", "return_book", "map_location"]

class UserForm(ModelForm):
    class Meta:
        model = Venue
        fields = ["person_name", "phone_number", "date_use", "date_return"]
