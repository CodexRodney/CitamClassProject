from rest_framework import serializers
from .models import Attendance

class AttendanceSerializer(serializers.ModelSerializer):
    # implement for it to return teachers name
    class Meta:
        model = Attendance
        fields = ['id', 'pupil', 'classroom', 'day', 'teacher', 'is_present']
    
    def create(self, validated_data):
        """
        Creates a new class from the request's data
        """
        attendance = Attendance(**validated_data)
        attendance.save()

        return attendance