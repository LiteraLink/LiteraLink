from django.forms import ModelForm
from BacaDiTempat.models import Venue

class VenueForm(ModelForm):
    class Meta:
        model = Venue
        fields = ["place_name", "price", "address", "venue_open", "book_amount", "map_location"]