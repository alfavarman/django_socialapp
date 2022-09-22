from django.shortcuts import render, redirect
from .models import Rooms
from .forms import RoomForm


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
    form = RoomForm
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def update_room(request, pk):
    room = Rooms.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')


    context = {'form': form}
    return render(request, 'base/room_form.html', context)
