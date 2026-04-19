from django.urls import path

from .views import (
    AirQualityRecordListCreateView,
    AirQualityRecordRetrieveUpdateDestroyView,
    CityTrendAnalyticsView,
    HealthCheckView,
)

urlpatterns = [
    path("health/", HealthCheckView.as_view(), name="health-check"),
    path("records/", AirQualityRecordListCreateView.as_view(), name="record-list-create"),
    path("records/<int:pk>/", AirQualityRecordRetrieveUpdateDestroyView.as_view(), name="record-retrieve"),
    path("analytics/city-trend/", CityTrendAnalyticsView.as_view(), name="city-trend-analytics"),
]
