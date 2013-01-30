from django.db import models

class ItemQuality(models.Model):
    value = models.IntegerField()
    name = models.CharField()

class Item(models.Model):
    name = models.CharField()
    defindex = models.IntegerField() # item's unique ID
    type_name = models.CharField()
    description = models.TextField()
    proper_name = models.BooleanField() # 'The' prefixed
    quality = models.ForeignKey(ItemQuality)
    image_url = models.URLField()
    image_url_large = models.URLField()
    item_set = models.CharField()

class ItemSet(models.Model):
    item_set = models.CharField()
    name = models.CharField()
    store_bundle = models.CharField()
