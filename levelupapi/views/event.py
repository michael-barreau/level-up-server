"""View module for handling requests about events"""
from asyncio import events
from datetime import date, time
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Game, Gamer
from rest_framework import routers
from django.core.exceptions import ValidationError


class EventView(ViewSet):
    """Level up event view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single event

        Returns:
            Response -- JSON serialized event
        """
        try:
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event)
            return Response(serializer.data)
        except Event.DoesNotExist as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
        event = Event.objects.get(pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)
        

    def list(self, request):
        """Handle GET requests to get all events

        Returns:
            Response -- JSON serialized list of events
        """
        
        events =Event.objects.all()

        # Add in the next 3 lines
        event = request.query_params.get('type', None)
        if event is not None:
            events = events.filter(event_id=event)

        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
        
        # events = Event.objects.all()
        # serializer = EventSerializer(events, many=True)
        # return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """
        organizer = Gamer.objects.get(user=request.auth.user)
        serializer = CreateEventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(organizer=organizer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
         # """Handle POST operations

        # Returns
        #     Response -- JSON serialized game instance
        # """
        # game = Game.objects.get(pk=request.data["game"])
        # organizer = Gamer.objects.get(user=request.auth.user)

        # event = Event.objects.create(
        #     game=game,
        #     description=request.data["description"],
        #     date=request.data["date"],
        #     time=request.data["time"],
        #     organizer=organizer
        # )
        # serializer = EventSerializer(event)
        # return Response(serializer.data)
    
    def update(self, request, pk):
        """Handle PUT requests for an event

        Returns:
            Response -- Empty body with 204 status code
        """
        event = Event.objects.get(pk=pk)
        serializer = CreateEventSerializer(event, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        event.save()
        # event.description = request.data["description"]
        # event.date = request.data["date"]
        # event.time = request.data["time"]
        # event.organizer = Gamer.objects.get(user=request.auth.user)

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for events
    """
    class Meta:
        model = Event
        fields = ('id', 'game', 'description', 'date', 'time', 'organizer')
        depth = 2
        
class CreateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'game', 'description', 'date', 'time', 'organizer']
        