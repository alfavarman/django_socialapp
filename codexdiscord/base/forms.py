from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Rooms

#
# class RoomForm(ModelForm):
#     class Meta:
#         model = Rooms
#         fields = ['name', 'topic', 'description', 'host', 'participants',] # '__all__' security
#         exclude = ['host', 'participants']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']
