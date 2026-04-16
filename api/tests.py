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
        response = self.client.post(reverse("record-list-create"), payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AirQualityRecord.objects.count(), 1)
        self.assertEqual(response.data["city"], "Delhi")

    def test_create_record_missing_required_field(self):
        payload = {
            "date": "2020-01-01",
            "aqi": 250,
        }
        response = self.client.post(reverse("record-list-create"), payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("city", response.data)


class AirQualityRecordListAPITests(APITestCase):
    def setUp(self):
        AirQualityRecord.objects.create(
            city="Delhi",
            date="2020-01-01",
            pm25=120.0,
            pm10=180.0,
            no2=50.0,
            co=1.0,
            aqi=250,
        )
        AirQualityRecord.objects.create(
            city="Mumbai",
            date="2020-01-02",
            pm25=80.0,
            pm10=130.0,
            no2=40.0,
            co=0.8,
            aqi=180,
        )
        AirQualityRecord.objects.create(
            city="Delhi",
            date="2020-01-03",
            pm25=100.0,
            pm10=150.0,
            no2=45.0,
            co=0.9,
            aqi=210,
        )

    def test_list_records_success(self):
        response = self.client.get(reverse("record-list-create"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_list_records_filter_by_city(self):
        response = self.client.get(reverse("record-list-create"), {"city": "Delhi"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertTrue(all(item["city"] == "Delhi" for item in response.data))

    def test_list_records_filter_by_date_range(self):
        response = self.client.get(
            reverse("record-list-create"),
            {"start_date": "2020-01-02", "end_date": "2020-01-03"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
