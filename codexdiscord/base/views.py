from django.shortcuts import render


rooms = [
    {'id': 1, 'name': 'Python shcool'},
    {'id': 2, 'name': 'DJANGO DISC'},
    {'id': 3, 'name': 'hacking'},
    {'id': 4, 'name': 'linux'},
    {'id': 5, 'name': 'recursive loop'},
]


def home(request):
    #as dictionary we pass variables. key is a name of variable, value is a reference to it
    context = {'rooms': rooms}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = None
    for i in rooms:
        if i['id'] == int(pk):
            room = i
    context = {'room': room}
    return render(request, 'base/room.html', context)



