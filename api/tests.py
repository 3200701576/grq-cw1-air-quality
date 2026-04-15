from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import AirQualityRecord


class AirQualityRecordCreateAPITests(APITestCase):
    def test_create_record_success(self):
        payload = {
            "city": "Delhi",
            "date": "2020-01-01",
            "pm25": 120.5,
            "pm10": 180.2,
            "no2": 55.4,
            "co": 1.1,
            "aqi": 250,
        }
        response = self.client.post(reverse("record-create"), payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AirQualityRecord.objects.count(), 1)
        self.assertEqual(response.data["city"], "Delhi")

    def test_create_record_missing_required_field(self):
        payload = {
            "date": "2020-01-01",
            "aqi": 250,
        }
        response = self.client.post(reverse("record-create"), payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("city", response.data)
