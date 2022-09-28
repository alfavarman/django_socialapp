from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

#
# class RoomForm(ModelForm):
#     class Meta:
#         model = Rooms
#         fields = ['name', 'topic', 'description', 'host', 'participants',] # '__all__' security
#         exclude = ['host', 'participants']


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Your best email? No spam!')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'name', 'email')
