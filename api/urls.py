from django.urls import path

from .views import (
    APITestPageView,
    AirQualityRecordListCreateView,
    AirQualityRecordRetrieveView,
    HealthCheckView,
)

urlpatterns = [
    path("health/", HealthCheckView.as_view(), name="health-check"),
    path("records/", AirQualityRecordListCreateView.as_view(), name="record-list-create"),
    path("records/<int:pk>/", AirQualityRecordRetrieveView.as_view(), name="record-retrieve"),
    path("test-client/", APITestPageView.as_view(), name="api-test-client"),
]
