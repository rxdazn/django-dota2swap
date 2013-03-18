from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser 
from django.utils import timezone

from dota2swap.shop import Item


class MemberManager(BaseUserManager):

    def create_user(self, username, email=None, password=None, **extra_fields):
        now = timezone.now()
        now = timezone.now()
        user = self.model(username=username,
                email=email,
                last_login=now,
                date_joined=now)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None):
        user = self.create_user(username, email, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class Member(AbstractBaseUser):
    username = models.CharField(max_length=50) # permanent username
    nickname  = models.CharField(max_length=128) # display name
    steam_id = models.CharField(max_length=20)
    email = models.EmailField(max_length=256, null=True, blank=True, unique=True, db_index=True)
    date_joined = models.DateTimeField()
    avatar_small = models.URLField()
    avatar_medium = models.URLField()
    avatar_full = models.URLField()
    reputation = models.IntegerField(default=0)
    transactions_completed = models.IntegerField(default=0)
    # items = models.ForeignKey(Item)
    # transactions = models.ForeignKey(Transaction)
    is_admin = models.BooleanField(default=False)

    objects = MemberManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['username',]

    from social_auth.signals import pre_update, socialauth_registered
    from social_auth.backends.steam import SteamBackend

    def user_update_handler(sender, user, response, details, **kwargs):
        user.username = details['username']
        user.nickname = details['player']['personaname'] 
        user.avatar_small = details['player']['avatar']
        user.avatar_medium = details['player']['avatarmedium']
        user.avatar_full = details['player']['avatarfull']
        user.save()
        return True

    def user_creation_handler(sender, user, response, details, **kwargs):
        user.steam_id = details['player']['steamid']
        return True

    pre_update.connect(user_update_handler, sender=SteamBackend)
    socialauth_registered.connect(user_creation_handler, sender=None)
