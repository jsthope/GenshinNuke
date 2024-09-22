from django import forms
from .models import Profile, Room
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

def file_size(value):
    limit = 50 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 50 MiB.')

def file_extention(value):
    allow = ['png','pdf','jpeg','jpg']
    if value.name.split('.')[-1].lower() not in allow:
        raise ValidationError("File extension not allowed")

class CreateUserForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'input'}))
    password1 = forms.CharField(widget=forms.TextInput(attrs={'class': 'input','type':'password'}))
    password2 = forms.CharField(widget=forms.TextInput(attrs={'class': 'input','type':'password'}))

class RoomForm(forms.ModelForm):
    class Meta:              
        model = Room
        fields = '__all__'
        exclude = ['host','view']

class ProfileForm(forms.ModelForm):
    class Meta:              
        model = Profile
        fields = ['picture']
    picture = forms.FileField(validators=[file_size,file_extention])






