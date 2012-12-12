from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    name = models.CharField()
    defindex = models.IntegerField() # item's unique ID
    # class = 
    type_name = models.CharField()
    description = models.TextField()
    proper_name = models.BooleanField() # 'The' prefixed
    #quality = models.IntegerField()
    image_url = models.URLField()
    image_url_large = models.URLField()
    item_set = models.CharField()
