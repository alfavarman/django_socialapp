from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db.models import Q
from .models import User, Rooms, Topic, Messages
from .forms import UserForm, UserRegistrationForm


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
    form = UserRegistrationForm()
    # when register send POST
    if request.method == 'POST':
        # form takes data from post
        form = UserRegistrationForm(request.POST)
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
    topics = Topic.objects.all()[0:5]
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
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Rooms.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )

        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.participants = request.user
        #     room.save()
        return redirect('home')

    context = {'topics': topics}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def update_room(request, pk):
    room = Rooms.objects.get(id=pk)
    topics = Topic.objects.all()
    if request.user != room.host:
        return messages.error(request, 'Only Room Host can edit the room')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'topics': topics, 'room': room}
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


@login_required(login_url='login')
def update_user(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.id)

    context = {'form': form}
    return render(request, 'base/update_user.html', context)


def topics_page(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})


def activity_page(request):
    room_messages = Messages.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})
