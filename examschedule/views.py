from rest_framework import viewsets
from .models import ExamSchedule
from .serializers import ExamScheduleSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated

class ExamScheduleViewSet(viewsets.ModelViewSet):
    queryset = ExamSchedule.objects.all()
    serializer_class = ExamScheduleSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()