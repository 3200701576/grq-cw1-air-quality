from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from rest_framework import generics

from .models import AirQualityRecord
from .serializers import AirQualityRecordSerializer


class HealthCheckView(View):
    def get(self, request):
        return JsonResponse({"status": "ok", "service": "air-quality-api"})


class AirQualityRecordListCreateView(generics.ListCreateAPIView):
    queryset = AirQualityRecord.objects.all()
    serializer_class = AirQualityRecordSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        city = self.request.query_params.get("city")
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")

        if city:
            queryset = queryset.filter(city__iexact=city)
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)

        return queryset


class AirQualityRecordRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = AirQualityRecord.objects.all()
    serializer_class = AirQualityRecordSerializer


class APITestPageView(TemplateView):
    template_name = "api/test_client.html"
