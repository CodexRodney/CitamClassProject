from base64 import urlsafe_b64decode
from django.urls.resolvers import re
from rest_framework.views import APIView
from .serializers import AdministratorSerializer, MessageSerializer
from .serializers import TeacherSerializer, ParentSerializer, DriverSerializer
# from .signals import send_verification_email
from .models import Administrator, Teacher, Driver, Parent
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


# Create your views here.
class RegisterAdminApiView(APIView):
    """
    Handles User Operations such as:
        get: Getting all users
        post: Used for signing up users
        put: Used to update user information
        delete: Used to Delete a user from database(to be implemented)
    """

    def post(self, request, *args, **kwargs):
        """
        Create a new Admin
        """
        data = {
            "first_name": request.data.get("first_name").title().strip(),
            "last_name": request.data.get("last_name").title().strip(),
            "email": request.data.get("email").strip(),
            "idno": request.data.get("idno").strip(),
            "password": request.data.get("password"),
            "role": request.data.get("role").lower().strip(),
        }
        if data["role"] == "admin":
            serializer = AdministratorSerializer(data=data)
        elif data["role"] == "teacher":
            serializer = TeacherSerializer(data=data)
        elif data["role"] == "parent":
            serializer = ParentSerializer(data=data)
        elif data["role"] == "driver":
            serializer = DriverSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()

            # signal to send verification to user
            # send_verification_email(serializer, request=request)

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
            if data["role"] == "admin":
                user_object = Administrator.objects.get(email=data["email"])
                serializer = AdministratorSerializer(user_object, data=data)
            elif data["role"] == "teacher":
                user_object = Teacher.objects.get(email=data["email"])
                serializer = TeacherSerializer(user_object, data=request.data)
            elif data["role"] == "parent":
                user_object = Driver.objects.get(email=data["email"])
                serializer = DriverSerializer(user_object, data=request.data)
            elif data["role"] == "driver":
                user_object = Parent.objects.get(email=data["email"])
                serializer = ParentSerializer(user_object, data=request.data)

            serializer =AdministratorSerializer(user_object, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            user_object = Administrator.objects.get(username=request.data.get("username"))

            serializer = AdministratorSerializer(user_object, data=request.data)
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
        role = request.data.get("role")
        try:
            if role == "admin":
                user_object = Administrator.objects.get(email=request.data.get("email"))
                serializer = AdministratorSerializer(user_object)
            elif role == "teacher":
                user_object = Teacher.objects.get(email=request.data.get("email"))
                serializer = TeacherSerializer(user_object)
            elif role == "driver":
                user_object = Driver.objects.get(email=request.data.get("email"))
                serializer = DriverSerializer(user_object)
            elif role == "parent":
                user_object = Parent.objects.get(email=request.data.get("email"))
                serializer = ParentSerializer(user_object)
        except Exception as e:
            data = {"message": "Invalid User Credentials"}
            serializer = MessageSerializer(data)
            return Response(serializer.data, status=status.HTTP_403_FORBIDDEN)

        if user_object.check_password(request.data.get("password")):
            user_object.last_login = timezone.now()
            user_object.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            data = {"message": "Invalid User Credentials"}
            serializer = MessageSerializer(data)
            return Response(serializer.data, status=status.HTTP_403_FORBIDDEN)


# class ForgetPasswordAPI(APIView):
#     """
#     Used to handle logic for resetting user password
#     when user forgot password
#     """

#     def post(self, request, *args, **kwargs):
#         user = get_object_or_404(CustomUser, email=request.data.get("email"))

#         if user:
#             # generates the token for a user
#             token = default_token_generator.make_token(user)

#             # Get the current domain
#             current_site = get_current_site(request)
#             uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
#             reset_url = f'http://{current_site.domain}{reverse("password_reset_confirm", kwargs={"uidb64": uidb64, "token": token})}'

#             # sending the user the email
#             send_password_reset_email(user.username, reset_url, user.email)

#             data = {"message": "!!"}
#             serializer = MessageSerializer(data)
#             return Response(serializer.data, status=status.HTTP_200_OK)


# class AuthenticateAPIView(APIView):
#     """
#     Should handle the list of users that are not authenticated
#     """

#     def get(self, request, *args, **kwargs):
#         """
#         Used to get users with an is_active = False
#         """
#         users = Administrator.objects.filter(is_active=False, email_verified=True)
#         if users:
#             serializer = AccountSerializer(users, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             serializer = AccountSerializer(users, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)

#     def put(self, request, *args, **kwargs):
#         """
#         Should authenticate Users that are not authenticated
#         """
#         users = request.data.get("users")
#         if users:
#             for user in users:
#                 user_object = Administrator.objects.get(username=user.get("username"))
#                 user_object.is_active = not user_object.is_active
#                 user_object.save()
#             data = {"message": "Successfully Updated!!"}
#             serializer = MessageSerializer(data)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(status=status.HTTP_403_FORBIDDEN)


# class UserVerificationEmail(View):
#     """
#     Testing Verification That will be used to verify user emails
#     """

#     def get(self, request, *args, **kwargs):
#         """
#         Testing verify email
#         """
#         token = request.build_absolute_uri().split("/")[-3]
#         token += "=="
#         uid = urlsafe_b64decode(token)
#         user = Administrator.objects.get(pk=uid)
#         user.email_verified = True  # verifying user email
#         user.save()

#         message = {"message": "Email Successfully Verified"}
#         serializer = MessageSerializer(message)
#         return render(request, "registration/email_verified.html")
