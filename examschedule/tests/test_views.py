import pytest
from django.urls import reverse
from rest_framework import status
from examschedule.models import ExamSchedule
from examschedule.tests.factories import ExamScheduleFactory
from reservation.tests.factories import ReservationFactory
from datetime import timedelta

@pytest.mark.django_db
def test_create_exam_schedule(authenticated_client):
    client, user = authenticated_client(is_admin=True)
    url = reverse('examschedule-list')
    data = {
        'exam_name': 'Test Exam',
        'exam_date': '2024-07-12',
    }
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert ExamSchedule.objects.count() == 1
    exam_schedule = ExamSchedule.objects.get(id=response.data['id'])
    assert exam_schedule.exam_name == 'Test Exam'
    assert exam_schedule.exam_date.isoformat() == '2024-07-12'

@pytest.mark.django_db
def test_update_exam_schedule(authenticated_client):
    client, user = authenticated_client(is_admin=True)
    exam_schedule = ExamScheduleFactory()
    url = reverse('examschedule-detail', args=[exam_schedule.id])
    current_exam_date = exam_schedule.exam_date
    new_exam_date = (current_exam_date + timedelta(days=1)).isoformat()
    data = {
        'exam_name': exam_schedule.exam_name,
        'exam_date': new_exam_date
    }
    response = client.patch(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    exam_schedule.refresh_from_db()
    assert exam_schedule.exam_name == data['exam_name']
    assert exam_schedule.exam_date.isoformat() == new_exam_date

@pytest.mark.django_db
def test_delete_exam_schedule_with_admin(authenticated_client):
    client, user = authenticated_client(is_admin=True)
    exam_schedule = ExamScheduleFactory()
    initial_count = ExamSchedule.objects.count()
    url = reverse('examschedule-detail', args=[exam_schedule.id])
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert ExamSchedule.objects.count() == initial_count - 1

@pytest.mark.django_db
def test_delete_exam_schedule_with_non_admin(authenticated_client, create_user):
    client, user = authenticated_client(is_admin=False)
    exam_schedule = ExamScheduleFactory()
    initial_count = ExamSchedule.objects.count()
    url = reverse('examschedule-detail', args=[exam_schedule.id])
    response = client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert ExamSchedule.objects.count() == initial_count

@pytest.mark.django_db
def test_exam_schedule_reservation_count(authenticated_client):
    client, user = authenticated_client()
    exam_schedule = ExamScheduleFactory()
    ReservationFactory.create_batch(5, schedule=exam_schedule)
    url = reverse('examschedule-detail', args=[exam_schedule.id])
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['reservation_count'] == 5