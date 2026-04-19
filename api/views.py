from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import AirQualityRecord
from .serializers import AirQualityRecordSerializer, CityTrendResponseSerializer


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


class AirQualityRecordRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AirQualityRecord.objects.all()
    serializer_class = AirQualityRecordSerializer


class APITestPageView(TemplateView):
    template_name = "api/test_client.html"


class CityTrendAnalyticsView(APIView):
    """
    获取指定城市某污染物的时间趋势数据
    参数: city - 城市名
          pollutant - 污染物类型 (pm25/pm10/no2/co/aqi)
    返回: 按日期排序的污染物数值列表
    """

    VALID_POLLUTANTS = ["pm25", "pm10", "no2", "co", "aqi"]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="city",
                location=OpenApiParameter.QUERY,
                required=True,
                type=str,
                description="城市名称（精确匹配，不区分大小写）",
            ),
            OpenApiParameter(
                name="pollutant",
                location=OpenApiParameter.QUERY,
                required=True,
                type=str,
                enum=["pm25", "pm10", "no2", "co", "aqi"],
                description="污染物类型",
            ),
        ],
        responses={
            200: CityTrendResponseSerializer,
            400: {
                "type": "object",
                "properties": {
                    "error": {"type": "string", "example": "city 参数是必需的"}
                },
            },
            404: {
                "type": "object",
                "properties": {
                    "message": {"type": "string", "example": "未找到城市 Delhi 的记录"}
                },
            },
        },
    )
    def get(self, request):
        city = request.query_params.get("city")
        pollutant = request.query_params.get("pollutant")

        # 验证必需参数
        if not city:
            return Response(
                {"error": "city 参数是必需的"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not pollutant:
            return Response(
                {"error": "pollutant 参数是必需的"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 验证污染物类型
        if pollutant not in self.VALID_POLLUTANTS:
            return Response(
                {
                    "error": f"pollutant 参数无效，必须是: {', '.join(self.VALID_POLLUTANTS)}"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 查询该城市的记录，按日期升序
        records = AirQualityRecord.objects.filter(city__iexact=city).order_by("date")

        if not records.exists():
            return Response(
                {"message": f"未找到城市 {city} 的记录"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # 构建趋势数据 - 返回日期和对应的污染物值
        trend_data = []
        for record in records:
            value = getattr(record, pollutant)
            if value is not None:
                trend_data.append({
                    "date": record.date.isoformat(),
                    "value": value,  # 使用固定字段名 "value"
                })

        return Response(
            {
                "city": city,
                "pollutant": pollutant,
                "count": len(trend_data),
                "data": trend_data,
            },
            status=status.HTTP_200_OK,
        )

