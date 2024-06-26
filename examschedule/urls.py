from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExamScheduleViewSet

router = DefaultRouter()
router.register(r'', ExamScheduleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]