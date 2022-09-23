from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Rooms, Topic, Messages
from .forms import RoomForm


def login_page(request):
    page = 'login'
    # if user is login already redirext to home
    if request.user.is_authenticated:
        return redirect('home')

    # retrieve login credential
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        # check if user exists
        try:
            User.objects.get(username=username)
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

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logout_page(request):
    logout(request)
    return redirect('home')


def register_page(request):
    form = UserCreationForm()
    # when register send POST
    if request.method == 'POST':
        # form takes data from post
        form = UserCreationForm(request.POST)
        # validation check
        if form.is_valid():
            # save without commit to lowercase input
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            # login in user
            login(request, user)
            # redirect logged user to home
            return redirect('home')
        # this section is not required as django handles registration errors!
        # else:
        #     # if error:
        #     messages.error(request, "Try register again")



    return render(request, 'base/login_register.html', {'form': form})


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    # Q allows for query using & and |
    rooms = Rooms.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()
    room_count = rooms.count()
    room_messages = Messages.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms': rooms, 'room_count': room_count, 'topics': topics, 'room_messages': room_messages}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Rooms.objects.get(id=pk)
    room_messages = room.messages_set.all().order_by('-created')
    participants = room.participants.all()

    context = {'room': room, 'room_messages': room_messages, 'participants': participants}

    if request.method == 'POST':
        message = Messages.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body'),
        )

        # participiant list should be returned by operson active in room.
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    return render(request, 'base/room.html', context)


@login_required(login_url='login')
def profile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.rooms_set.all()
    room_messages = user.messages_set.all()
    topics = Topic.objects.all()

    context = {'user': user, "rooms": rooms, "room_messages": room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)


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

    if request.user != room.host:
        return messages.error(request, 'Only host can edit room')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})


@login_required(login_url='login')
def delete_message(request, pk):
    comment = Messages.objects.get(id=pk)

    if request.user != comment.user:
        return messages.error(request, 'Only author can edit room')

    if request.method == 'POST':
        comment.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': comment})
