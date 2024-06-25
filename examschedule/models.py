from django.db import models

class ExamSchedule(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"Exam from {self.start_time} to {self.end_time}"
