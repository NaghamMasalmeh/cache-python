from django.db import models

# Create your models here.

class CacheEntry(models.Model):
    key = models.PositiveIntegerField()
    value = models.CharField(max_length=30)
    access_time = models.TimeField()