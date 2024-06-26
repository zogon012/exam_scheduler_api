from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Reservation
from .serializers import ReservationSerializer
from examschedule.models import ExamSchedule
from datetime import datetime
from django.db import transaction

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def get_queryset(self):
        if self.request.user.is_admin:
            return Reservation.objects.all()
        return Reservation.objects.filter(user=self.request.user)

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['confirm_reservations']:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        schedule_id = request.data.get('schedule')
        try:
            schedule = ExamSchedule.objects.get(id=schedule_id)
        except ExamSchedule.DoesNotExist:
            return Response({'detail': 'Schedule does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        if (schedule.exam_date - datetime.now().date()).days < 3:
            return Response({'detail': 'You cannot book a reservation less than 3 days before the exam date.'},
                            status=status.HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        data['is_confirmed'] = False
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_destroy(self, instance):
        if not self.request.user.is_admin and instance.is_confirmed:
            return Response({'detail': 'You cannot delete a confirmed reservation.'}, status=status.HTTP_403_FORBIDDEN)
        instance.delete()

    @action(detail=False, methods=['post'], url_path='confirm', permission_classes=[IsAdminUser])
    def confirm_reservations(self, request):
        schedules = Reservation.objects.values_list('schedule', flat=True).distinct()
        confirmed_count = 0
        with transaction.atomic():
            for schedule_id in schedules:
                reservations = Reservation.objects.filter(schedule_id=schedule_id, is_confirmed=False).order_by('created_at')[:50000]
                confirmed_reservations = Reservation.objects.filter(schedule_id=schedule_id, is_confirmed=True)
                confirmed_count_schedule = confirmed_reservations.count()
                if confirmed_count_schedule < 50000:
                    to_confirm = list(reservations[:50000 - confirmed_count_schedule])
                    for reservation in to_confirm:
                        reservation.is_confirmed = True
                    Reservation.objects.bulk_update(to_confirm, ['is_confirmed'])
                    confirmed_count += len(to_confirm)
        return Response({'detail': f'{confirmed_count} reservations confirmed successfully.'}, status=status.HTTP_200_OK)