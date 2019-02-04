from django.db import models
from django.contrib import admin

class openUVData(models.Model):
	uv_date=(models.DateTimeField('datetime of reading'))
	uv=(models.DecimalField(max_digits=8,decimal_places=6))

class WilyWeatherData(models.Model):
	uv_date=(models.DateTimeField('datetime of reading'))
	uv=(models.DecimalField(max_digits=5,decimal_places=3))

admin.site.register(openUVData)
admin.site.register(WilyWeatherData)

