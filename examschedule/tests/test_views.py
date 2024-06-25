# examschedule/tests/test_views.py

import pytest
from django.urls import reverse
from rest_framework import status
from examschedule.models import ExamSchedule
from examschedule.tests.factories import ExamScheduleFactory
from datetime import timedelta

@pytest.mark.django_db
def test_create_exam_schedule(authenticated_client):
    client, user = authenticated_client(is_admin=True)
    url = reverse('examschedule-list')
    data = {
        'start_time': '2024-06-25T10:00:00Z',
        'end_time': '2024-06-25T12:00:00Z',
    }
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert ExamSchedule.objects.count() == 1
    exam_schedule = ExamSchedule.objects.get(id=response.data['id'])
    assert exam_schedule.start_time.isoformat() == '2024-06-25T10:00:00+00:00'
    assert exam_schedule.end_time.isoformat() == '2024-06-25T12:00:00+00:00'

@pytest.mark.django_db
def test_update_exam_schedule(authenticated_client):
    client, user = authenticated_client(is_admin=True)
    exam_schedule = ExamScheduleFactory()
    url = reverse('examschedule-detail', args=[exam_schedule.id])
    new_end_time = exam_schedule.end_time + timedelta(hours=1)
    data = {'end_time': new_end_time.isoformat()}
    response = client.patch(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    exam_schedule.refresh_from_db()
    # 타임존 정보 제거 후 비교
    assert exam_schedule.end_time.replace(tzinfo=None) == new_end_time.replace(tzinfo=None)

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