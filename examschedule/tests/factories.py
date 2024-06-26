import factory
from examschedule.models import ExamSchedule
from datetime import date

class ExamScheduleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ExamSchedule
        django_get_or_create = ('exam_name', 'exam_date')

    exam_name = factory.Faker('word')
    exam_date = factory.LazyFunction(lambda: date.today())