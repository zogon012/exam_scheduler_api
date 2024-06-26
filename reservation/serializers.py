from rest_framework import serializers
from reservation.models import Reservation

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'user', 'schedule', 'is_confirmed', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

    def create(self, validated_data):
        request = self.context.get('request', None)
        if request and request.user:
            validated_data['user'] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get('request', None)
        if request and request.user and not request.user.is_admin:
            validated_data.pop('is_confirmed', None)
        return super().update(instance, validated_data)