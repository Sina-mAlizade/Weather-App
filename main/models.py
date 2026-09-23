from django.db import models

class SearchHistory(models.Model):
    city_name = models.CharField(max_length=100)
    temperature = models.FloatField(null=True, blank=True)
    feels_like = models.FloatField(null=True, blank=True)
    temp_min = models.FloatField(null=True, blank=True)
    temp_max = models.FloatField(null=True, blank=True)
    humidity = models.IntegerField(null=True, blank=True)
    pressure = models.IntegerField(null=True, blank=True)
    cloudiness = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    wind_speed = models.FloatField(null=True, blank=True)
    wind_direction = models.CharField(max_length=5, null=True, blank=True)
    visibility = models.IntegerField(null=True, blank=True)
    sunrise = models.CharField(max_length=10, null=True, blank=True)
    sunset = models.CharField(max_length=10, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    searched_at = models.DateTimeField(auto_now_add=True)
    uv_index = models.IntegerField(null=True , blank=True)
    aqi = models.IntegerField(null=True, blank=True)
    aqi_category = models.CharField(max_length=40, null=True, blank=True)

    def __str__(self):
        return f"{self.city_name} at {self.searched_at.strftime('%Y-%m-%d %H:%M')}"
