from django.db import models

from accounts.models import Member


class ItemQuality(models.Model):
    value = models.IntegerField()
    name = models.CharField(max_length=50)

class Item(models.Model):
    name = models.CharField(max_length=100)
    defindex = models.IntegerField() # item's unique ID
    type_name = models.CharField(max_length=30)
    description = models.TextField()
    proper_name = models.BooleanField() # 'The' prefixed
    quality = models.ForeignKey(ItemQuality)
    image_url = models.URLField()
    image_url_large = models.URLField()
    item_set = models.CharField(max_length=100)

class ItemSet(models.Model):
    item_set = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    store_bundle = models.CharField(max_length=100)

class Transaction(models.Model):
    item_pack = models.ForeignKey(Item)
    creator = models.OneToOneField(Member)
