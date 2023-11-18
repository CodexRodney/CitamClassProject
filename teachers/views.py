from django.shortcuts import render
from Administrator.models import ClassRoom, Users
from Administrator.serializers import MessageSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from Administrator.serializers import ClassSerializer

# Create your views here.
class ClassesAPIView(APIView):
    """
    Used to handle class issues  by teachers
    """
    def post(self, request,*args, **kwargs):
        """
        Used to Return Classes Assigned to a Teacher
        """
        teacher = Users.objects.filter(email=request.data.get("email"))

        if not teacher or teacher[0].role != "teacher":
            data = {"message": "Teacher Doesn't Exist"}
            serializer = MessageSerializer(data)
            return Response(serializer.data, status=status.HTTP_403_FORBIDDEN)
        
        classes = ClassRoom.objects.filter(teacher=teacher)
        serializer = ClassSerializer(classes, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)