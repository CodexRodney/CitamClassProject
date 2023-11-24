from .models import Event
from rest_framework import serializers

class EventSerializer(serializers.ModelSerializer):
    # implement for it to return teachers name
    class Meta:
        model = Event
        fields = ['parent_email', 'parent_name', 'parent_phone_number', 'pupil',
                  'need_tranport', 'parent_location', 'prnt_cfrm_pickup', 'tchr_cfrm_received',
                  'tchr_cfrm_released', 'prnt_cfrm_dropped', 'dbvms_year', 'teacher_id', 'grade']
    
    def create(self, validated_data):
        """
        Creates a new class from the request's data
        """
        atendee = Event(**validated_data)
        atendee.save()

        return atendee