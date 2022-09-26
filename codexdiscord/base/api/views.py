from django.http import JsonResponse
from base.api.serializers import RoomSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Rooms


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id',
        'GET /api/topics:name',
    ]
    return JsonResponse(routes, safe=False)


@api_view(['GET'])
def getRooms(request):
    rooms = Rooms.objects.all()
    serialized_room = RoomSerializer(rooms, many=True)
    return Response(serialized_room.data)


@api_view(['GET'])
def getRoom(request, pk):
    room = Rooms.objects.get(id=pk)
    serialized_room = RoomSerializer(room)
    return Response(serialized_room.data)
