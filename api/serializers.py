from rest_framework import serializers

from .models import AirQualityRecord


class AirQualityRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirQualityRecord
        fields = [
            "id",
            "city",
            "date",
            "pm25",
            "pm10",
            "no2",
            "co",
            "aqi",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
