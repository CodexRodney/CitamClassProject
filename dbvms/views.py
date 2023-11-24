from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import EventSerializer
from .models import Event
from datetime import datetime
from Administrator.serializers import MessageSerializer
from Administrator.models import Users

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
    
class ConfirmTeacherPickup(APIView):
    """
    Used to handle Pickups for kids by Teacher
    """
    def post(self, request, *args, **kwargs):
        """
        Used by teacher to confirm the kid has arrived to the event
        """
        parent_email = request.data.get("parent_email")

        atendee = Event.objects.filter(parent_email=parent_email)

        teacher_id = request.data.get("teacher_id")
        teacher = Users.objects.filter(id=teacher_id)


        if not atendee or not teacher:
            data = {"message": "Invalid Data"}
            serializer = MessageSerializer(data)
            return Response(serializer.data, status=status.HTTP_403_FORBIDDEN)
        
        if atendee[0].teacher_id != teacher.id:
            data = {"message": "Invalid Data"}
            serializer = MessageSerializer(data)
            return Response(serializer.data, status=status.HTTP_403_FORBIDDEN)
                
        atendee[0].tchr_cfrm_received = datetime.now()
        atendee[0].save()

        data = {"message": "SuccessFully Updated"}
        serializer = MessageSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):
        """
        Used by teacher to confirm the kid is returned from the event
        """
        parent_email = request.data.get("parent_email")

        atendee = Event.objects.filter(parent_email=parent_email)

        teacher_id = request.data.get("teacher_id")
        teacher = Users.objects.filter(id=teacher_id)


        if not atendee or not teacher:
            data = {"message": "Invalid Data"}
            serializer = MessageSerializer(data)
            return Response(serializer.data, status=status.HTTP_403_FORBIDDEN)
        
        if atendee[0].teacher_id != teacher.id:
            data = {"message": "Invalid Data"}
            serializer = MessageSerializer(data)
            return Response(serializer.data, status=status.HTTP_403_FORBIDDEN)
                
        atendee[0].tchr_cfrm_released = datetime.now()
        atendee[0].save()

        data = {"message": "SuccessFully Updated"}
        serializer = MessageSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)