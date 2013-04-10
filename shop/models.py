from django.db import models

from accounts.models import Member

# raw json:
# https://gist.github.com/rxdazn/f1da0609ffc9f597d4b3/raw/077b8cc5f879fc31bc0958d982392e624e0b60c5/schema.json
#
# chrome json formatter 
# https://chrome.google.com/webstore/detail/json-formatter/bcjindcccaagfpapjjmafapmmgkkhgoa?hl=en 
#
# see http://wiki.teamfortress.com/wiki/WebAPI/GetSchema
# for details about these models

class ItemQuality(models.Model):
    value = models.IntegerField(unique=True)
    name = models.CharField(max_length=50)


class ItemOrigin(models.Model):
    value = models.IntegerField(unique=True)
    name = models.CharField(max_length=50)


class ItemParticles(models.Model):
    value = models.IntegerField(unique=True)
    attach_to_rootbone = models.BooleanField(default=False)
    attachment = models.CharField(null=True, blank=True, max_length=50)
    system = models.CharField(max_length=50)
    name = models.CharField(max_length=50)


class ItemCapabilities(models.Model):
    can_craft_mark = models.NullBooleanField(null=True)
    nameable = models.NullBooleanField(null=True)
    can_gift_wrap = models.NullBooleanField(null=True)
    can_be_restored = models.NullBooleanField(null=True)
    decodable = models.NullBooleanField(null=True)
    paintable_unusual = models.NullBooleanField(null=True)
    strange_parts = models.NullBooleanField(null=True)
    usable_gc = models.NullBooleanField(null=True)
    usable_out_of_game = models.NullBooleanField(null=True)


class ItemLevel(models.Model):
    name = models.CharField(max_length=50)
    level = models.IntegerField()
    required_score = models.IntegerField()


class ItemLevels(models.Model):
    name = models.CharField(max_length=50, unique=True)
    levels = models.ManyToManyField(ItemLevel)


class KillEaterRank(models.Model):
    name = models.CharField(max_length=50)
    level = models.IntegerField()
    required_score = models.IntegerField()


class KillEaterScoreType(models.Model):
    type = models.IntegerField()
    type_name = models.CharField(max_length=50)


class Attribute(models.Model):
    defindex = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    attribute_class = models.CharField(max_length=100)
    min_value = models.FloatField()
    max_value = models.FloatField()
    description = models.TextField(null=True, blank=True)
    description_format = models.CharField(max_length=100, null=True, blank=True)
    effect_type = models.CharField(max_length=100)
    hidden = models.BooleanField(default=False)
    stored_as_integer = models.BooleanField(default=False)

class ItemAttribute(models.Model):
    attribute = models.ForeignKey(Attribute)
    value = models.IntegerField()

class Item(models.Model):
    defindex = models.IntegerField(unique=True) # item's unique ID
    name = models.CharField(max_length=100) # proper name with spaces
    type_token = models.CharField(max_length=100) # #DOTA_WearableTyep_Daggers
    description_token = models.CharField(max_length=100) # #DOTA_Item_Rikis_Dagger
    description = models.TextField(null=True, blank=True)
    capabilities = models.ForeignKey(ItemCapabilities, null=True, blank=True)
    #tool = models.ForeignKey(Tool, null=True, blank=True) # e.g bundles #OpenPack token
    attributes = models.ManyToManyField(ItemAttribute, null=True, blank=True)
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
    store_bundle = models.CharField(max_length=100, null=True, blank=True)
    items = models.ManyToManyField(Item)
    attributes = models.ManyToManyField(ItemAttribute, null=True, blank=True)
     # FIXME items ?


class Transaction(models.Model):
    item_pack = models.ForeignKey(Item)
    creator = models.OneToOneField(Member)
