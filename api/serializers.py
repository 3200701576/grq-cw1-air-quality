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
        extra_kwargs = {
            "city": {"help_text": "城市名称"},
            "date": {"help_text": "日期（格式：YYYY-MM-DD）"},
            "pm25": {"help_text": "PM2.5 浓度 (μg/m³)"},
            "pm10": {"help_text": "PM10 浓度 (μg/m³)"},
            "no2": {"help_text": "NO2 浓度 (μg/m³)"},
            "co": {"help_text": "CO 浓度 (mg/m³)"},
            "aqi": {"help_text": "空气质量指数"},
        }


class TrendDataItemSerializer(serializers.Serializer):
    """趋势数据项序列化器"""
    date = serializers.DateField(help_text="日期（ISO 8601 格式）")
    value = serializers.FloatField(help_text="污染物浓度值")


class CityTrendResponseSerializer(serializers.Serializer):
    """城市趋势分析响应序列化器"""
    city = serializers.CharField(help_text="城市名称")
    pollutant = serializers.CharField(help_text="污染物类型（pm25/pm10/no2/co/aqi）")
    count = serializers.IntegerField(help_text="有效数据点数量（已过滤空值）")
    data = TrendDataItemSerializer(many=True, help_text="按日期排序的趋势数据列表")

