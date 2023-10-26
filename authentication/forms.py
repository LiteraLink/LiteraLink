from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    full_name = forms.CharField(max_length=200)
    email = forms.EmailField(max_length=200)

    role = forms.ChoiceField(
        label="Register as",
        required=True,
        choices=[
            ('A', 'Admin'),
            ('M', 'Member'),
        ],
    )

    class Meta:
        model = User
        fields = ['full_name', 'username', 'email', 'role','password1']

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=commit)
        user.role = self.cleaned_data.get("role")
        user.full_name = self.cleaned_data.get("full_name")
        user.email = self.cleaned_data.get("email")

        return user
