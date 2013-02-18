from django.db import models
from django.contrib.auth.models import User

class MemberManager(models.Manager):

    def create_user(self, userans, email, password=None, **kwargs):
        print 'create user', username, email, password, kwargs
        return user

class   Member(models.Model):
    user = models.ForeignKey(User)
    username = models.CharField(max_length=30)
    steam_id = models.CharField(max_length=20)
    reputation = models.IntegerField(default=0)
    transactions_completed = models.IntegerField(default=0)
    objects = MemberManager()

