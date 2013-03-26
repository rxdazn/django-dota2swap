from django.db import models

from accounts.models import Member


class ItemQuality(models.Model):
    value = models.IntegerField(unique=True)
    name = models.CharField(max_length=50)


class ItemCapabilities(models.Model):
    can_be_restored = models.BooleanField()
    can_craft_mark = models.BooleanField()
    paintable_unusual = models.BooleanField()
    strange_parts = models.BooleanField()
    usable_out_of_game = models.BooleanField()
    usable_gc = models.BooleanField()


class Attribute(models.Model):
    defindex = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    attribute_class = models.CharField(max_length=100)
    min_value = models.FloatField()
    max_value = models.FloatField()
    description_token = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    description_format = models.CharField(max_length=100, null=True, blank=True)
    effect_type = models.CharField(max_length=100)
    hidden = models.BooleanField(default=False)
    stored_as_integer = models.BooleanField(default=False)


class Item(models.Model):
    defindex = models.IntegerField(unique=True) # item's unique ID
    name = models.CharField(max_length=100) # proper name with spaces
    type_token = models.CharField(max_length=100) # #DOTA_WearableTyep_Daggers
    description_token = models.CharField(max_length=100) # #DOTA_Item_Rikis_Dagger 
    description = models.TextField(null=True, blank=True)
    #capabilities = models.ForeignKey(ItemCapabilities, null=True, blank=True)
    # tool = models.ForeignKey(Tool, null=True, blank=True) # e.g bundles #OpenPack token
    # attributes = models.ForeignKey(Attribute, null=True, blank=True)
    proper_name = models.BooleanField() # 'The' prefixed
    item_class = models.CharField(max_length=100)
    quality = models.ForeignKey(ItemQuality)
    image = models.URLField()
    image_large = models.URLField()
    item_set = models.CharField(max_length=100, null=True, blank=True)
    min_ilevel = models.IntegerField(default=1)
    max_ilevel = models.IntegerField(default=1)


class ItemSet(models.Model):
    item_set = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    store_bundle = models.CharField(max_length=100)


class Transaction(models.Model):
    item_pack = models.ForeignKey(Item)
    creator = models.OneToOneField(Member)
