from django.urls import path

from .views import APITestPageView, AirQualityRecordListCreateView, HealthCheckView

urlpatterns = [
    path("health/", HealthCheckView.as_view(), name="health-check"),
    path("records/", AirQualityRecordListCreateView.as_view(), name="record-list-create"),
    path("test-client/", APITestPageView.as_view(), name="api-test-client"),
]
