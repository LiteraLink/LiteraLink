from django.forms import ModelForm
from Bibliofilia.models import Forum

class BibliofiliaForm(ModelForm):
    class Meta:
        model = Forum
        fields = ["BookName", "forumsDescription", "bookPicture", "userReview"]
