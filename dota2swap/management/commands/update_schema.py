from optparse import make_option, OptionParser

from django.core.management.base import BaseCommand, CommandError

from dota2swap.utils.api import SteamWrapper
from shop import models


class Command(BaseCommand):
    help = 'Fetches the item schema and updates items'

    parser = OptionParser()
    parser.add_option( '-v', '--verbose',
                action='store', dest='verbosity', default=False,
                help='Verbosity level')

    def handle(self, *args, **options):
        verbose = options.get('verbosity')
        self.stdout.write('Fetching item schema...')
        schema = SteamWrapper.get_schema()
        if schema['result']['status']:
            self.stdout.write('Successfully fetched item schema.')
            result = schema['result']

            self.stdout.write('Processing item origins (%d)...' %
                    len(result['originNames']))

            self.stdout.write('Processing controlled item attached particles (%d)...' %
                    len(result['attribute_controlled_attached_particles']))

            self.stdout.write('Processing item qualities (%d)...' %
                    len(result['qualities']))

            self.stdout.write('Processing items (%d)...' %
                    len(result['items']))
            for item in result['items']:
                try:
                    obj = models.Item.objects.get(defindex=item['defindex'])
                except DoesNotExist:
                    obj = models.Item.objects.create(defintex=item['defindex'],
                            'name': item.get('name'),
                            'string_token': item.get('item_name'),
                            'type_token': item.get('item_type_name'),
                            'proper_name': item.get('proper_name'),
                            'quality': quality,
                            'item_class': item.get('item_class'),
                            'image': item.get('image_url'),
                            'image_large': item.get('image_large_url'),
                            'min_ilevel': item.get('min_ilevel'),
                            'max_ilevel': item.get('max_ilevel'),
                            )
            self.stdout.write('Processing item attributes (%d)...' %
                    len(result['attributes']))

            self.stdout.write('Processing item sets (%d)...' %
                    len(result['item_sets']))

            self.stdout.write('Processing item kill eater ranks (%d)...' %
                    len(result['kill_eater_ranks']))

            self.stdout.write('Processing item levels (%d)...' %
                    len(result['item_levels']))

            self.stdout.write('Processing kill eater score types (%d)...' %
                    len(result['kill_eater_score_types']))
        else:
            self.stderr.write('Error fetching schema. Result status value: %d' % schema['result']['status'])
