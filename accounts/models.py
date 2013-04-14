from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser 
from django.utils import timezone

#from shop.models import Item


class MemberManager(BaseUserManager):

    def create_user(self, username, email=None, password=None, **extra_fields):
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

    def update_inventory(self):
        inventory_json = SteamWrapper.get_player_inventory(self.steam_id)
        if inventory_json['status'] is 1:
            items = []
            for item in inventory['items']:
                origin = models.ItemOrigin.objects.get(value=items['origin'])
                quality = models.ItemQuality.objects.get(value=items['quality'])
                attributes = []
                if 'attributes' in item:
                    for attribute in item['attributes']:
                        account_info = None
                        if 'account_info' in attribute:
                            account_info = models.AccountInfo(
                                    steam_id=attribute['account_info'],
                                    personaname=attribute['personaname'])
                        attribute = models.InventoryItemAttribute.objects.create(
                            defindex=attribute['defindex'],
                            value=attribute['value'],
                            float_value=attribute.get('float_value'),
                            account_info=account_info)
                        attributes.append(attribute)

                item, created = models.InventoryItem.objects.get_or_create(
                        unique_id=item['id'],
                        original_id=item['original_id'],
                        defindex=item['defindex'],
                        level=item['level'],
                        quantity=item['quantiy'],
                        origin=origin,
                        inventory=item.get('inventory'),
                        flag_cannot_trade=item.get('flag_cannot_trade'),
                        flag_cannot_craft=item.get('flag_cannot_craft'),
                        quality=quality,
                        custom_name=item.get('custom_name'),
                        custom_description=item.get('custom_desc'),
                        contained_item=item.get('contained_item'),
                        )
                item.save()
                item.attributes.add(*attributes)
            return 'Sucessfuly updated inventory.'
            
        elif inventory_json['status'] is 8:
            return 'Couldn\'t update inventory. The steamid parameter was invalid or missing.'
        elif inventory_json['status'] is 15:
            return 'Couldn\'t update inventory. Backpack is private.'
        elif inventory_json['status'] is 18:
            return 'Couldn\'t update inventory. Backpack is private.'



