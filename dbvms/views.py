from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import EventSerializer
from .models import Event
from datetime import datetime
from Administrator.serializers import MessageSerializer

# Create your views here.
class RegisterDBVMS(APIView):
    """
    Used to register children for dbvms
    """
    def post(self, request, *args, **kwargs):
        """
        Used to register children for dbvms
        """
        serializer = EventSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ConfirmParentPickUps(APIView):
    """
    Used to handle Pickups for kids
    """
    def post(self, request, *args, **kwargs):
        """
        Used by parent to confirm the kid is being picked up
        """
        parent_email = request.data.get("parent_email")

        atendee = Event.objects.filter(parent_email=parent_email)

        if not atendee:
            data = {"message": "Invalid Data"}
            serializer = MessageSerializer(data)
            return Response(serializer.data, status=status.HTTP_403_FORBIDDEN)
        
        atendee[0].prnt_cfrm_pickup = datetime.now()
        atendee[0].save()

        data = {"message": "SuccessFully Updated"}
        serializer = MessageSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):
        """
        Used by parent to confirm the kid is returned from the event
        """
        parent_email = request.data.get("parent_email")

        atendee = Event.objects.filter(parent_email=parent_email)

        if not atendee:
            data = {"message": "Invalid Data"}
            serializer = MessageSerializer(data)
            return Response(serializer.data, status=status.HTTP_403_FORBIDDEN)
        
        atendee[0].prnt_cfrm_dropped = datetime.now()
        atendee[0].save()

        data = {"message": "SuccessFully Updated"}
        serializer = MessageSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)