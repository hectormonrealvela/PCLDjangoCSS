from django import forms
from .models import Document

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django import forms



class DocumentForm(forms.ModelForm):

    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))


    class Meta:
        model = Document
        fields = '__all__'


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nombre de Usuario'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}))

class RegisterForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Usuario'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))


    class Meta:
        model = User
        fields = ['username', 'password','email']