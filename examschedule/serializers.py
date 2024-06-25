from rest_framework import serializers
from .models import ExamSchedule

class ExamScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamSchedule
        fields = ['id', 'start_time', 'end_time']