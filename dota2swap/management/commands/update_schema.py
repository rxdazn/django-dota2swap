from optparse import make_option, OptionParser

from django.core.management.base import BaseCommand, CommandError

from dota2swap.utils.api import SteamWrapper


class Command(BaseCommand):
    help = 'Fetches the item schema and updates items'

    parser = OptionParser()
    parser.add_option( '-v', '--verbose',
                action='store', dest='verbosity', default=False,
                help='Verbosity level')

    def handle(self, *args, **options):
        verbose = options.get('verbosity')
        self.stdout.write('fetching item schema...')
        schema = SteamWrapper.get_schema()
        print schema
