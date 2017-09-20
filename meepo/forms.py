from django import forms
from .models import Pet, User
from django.contrib.auth.forms import UserCreationForm

class PetForm(forms.ModelForm):

    class Meta:
        model = Pet
        fields = ('name',)


class SignUpForm(UserCreationForm):
    phone_number = forms.CharField(max_length=10)
    email = forms.EmailField(max_length=254, required=True)

    class Meta:
        model = User
        fields = ('username', 'phone_number', 'email', 'password1', 'password2', )