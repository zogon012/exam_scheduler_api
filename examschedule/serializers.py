from rest_framework import serializers
from .models import ExamSchedule
from reservation.models import Reservation

class ExamScheduleSerializer(serializers.ModelSerializer):
    reservation_count = serializers.SerializerMethodField()

    class Meta:
        model = ExamSchedule
        fields = ['id', 'exam_name', 'exam_date', 'reservation_count']

    def get_reservation_count(self, obj):
        return Reservation.objects.filter(schedule=obj).count()