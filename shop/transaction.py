from django.db import models

class Transaction(models.Model):
    item_pack = models.OneToMany(Item)
    creator = models.OneToOne(Member)
