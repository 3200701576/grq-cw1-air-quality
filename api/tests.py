from django.urls import reverse
from django.http import JsonResponse
import json
from rest_framework import status
from rest_framework.test import APITestCase

from .models import AirQualityRecord


class HealthCheckAPITests(APITestCase):
    def test_health_check_returns_ok(self):
        response = self.client.get(reverse("health-check"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response["Content-Type"], "application/json")
        data = json.loads(response.content)
        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["service"], "air-quality-api")


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

    def test_create_record_duplicate_city_date_fails(self):
        payload = {
            "city": "Delhi",
            "date": "2020-01-01",
            "pm25": 120.5,
            "pm10": 180.2,
            "no2": 55.4,
            "co": 1.1,
            "aqi": 250,
        }
        self.client.post(reverse("record-list-create"), payload, format="json")
        response = self.client.post(reverse("record-list-create"), payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)

    def test_create_record_invalid_date_format_fails(self):
        payload = {
            "city": "Delhi",
            "date": "01-01-2020",
            "aqi": 250,
        }
        response = self.client.post(reverse("record-list-create"), payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("date", response.data)

    def test_create_record_invalid_numeric_type_fails(self):
        payload = {
            "city": "Delhi",
            "date": "2020-01-01",
            "aqi": "bad-value",
        }
        response = self.client.post(reverse("record-list-create"), payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("aqi", response.data)


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

    def test_list_records_filter_with_city_and_date_range(self):
        response = self.client.get(
            reverse("record-list-create"),
            {"city": "Delhi", "start_date": "2020-01-02", "end_date": "2020-01-03"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["city"], "Delhi")
        self.assertEqual(response.data[0]["date"], "2020-01-03")


class AirQualityRecordRetrieveAPITests(APITestCase):
    def setUp(self):
        self.record = AirQualityRecord.objects.create(
            city="Delhi",
            date="2020-01-01",
            pm25=120.0,
            pm10=180.0,
            no2=50.0,
            co=1.0,
            aqi=250,
        )

    def test_retrieve_record_success(self):
        response = self.client.get(reverse("record-retrieve", args=[self.record.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.record.id)
        self.assertEqual(response.data["city"], "Delhi")

    def test_retrieve_record_not_found(self):
        response = self.client.get(reverse("record-retrieve", args=[99999]))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_record_success(self):
        payload = {
            "aqi": 199,
            "pm25": 95.5,
        }
        response = self.client.patch(
            reverse("record-retrieve", args=[self.record.id]), payload, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.record.refresh_from_db()
        self.assertEqual(self.record.aqi, 199)
        self.assertEqual(self.record.pm25, 95.5)

    def test_put_record_success(self):
        payload = {
            "city": "Delhi",
            "date": "2020-01-01",
            "pm25": 200.0,
            "pm10": 300.0,
            "no2": 80.0,
            "co": 2.0,
            "aqi": 300,
        }
        response = self.client.put(
            reverse("record-retrieve", args=[self.record.id]), payload, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.record.refresh_from_db()
        self.assertEqual(self.record.pm25, 200.0)
        self.assertEqual(self.record.aqi, 300)

    def test_put_record_missing_required_field(self):
        payload = {
            "pm25": 200.0,
        }
        response = self.client.put(
            reverse("record-retrieve", args=[self.record.id]), payload, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("city", response.data)

    def test_patch_record_invalid_numeric_type_fails(self):
        payload = {
            "aqi": "bad-value",
        }
        response = self.client.patch(
            reverse("record-retrieve", args=[self.record.id]), payload, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("aqi", response.data)

    def test_patch_record_not_found(self):
        payload = {
            "aqi": 160,
        }
        response = self.client.patch(
            reverse("record-retrieve", args=[99999]), payload, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_record_success(self):
        response = self.client.delete(reverse("record-retrieve", args=[self.record.id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(AirQualityRecord.objects.count(), 0)

    def test_delete_record_not_found(self):
        response = self.client.delete(reverse("record-retrieve", args=[99999]))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CityTrendAnalyticsAPITests(APITestCase):
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
            city="Delhi",
            date="2020-01-02",
            pm25=110.0,
            pm10=170.0,
            no2=48.0,
            co=0.9,
            aqi=230,
        )
        AirQualityRecord.objects.create(
            city="Delhi",
            date="2020-01-03",
            pm25=100.0,
            pm10=160.0,
            no2=45.0,
            co=0.8,
            aqi=210,
        )
        AirQualityRecord.objects.create(
            city="Mumbai",
            date="2020-01-01",
            pm25=80.0,
            pm10=130.0,
            no2=40.0,
            co=0.8,
            aqi=180,
        )

    def test_city_trend_success(self):
        response = self.client.get(reverse("city-trend-analytics"), {"city": "Delhi", "pollutant": "pm25"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["city"], "Delhi")
        self.assertEqual(response.data["pollutant"], "pm25")
        self.assertEqual(response.data["count"], 3)
        self.assertEqual(len(response.data["data"]), 3)
        self.assertEqual(response.data["data"][0]["date"], "2020-01-01")
        self.assertEqual(response.data["data"][0]["value"], 120.0)

    def test_city_trend_requires_city_parameter(self):
        response = self.client.get(reverse("city-trend-analytics"), {"pollutant": "pm25"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "city 参数是必需的")

    def test_city_trend_requires_pollutant_parameter(self):
        response = self.client.get(reverse("city-trend-analytics"), {"city": "Delhi"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "pollutant 参数是必需的")

    def test_city_trend_invalid_pollutant(self):
        response = self.client.get(reverse("city-trend-analytics"), {"city": "Delhi", "pollutant": "invalid"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("pollutant 参数无效", response.data["error"])

    def test_city_trend_city_not_found(self):
        response = self.client.get(reverse("city-trend-analytics"), {"city": "UnknownCity", "pollutant": "pm25"})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("未找到城市", response.data["message"])

    def test_city_trend_with_different_pollutants(self):
        # 测试 aqi
        response = self.client.get(reverse("city-trend-analytics"), {"city": "Delhi", "pollutant": "aqi"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"][0]["value"], 250)

        # 测试 no2
        response = self.client.get(reverse("city-trend-analytics"), {"city": "Delhi", "pollutant": "no2"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"][0]["value"], 50.0)

        # 测试 co
        response = self.client.get(reverse("city-trend-analytics"), {"city": "Delhi", "pollutant": "co"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"][0]["value"], 1.0)

        # 测试 pm10
        response = self.client.get(reverse("city-trend-analytics"), {"city": "Delhi", "pollutant": "pm10"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"][0]["value"], 180.0)

    def test_city_trend_filters_null_values(self):
        # 创建一个记录，pm25 为 null
        AirQualityRecord.objects.create(
            city="Delhi",
            date="2020-01-04",
            pm25=None,
            pm10=150.0,
            no2=42.0,
            co=0.7,
            aqi=200,
        )
        response = self.client.get(reverse("city-trend-analytics"), {"city": "Delhi", "pollutant": "pm25"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 只有前 3 条记录有 pm25 值，第 4 条为 None 应该被过滤
        self.assertEqual(response.data["count"], 3)
        for item in response.data["data"]:
            self.assertIsNotNone(item["value"])

