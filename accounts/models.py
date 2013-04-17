from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils import timezone

from django.contrib import messages

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
    email = models.EmailField(max_length=256, null=True, blank=True)
    date_joined = models.DateTimeField()
    avatar_small = models.URLField()
    avatar_medium = models.URLField()
    avatar_full = models.URLField()
    personastate = models.IntegerField(default=0)
    reputation = models.IntegerField(default=0)
    transactions_completed = models.IntegerField(default=0)
    items = models.ManyToManyField('shop.InventoryItem')
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
        print '===> !!! create user'
        now = timezone.now()
        user.steam_id = details['player']['steamid']
        return True

    pre_update.connect(user_update_handler, sender=SteamBackend)
    socialauth_registered.connect(user_creation_handler, sender=None)

    def update_inventory(self):
        from dota2swap.utils.api import SteamWrapper
        from shop import models

        player_backpack = SteamWrapper.get_player_inventory(self.steam_id)
        if 'result' not in player_backpack:
            print 'player_backpack', player_backpack.keys()
            print 'Error fetching user backpack'
            return None
        else:
            inventory_json = player_backpack['result']
            if inventory_json['status'] is 1:
                items = []

                print 'backpack has {0} items', inventory_json['items'].__len__()
                for item in inventory_json['items']:
                    try:
                        item = models.InventoryItem.objects.get(unique_id=item['id'])
                        print 'object already exists'
                        related_members = item.member_set.all()
                        if related_members:
                            if related_members[0].steam_id != self.steam_id:
                                print 'diff owner', related_members[0].steam_id, self.steam_id
                                item.member_set.remove(related_members) # change owner if found in another backpack
                                item.member_set.add(self)
                    except models.InventoryItem.DoesNotExist:
                        origin=None
                        if 'origin' in item:
                            origin = models.ItemOrigin.objects.get(value=item['origin'])
                        quality = models.ItemQuality.objects.get(value=item['quality'])
                        attributes = []
                        if 'attributes' in item:
                            for attribute in item['attributes']:
                                account_info = None
                                if 'account_info' in attribute:
                                    account_info = models.AccountInfo(
                                            steam_id=attribute['account_info'],
                                            personaname=attribute['personaname'])
                                base_attribute = models.Attribute.objects.get(defindex=attribute['defindex'])
                                attribute = models.InventoryItemAttribute.objects.create(
                                    attribute=base_attribute,
                                    value=attribute['value'],
                                    float_value=attribute.get('float_value'),
                                    account_info=account_info)
                                attributes.append(attribute)
                        # item only added if it is not in the user's backpack yet
                        base_item = models.Item.objects.get(defindex=item['defindex'])
                        # inventory slot number is stored in the last 16 bits
                        # of the item['inventory'] 32 bit unsigned int
                        # int32 -> binary -> slice last 16 bits -> construct int from base 2
                        # first row of inventory (5) items have their
                        # slot_number set to 0 so they are randomly displayed
                        slot_number = int(bin(item['inventory'])[-16:], 2)
                        item = models.InventoryItem(
                                base_item=base_item,
                                unique_id=item['id'],
                                original_id=item['original_id'],
                                defindex=item['defindex'],
                                slot_number=slot_number,
                                level=item['level'],
                                quantity=item['quantity'],
                                origin=origin,
                                inventory=item.get('inventory'),
                                flag_cannot_trade=item.get('flag_cannot_trade'),
                                flag_cannot_craft=item.get('flag_cannot_craft'),
                                quality=quality,
                                custom_name=item.get('custom_name'),
                                custom_description=item.get('custom_desc'),
                                contained_item=item.get('contained_item'),)
                        item.save()
                        item.attributes.add(*attributes)
                        items.append(item)
                print '%d items to add' % items.__len__()
                self.items.add(*items)
                return 'Sucessfuly updated inventory.'

            elif inventory_json['status'] is 8:
                return 'Couldn\'t update inventory. The steamid parameter was invalid or missing.'
            elif inventory_json['status'] is 15:
                return 'Couldn\'t update inventory. Backpack is private.'
            elif inventory_json['status'] is 18:
                return 'Couldn\'t update inventory. Backpack is private.'
