from .models import Administrator, Parent, Teacher, Driver
from rest_framework import serializers

class AdministratorSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Administrator

        fields = ['first_name', 'last_name', 'gender', 'dob',
                  'email', 'phone_no', 'idno', 'role']
        
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        """
        Creates a new user profile from the request's data
        """
        account = Administrator(**validated_data)
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

class ParentSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Parent
        fields = ['first_name', 'last_name', 'gender', 'dob',
                  'email', 'phone_no', 'location', 'idno', 'role']
        extra_kwargs = {
            "password": {"write_only": True}
        }
    def create(self, validated_data):
        """
        Creates a new user profile from the request's data
        """
        account = Parent(**validated_data)
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

class TeacherSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'gender', 'dob',
                  'email', 'phone_no', 'idno', 'role']
        extra_kwargs = {
            "password": {"write_only": True}
        }
    def create(self, validated_data):
        """
        Creates a new user profile from the request's data
        """
        account = Teacher(**validated_data)
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


class DriverSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Driver
        fields = ['first_name', 'last_name', 'gender', 'dob',
                  'email', 'phone_no', 'idno', 'role']
        extra_kwargs = {
            "password": {"write_only": True}
        }
    def create(self, validated_data):
        """
        Creates a new user profile from the request's data
        """
        account = Driver(**validated_data)
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

class AdministratorUpdateSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Administrator
        fields = ['first_name', 'last_name', 'gender', 'dob',
                  'email', 'phone_no', 'idno', 'role']
        extra_kwargs = {
            "password": {"write_only": True}
        }
