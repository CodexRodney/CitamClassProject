from django.shortcuts import render
from Administrator.models import ClassRoom, Users, Pupil
from Administrator.serializers import MessageSerializer, PupilSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from Administrator.serializers import ClassSerializer
from .serializers import AttendanceSerializer

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

        if not teacher or teacher[0].role != "teacher" and not ("teacher" in teacher[0].other_role):
            data = {"message": "Teacher Doesn't Exist"}
            serializer = MessageSerializer(data)
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        
        classes = ClassRoom.objects.filter(teacher=teacher[0])
        serializer = ClassSerializer(classes, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class ListStudentsAPIView(APIView):
     """
     Will be used to list students in a class
     """
     def post(self, request, *args, **kwargs):
          """
          Used to list all students in a class
          """
          classroom = ClassRoom.objects.filter(name=request.data.get("classname"))

          if not classroom:
            data = {"message": "Teacher Doesn't Exist"}
            serializer = MessageSerializer(data)
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
          
          # get a list of all students in the requested class
          pupils = Pupil.objects.filter(class_room=classroom[0])
          serializer = PupilSerializer(pupils, many=True)

          return Response(serializer.data, status=status.HTTP_200_OK)

class AttendanceAPIView(APIView):
    """
    Will be Used to Handle Attendance
    """
    def post(self, request, *args, **kwargs):
        """
        Used to mark Attendance of a Student
        """
        data = request.data
        # add other checks later
        serializer = AttendanceSerializer(data=data)
        if serializer.is_valid():
                serializer.save()
                return Response({"message": "Attendance Successfully Marked"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PromoteStudentAPIView(APIView):
    """
    Used to Promote Students by Teachers
    """
    def post(self, request, *args, **kwargs):
        """
        Used to Promote a student to the next class
        """
        pupil = Pupil.objects.filter(birth_certficate_no=request.data.get("birth_certificate_no"))
        classroom = ClassRoom.objects.filter(class_name=request.data.get("classname"))

        if not pupil:
            data = {"message": "Pupil Doesn't Exist"}
            serializer = MessageSerializer(data)
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        
        if not classroom:
            data = {"message": "Class Doesn't Exist"}
            serializer = MessageSerializer(data)
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        
        pupil[0].class_room = classroom[0]
        pupil[0].save()

        return Response({"message": "Student Promoted Successfully"}, status=status.HTTP_200_OK)