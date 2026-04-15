from django.db import models


class AirQualityRecord(models.Model):
    city = models.CharField(max_length=100)
    date = models.DateField()
    pm25 = models.FloatField(null=True, blank=True)
    pm10 = models.FloatField(null=True, blank=True)
    no2 = models.FloatField(null=True, blank=True)
    co = models.FloatField(null=True, blank=True)
    aqi = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date", "city"]
        constraints = [
            models.UniqueConstraint(fields=["city", "date"], name="uniq_city_date")
        ]

    def __str__(self):
        return f"{self.city} - {self.date}"
