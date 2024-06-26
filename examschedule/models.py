from django.db import models

class ExamSchedule(models.Model):
    exam_name = models.CharField(max_length=255)
    exam_date = models.DateField()

    class Meta:
        unique_together = ('exam_name', 'exam_date')

    def __str__(self):
        return f"{self.exam_name} on {self.exam_date}"