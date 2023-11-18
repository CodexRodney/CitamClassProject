from .models import Users, ClassRoom, Pupil
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Users
        fields = ['id', 'first_name', 'last_name', 'gender', 'dob', 'password',
                  'email', 'phone_no', 'location', 'idno', 'role']
        
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        """
        Creates a new user profile from the request's data
        """
        account = Users(**validated_data)
        account.set_password(account.password)
        account.save()

        # user_profile = UserProfileModel.objects.create(account=account, **validated_data)
        return account
    
    def update(self, instance, validated_data):
        """
        Updates a user's profile from the request's data
        """
        instance.set_password(instance.password)
        validated_data["password"] = instance.password
        return super().update(instance, validated_data)
    
class MessageSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=100)

class UserUpdateSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Users
        fields = ['id', 'first_name', 'last_name', 'gender', 'dob',
                  'email', 'phone_no', 'location', 'idno', 'role']
        extra_kwargs = {
            "password": {"write_only": True}
        }

class ClassSerializer(serializers.ModelSerializer):
    # implement for it to return teachers name
    class Meta:
        model = ClassRoom
        fields = ['id', 'name', 'grade', 'capacity', 'teacher']
    
    def create(self, validated_data):
        """
        Creates a new class from the request's data
        """
        classroom = ClassRoom(**validated_data)
        classroom.save()

        return classroom
    
class PupilSerializer(serializers.ModelSerializer):
    # implement for it to return teachers name
    class Meta:
        model = Pupil
        fields = ['id', 'first_name', 'last_name', 'birth_certificate_no', 'class_room', 'parent', 'graduated']
    
    def create(self, validated_data):
        """
        Creates a new class from the request's data
        """
        pupil = Pupil(**validated_data)
        pupil.save()

        return pupil