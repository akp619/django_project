from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerializer

@api_view(['GET'])
def get_routes(request):
    routes = [
                  'GET /api',
                  'GET /api/rooms',
                  'GET /api/rooms/:id'
              ]
    return Response(routes)


@api_view(['GET'])
def get_rooms(request):
    rooms = Room.objects.all()
    print(type(rooms), "==type==")
    roomsSerializer = RoomSerializer(rooms, many=True)
    print(roomsSerializer, "==roomsSerializer==")
    return Response(roomsSerializer.data)


@api_view(['GET'])
def get_room(request, pk):
    room = Room.objects.get(id=pk)
    roomsSerializer = RoomSerializer(room)
    print(roomsSerializer, "==roomsSerializer==")
    return Response(roomsSerializer.data)