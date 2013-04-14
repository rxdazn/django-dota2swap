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
    can_craft_mark = models.NullBooleanField()
    nameable = models.NullBooleanField()
    can_gift_wrap = models.NullBooleanField()
    can_be_restored = models.NullBooleanField()
    decodable = models.NullBooleanField()
    paintable_unusual = models.NullBooleanField()
    strange_parts = models.NullBooleanField()
    usable_gc = models.NullBooleanField()
    usable_out_of_game = models.NullBooleanField()


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

class AccountInfo(models.Model):
    steam_id = models.CharField(max_length=100)
    personaname = models.CharField(max_length=100)

class InventoryItemAttribute(ItemAttribute):
    float_value = models.FloatField(null=True, blank=True)
    account_info = models.ForeignKey(AccountInfo, null=True, blank=True)

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

class InventoryItem(models.Model):
    unique_id = models.IntegerField()
    original_id = models.IntegerField()
    defindex = models.IntegerField()
    level = models.IntegerField()
    quantity = models.IntegerField()
    origin = models.ForeignKey(ItemOrigin)
    inventory = models.IntegerField(null=True, blank=True)
    flag_cannot_trade = models.NullBooleanField()
    flag_cannot_craft = models.NullBooleanField()
    quality = models.ForeignKey(ItemQuality)
    custom_name = models.CharField(max_length=200, null=True, blank=True)
    custom_description = models.CharField(max_length=200, null=True, blank=True)
    contained_item = models.CharField(max_length=600, null=True, blank=True)
    attributes = models.ManyToManyField(InventoryItemAttribute, null=True, blank=True)


class Transaction(models.Model):
    item_pack = models.ManyToManyField(InventoryItem)
    visible = models.BooleanField(default=True)
