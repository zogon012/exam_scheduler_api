# reservation/tests/test_reservation_views.py

import pytest
from django.urls import reverse
from rest_framework import status
from reservation.models import Reservation
from reservation.tests.factories import ReservationFactory, ScheduleFactory

@pytest.mark.django_db
def test_create_reservation(authenticated_client):
    client, user = authenticated_client()
    schedule = ScheduleFactory()
    url = reverse('reservation-list')
    data = {
        'schedule': schedule.id,
    }
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Reservation.objects.count() == 1
    reservation = Reservation.objects.get(id=response.data['id'])
    assert reservation.schedule.id == schedule.id
    assert reservation.user.id == user.id
    assert not reservation.is_confirmed

@pytest.mark.django_db
def test_update_reservation_with_admin(authenticated_client):
    client, user = authenticated_client(is_admin=True)
    reservation = ReservationFactory()
    url = reverse('reservation-detail', args=[reservation.id])
    data = {'is_confirmed': True}
    response = client.patch(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    reservation.refresh_from_db()
    assert reservation.is_confirmed

@pytest.mark.django_db
def test_update_reservation_with_non_admin(authenticated_client):
    client, user = authenticated_client(is_admin=False)
    reservation = ReservationFactory(user=user)
    url = reverse('reservation-detail', args=[reservation.id])
    data = {'is_confirmed': True}
    response = client.patch(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    reservation.refresh_from_db()
    assert not reservation.is_confirmed

@pytest.mark.django_db
def test_delete_reservation_with_admin(authenticated_client):
    client, user = authenticated_client(is_admin=True)
    reservation = ReservationFactory()
    initial_count = Reservation.objects.count()
    url = reverse('reservation-detail', args=[reservation.id])
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Reservation.objects.count() == initial_count - 1

@pytest.mark.django_db
def test_delete_reservation_with_non_admin(authenticated_client):
    client, user = authenticated_client(is_admin=False)
    reservation = ReservationFactory(user=user)
    initial_count = Reservation.objects.count()
    url = reverse('reservation-detail', args=[reservation.id])
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Reservation.objects.count() == initial_count - 1

@pytest.mark.django_db
def test_confirm_reservations(authenticated_client):
    client, user = authenticated_client(is_admin=True)
    schedule = ScheduleFactory()

    ReservationFactory.create_batch(100, schedule=schedule, is_confirmed=False)
    url = reverse('reservation-confirm-reservations')

    response = client.post(url)
    assert response.status_code == status.HTTP_200_OK
    confirmed_reservations = Reservation.objects.filter(is_confirmed=True)
    unconfirmed_reservations = Reservation.objects.filter(is_confirmed=False)

    assert confirmed_reservations.count() == 100
    assert unconfirmed_reservations.count() == 0

@pytest.mark.django_db
def test_list_reservations_as_admin(authenticated_client):
    client, user = authenticated_client(is_admin=True)
    ReservationFactory.create_batch(10)
    url = reverse('reservation-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 10

@pytest.mark.django_db
def test_list_reservations_as_non_admin(authenticated_client):
    client, user = authenticated_client(is_admin=False)
    ReservationFactory.create_batch(5, user=user)
    ReservationFactory.create_batch(5)
    url = reverse('reservation-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 5
    for reservation in response.data:
        assert reservation['user'] == user.id

@pytest.mark.django_db
def test_non_admin_cannot_confirm_reservations(authenticated_client):
    client, user = authenticated_client(is_admin=False)
    schedule = ScheduleFactory()
    ReservationFactory.create_batch(10, schedule=schedule, is_confirmed=False)
    url = reverse('reservation-confirm-reservations')

    response = client.post(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    confirmed_reservations = Reservation.objects.filter(is_confirmed=True)
    assert confirmed_reservations.count() == 0
