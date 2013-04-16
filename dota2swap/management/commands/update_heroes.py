from django.core.management.base import BaseCommand, CommandError
from django.core.management.base import NoArgsCommand

from dota2swap.utils.api import SteamWrapper

from dota2swap.models import Hero

class Command(NoArgsCommand):
    help = 'Fetches and updates the heroes'

    def disable_heroes(self, hero):
        if hero.unique_id >= 101:
            hero.available = False

    def update_hero(self, hero):
        try:
            db_hero = Hero.objects.get(unique_id=hero['id'])
            print 'Updating %s..' % hero['localized_name']
        except Hero.DoesNotExist:
            print 'Creating %s..' % hero['localized_name']
            db_hero = Hero()
            db_hero.unique_id = hero['id']
        db_hero.name = hero['name']
        db_hero.localized_name = hero['localized_name']
        db_hero.image_small = 'http://media.steampowered.com/apps/dota2/images/heroes/%s_sb.png' % '_'.join(db_hero.name.split('_')[3:])
        db_hero.image_full = 'http://media.steampowered.com/apps/dota2/images/heroes/%s_full.png' % '_'.join(db_hero.name.split('_')[3:])
        self.disable_heroes(db_hero)
        db_hero.save()
        print 'Done.'

    def fetch_heroes(self, result):
        try:
            for hero in result['result']['heroes']:
                self.update_hero(hero)
        except KeyError:
            print "Error while contacting steam API. Please retry."

    def handle(self, *args, **options):
        self.stdout.write('Fetching hero list..')
        result = SteamWrapper.get_hero_list()
        self.fetch_heroes(result)
        self.stdout.write('Finished.')
