from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import EventSerializer

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
    
