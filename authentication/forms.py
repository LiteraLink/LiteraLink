from typing import Any
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    full_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(max_length=200, widget=forms.EmailInput(attrs={'class':'form-control'}))

    role = forms.ChoiceField(
        label="Register as",
        required=True,
        choices=[
            ('A', 'Admin'),
            ('M', 'Member'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['full_name', 'username', 'email', 'role','password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=commit)
        user.role = self.cleaned_data.get("role")
        user.full_name = self.cleaned_data.get("full_name")
        user.email = self.cleaned_data.get("email")

        return user
