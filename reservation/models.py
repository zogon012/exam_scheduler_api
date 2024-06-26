from django.conf import settings
from django.db import models
from examschedule.models import ExamSchedule

class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    schedule = models.ForeignKey(ExamSchedule, on_delete=models.CASCADE)
    is_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'schedule')

    def __str__(self):
        return f"Reservation by {self.user} for {self.schedule}"

    def get_position(self):
        reservations = Reservation.objects.filter(schedule=self.schedule).order_by('created_at')
        for index, reservation in enumerate(reservations, start=1):
            if reservation.id == self.id:
                return index
        return None