from django.db import models
from django.contrib.auth.models import User

class   Member(models.Model):
    user = models.ForeignKey(User)
    steam_id = models.CharField(max_length=20)
    reputation = models.IntegerField(default=0)
    transactions_completed = models.IntegerField(default=0)
