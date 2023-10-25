from django.forms import ModelForm
from DimanaSajaKapanSaja.models import Station

class StationForm(ModelForm):
    class Meta:
        model = Station
        fields = ["name", "address", "opening_hours", "rentable", "returnable", "map_location"]
