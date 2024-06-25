# examschedule/tests/factories.py

import factory
from examschedule.models import ExamSchedule
from datetime import timedelta

class ExamScheduleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ExamSchedule
        django_get_or_create = ('start_time', 'end_time')

    start_time = factory.Faker('date_time_this_month', before_now=False, after_now=True)
    end_time = factory.LazyAttribute(lambda obj: obj.start_time + timedelta(hours=2))