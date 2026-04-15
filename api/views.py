from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from rest_framework import generics

from .models import AirQualityRecord
from .serializers import AirQualityRecordSerializer


class HealthCheckView(View):
    def get(self, request):
        return JsonResponse({"status": "ok", "service": "air-quality-api"})


class AirQualityRecordCreateView(generics.CreateAPIView):
    queryset = AirQualityRecord.objects.all()
    serializer_class = AirQualityRecordSerializer


class APITestPageView(TemplateView):
    template_name = "api/test_client.html"
