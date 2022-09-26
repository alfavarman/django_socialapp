from rest_framework.serializers import ModelSerializer
from base.models import Rooms, Topic


class RoomSerializer(ModelSerializer):
    class Meta:
        model = Rooms
        fields = ['id', 'host', 'topic', 'name', 'description']


class TopicSerializer(ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'name']
