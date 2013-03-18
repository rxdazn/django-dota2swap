from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

#from dota2sawp.utils.fetch_schema


class Command(BaseCommand):
    help = 'Fetches the item schema and updates items'

    option_list = BaseCommand.option_list + (
            make_option('-v', '--verbose',
                action='store', dest='verbosity', default=False,
                help='Verbosity level')

    def handle(self, *args, **options):
        verbose = options.get('verbosity')

        #if verbose:
