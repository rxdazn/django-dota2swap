from django.db import models

class Hero(models.Model):
    unique_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    alternative_name = models.CharField(max_length=100, default='') # named used in item paths
    localized_name = models.CharField(max_length=255)
    image_small = models.URLField()
    image_full = models.URLField()
    available = models.BooleanField(default=True)
