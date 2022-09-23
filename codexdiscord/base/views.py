from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Rooms, Topic
from .forms import RoomForm


def login_page(request):

    # retrieve login credential
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # check if user exists
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User not exists')

        # make sure credential are correct if not user = None
        user = authenticate(request, username=username, password=password)

        # login user if successfully authenticated
        if user is not None:
            login(request, user)
            return redirect('home')
        # if not authenticated
        else:
            messages.error(request, 'Wrong user or password, please try again')

    context = {}
    return render(request, 'base/login_register.html', context)


def logout_page(request):
    logout(request)
    return redirect('home')


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    #Q allowes for query using & |
    rooms = Rooms.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()

    context = {'rooms': rooms, 'topics': topics}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Rooms.objects.get(id=pk)
    context = {'room': room}
    return render(request, 'base/room.html', context)


@login_required(login_url='login')
def create_room(request):
    form = RoomForm
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
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


@login_required(login_url='login')
def delete_room(request, pk):
    room = Rooms.objects.get(id=pk)

    if request.user != room.host:   #better solution to now show button Edit to Guest(notlogin) and to nonhost
        return messages.error(request, 'Only host can edit room')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})
