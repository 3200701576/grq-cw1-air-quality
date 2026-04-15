from django.urls import path

from .views import APITestPageView, AirQualityRecordCreateView, HealthCheckView

urlpatterns = [
    path("health/", HealthCheckView.as_view(), name="health-check"),
    path("records/", AirQualityRecordCreateView.as_view(), name="record-create"),
    path("test-client/", APITestPageView.as_view(), name="api-test-client"),
]
