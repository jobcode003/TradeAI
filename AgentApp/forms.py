from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    date_of_birth = forms.DateField(required=True, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Date of Birth'}))

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'email', 'date_of_birth')

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
