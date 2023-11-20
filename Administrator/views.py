from base64 import urlsafe_b64decode
from django.urls.resolvers import re
from rest_framework.views import APIView
from .serializers import UserSerializer, MessageSerializer, UserUpdateSerializer, ClassSerializer
from .serializers import PupilSerializer, DropOutsSerializer
# from .signals import send_verification_email
from .models import Users, ClassRoom, Pupil
# from .sendmails import send_password_reset_email, custom_message
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils import timezone
from django.views.generic.base import View
from django.shortcuts import render

# TODO implement api to get add extra roles to a user

# Create your views here.
class RegisterUsersApiView(APIView):
    """
    Handles User Operations such as:
        get: Getting all users
        post: Used for signing up users
        put: Used to update user information
        delete: Used to Delete a user from database(to be implemented)
    """

    def post(self, request, *args, **kwargs):
        """
        Creates teachers, drivers, admins and parents
        """
        data = {
            "first_name": request.data.get("first_name").title().strip(),
            "last_name": request.data.get("last_name").title().strip(),
            "email": request.data.get("email").strip(),
            "location": request.data.get("location").strip(),
            "idno": request.data.get("idno").strip(),
            "password": request.data.get("password"),
            "role": request.data.get("role").lower().strip(),
            "gender": request.data.get("gender").lower().strip()
        }
        serializer = UserSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        """
        Completes and updates user information
        """

        # check if password field exists
        password = request.data.get("password")
        data = {
            "first_name": request.data.get("first_name").title().strip(),
            "last_name": request.data.get("last_name").title().strip(),
            "email": request.data.get("email").strip(),
            "idno": request.data.get("idno").strip(),
            "password": request.data.get("password"),
            "role": request.data.get("role").lower().strip(),
        }
        if password:
            user_object = Users.objects.get(email=data["email"])
            serializer = UserSerializer(user_object, data=data)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            user_object = Users.objects.get(username=request.data.get("username"))

            serializer = UserUpdateSerializer(user_object, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginApiView(APIView):
    """
    Used to login the user to the account
    Return:
            - 404 if user doesn't exist in the system
            - 403 if password credentials is wrong
            - a user object with 200 success code if password is correct
    """

    def post(self, request, *args, **kwargs):
        # change to send the same message as wrong password
        user_object = Users.objects.filter(email=request.data.get("email"))

        if not user_object:
            data = {"message": "Invalid User Credentials"}
            serializer = MessageSerializer(data)
            return Response(serializer.data, status=status.HTTP_403_FORBIDDEN)
        
        serializer = UserSerializer(user_object[0])

        if user_object[0].check_password(request.data.get("password")):
            user_object[0].last_login = timezone.now()
            user_object[0].save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            data = {"message": "Invalid User Credentials"}
            serializer = MessageSerializer(data)
            return Response(serializer.data, status=status.HTTP_403_FORBIDDEN)

class CreateClassAPI(APIView):
    """
    Will hold operations for classes
    """
    def get(self, request, *args, **kwargs):
        """
        Used to return all classes registered
        """
        classrooms = ClassRoom.objects.all()
        serializer = ClassSerializer(classrooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        """
        Used To register a Class
        """
        if request.data.get("capacity") <= 0 or request.data.get("capacity") is None:
            data = {"message": "Invalid Data"}
            serializer = MessageSerializer(data)
            return Response(serializer.data, status=status.HTTP_403_FORBIDDEN)
        
        data = request.data
        teacher = Users.objects.filter(id=data.get("teacher"))
        if not teacher:
            data = {"message": "Teacher Not Registered"}
            serializer = MessageSerializer(data)
            return Response(serializer.data, status=status.HTTP_403_FORBIDDEN)

        # checking if user is a teacher
        if teacher[0].role != "teacher" or not ("teacher" in teacher[0].role):
            data = {"message": "Teacher Not Registered"}
            serializer = MessageSerializer(data)
            return Response(serializer.data, status=status.HTTP_403_FORBIDDEN)

        serializer = ClassSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        """
        Used to Update a Class's Info
        """
        classroom = ClassRoom.objects.filter(id=request.data.get("id"))
        data = request.data


        if not classroom:
            data = {"message": "ClassRoom Doesn't Exist"}
            serializer = MessageSerializer(data)
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        
        classroom[0].name = data["name"]
        classroom[0].grade = data["grade"]

        # get the teacher
        teacher = Users.objects.filter(id = data.get("teacher"))
        if not teacher:
            data = {"message": "Teacher Not Registered"}
            serializer = MessageSerializer(data)
            return Response(serializer.data, status=status.HTTP_403_FORBIDDEN)
        
        # checking if user is a teacher
        if teacher[0].role != "teacher" or not ("teacher" in teacher[0].role):
            data = {"message": "Teacher Not Registered"}
            serializer = MessageSerializer(data)
            return Response(serializer.data, status=status.HTTP_403_FORBIDDEN)
        
        classroom[0].teacher = teacher[0]
        classroom[0].capacity = data["capacity"]
        classroom[0].save()

        return Response(classroom[0].to_json(), status=status.HTTP_200_OK)

class PupilsAPI(APIView):
    """
    Will hold admin Operations on Student
    """
    def get(self, request, *args, **kwargs):
        """
        Used to return all classes registered
        """
        pupil = Pupil.objects.all()
        serializer = PupilSerializer(pupil, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        """
        Used to register a Kid to A Parent
        """
        data = request.data
        serializer = PupilSerializer(data=data)

        parent = Users.objects.filter(id=request.data.get("parent"))

        if not parent:
            data = {"message": "Parent Not Registered"}
            serializer = MessageSerializer(data)
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

        if parent[0].role != "parent" or not ("parent" in parent[0].other_role):
            data = {"message": "Parent Not Registered"}
            serializer = MessageSerializer(data)
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, *args, **kwargs):
        """
        Used to Update a Students Information
        """
        pupil = Pupil.objects.filter(birth_certificate_no=request.data.get("birth_certificate_no"))

        if not pupil:
            data = {"message": "Pupil Not Registered"}
            serializer = MessageSerializer(data)
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        
        parent = Users.objects.filter(email=request.data.get("parent_email"))

        if not parent:
            data = {"message": "Parent Not Registered"}
            serializer = MessageSerializer(data)
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        
        # checking if user is a parent
        if parent[0].role != "parent" or not ("parent" in parent[0].other_role):
            data = {"message": "Parent Not Registered"}
            serializer = MessageSerializer(data)
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

        classroom = ClassRoom.objects.filter(name=request.data.get("class_room"))

        if not classroom:
            data = {"message": "ClassRoom Doesn't Exist"}
            serializer = MessageSerializer(data)
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        
        pupil[0].first_name = request.data.get("first_name")
        pupil[0].last_name = request.data.get("last_name")
        pupil[0].birth_certificate_no = request.data.get("class_room")
        pupil[0].class_room = classroom[0]
        pupil[0].parent = parent[0]
        pupil[0].graduated = request.data.get("graduated")

        return Response(pupil[0].to_json(), status=status.HTTP_200_OK)

class DropOffLocations(APIView):
    """
    Used To Handle DropOffs
    """
    def post(self, request, *args, **kwargs):
        """
        Used to add dropoffs 
        """
        data = request.data

        serializer = DropOutsSerializer(data=data)
        if serializer.is_valid():
                serializer.save()
                return Response({"message": "Attendance Successfully Marked"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, *args, **kwargs):
        """
        Used to Update Dropouts 
        """
        pass


        


# # class ForgetPasswordAPI(APIView):
# #     """
# #     Used to handle logic for resetting user password
# #     when user forgot password
# #     """

# #     def post(self, request, *args, **kwargs):
# #         user = get_object_or_404(CustomUser, email=request.data.get("email"))

# #         if user:
# #             # generates the token for a user
# #             token = default_token_generator.make_token(user)

# #             # Get the current domain
# #             current_site = get_current_site(request)
# #             uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
# #             reset_url = f'http://{current_site.domain}{reverse("password_reset_confirm", kwargs={"uidb64": uidb64, "token": token})}'

# #             # sending the user the email
# #             send_password_reset_email(user.username, reset_url, user.email)

# #             data = {"message": "!!"}
# #             serializer = MessageSerializer(data)
# #             return Response(serializer.data, status=status.HTTP_200_OK)


# # class AuthenticateAPIView(APIView):
# #     """
# #     Should handle the list of users that are not authenticated
# #     """

# #     def get(self, request, *args, **kwargs):
# #         """
# #         Used to get users with an is_active = False
# #         """
# #         users = Administrator.objects.filter(is_active=False, email_verified=True)
# #         if users:
# #             serializer = AccountSerializer(users, many=True)
# #             return Response(serializer.data, status=status.HTTP_200_OK)
# #         else:
# #             serializer = AccountSerializer(users, many=True)
# #             return Response(serializer.data, status=status.HTTP_200_OK)

# #     def put(self, request, *args, **kwargs):
# #         """
# #         Should authenticate Users that are not authenticated
# #         """
# #         users = request.data.get("users")
# #         if users:
# #             for user in users:
# #                 user_object = Administrator.objects.get(username=user.get("username"))
# #                 user_object.is_active = not user_object.is_active
# #                 user_object.save()
# #             data = {"message": "Successfully Updated!!"}
# #             serializer = MessageSerializer(data)
# #             return Response(serializer.data, status=status.HTTP_200_OK)
# #         else:
# #             return Response(status=status.HTTP_403_FORBIDDEN)


# # class UserVerificationEmail(View):
# #     """
# #     Testing Verification That will be used to verify user emails
# #     """

# #     def get(self, request, *args, **kwargs):
# #         """
# #         Testing verify email
# #         """
# #         token = request.build_absolute_uri().split("/")[-3]
# #         token += "=="
# #         uid = urlsafe_b64decode(token)
# #         user = Administrator.objects.get(pk=uid)
# #         user.email_verified = True  # verifying user email
# #         user.save()

# #         message = {"message": "Email Successfully Verified"}
# #         serializer = MessageSerializer(message)
# #         return render(request, "registration/email_verified.html")
