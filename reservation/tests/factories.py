import factory
from django.contrib.auth import get_user_model
from examschedule.models import ExamSchedule
from reservation.models import Reservation
from datetime import timedelta, datetime

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'password')

class ScheduleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ExamSchedule

    exam_name = factory.Faker('word')
    exam_date = factory.LazyFunction(lambda: datetime.now().date() + timedelta(days=4))

class ReservationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Reservation

    user = factory.SubFactory(UserFactory)
    schedule = factory.SubFactory(ScheduleFactory)
    is_confirmed = False