from django.shortcuts import render
from .models import Rooms


# rooms = [
#     {'id': 1, 'name': 'Python shcool'},
#     {'id': 2, 'name': 'DJANGO DISC'},
#     {'id': 3, 'name': 'hacking'},
#     {'id': 4, 'name': 'linux'},
#     {'id': 5, 'name': 'recursive loop'},
# ]


def home(request):
    rooms = Rooms.objects.all()
    #as dictionary we pass variables. key is a name of variable, value is a reference to it
    context = {'rooms': rooms}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Rooms.objects.get(id=pk)
    context = {'room': room}
    return render(request, 'base/room.html', context)


def create_room(request):
    context = {}
    return render(request, 'base/room_form.html', context)
