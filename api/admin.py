from django.contrib import admin

from .models import AirQualityRecord


@admin.register(AirQualityRecord)
class AirQualityRecordAdmin(admin.ModelAdmin):
    list_display = ("city", "date", "aqi", "pm25", "pm10", "no2", "co")
    list_filter = ("city", "date")
    search_fields = ("city",)
