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


    def process_origin_names(self, result, verbose):
        self.stdout.write('Processing item origins (%d)...' %
                len(result['originNames']))
        for origin_name in result['originNames']:
            origin, created = models.ItemOrigin.objects.get_or_create(
                    value=origin_name['origin'],
                    name=origin_name['name']
                    )
            if created and verbose:
                self.stdout.write('created origin %s value %d' %(
                    origin.name,
                    origin.value)
                    )


    def process_item_particles(self, result, verbose):
        self.stdout.write('Processing controlled item attached particles (%d)...' %
                len(result['attribute_controlled_attached_particles']))

        for item_particle in result['attribute_controlled_attached_particles']:
            origin, created = models.ItemParticles.objects.get_or_create(
                    value=item_particle['id'],
                    name=item_particle['name'],
                    system=item_particle['system'],
                    attach_to_rootbone=item_particle['attach_to_rootbone'],
                    attachment=item_particle.get('attachment'),
                    )
            if created and verbose:
                self.stdout.write('created particle %s value %d' %(
                    origin.name,
                    origin.value)
                    )


    def process_item_quality(self, result, verbose):
        self.stdout.write('Processing item qualities (%d)...' %
                len(result['qualities']))

        for item_quality in result['attribute_controlled_attached_particles']:
            quality, created = models.ItemQuality.objects.get_or_create(
                    value=item_quality,
                    name=result['attribute_controlled_attached_particles'][item_quality],
                    )
            if created and verbose:
                self.stdout.write('created quality %s value %d' %(
                    quality.name,
                    quality.value)
                    )


    def process_item_attributes(self, result, verbose):
        self.stdout.write('Processing item attributes (%d)...' %
                len(result['attributes']))

        for item_attribute in result['attributes']:
            attribute, created = models.Attribute.objects.get_or_create(
                defindex=item_attribute['defindex'],
                name=item_attribute['name'],
                attribute_class=item_attribute['attribute_class'],
                min_value=item_attribute['min_value'],
                max_value=item_attribute['max_value'],
                description_token=item_attribute['description_token'],
                description=item_attribute['description'],
                description_format=item_attribute['description_format'],
                effect_type=item_attribute['effect_type'],
                hidden=item_attribute['hidden'],
                stored_as_integer=item_attribute['stored_as_integer'],
                )
            if created and verbose:
                self.stdout.write('created attribute name %s index %d' %(
                    attribute.name,
                    attribute.defindex,)
                    )


    def process_item_sets(self, result, verbose):
        # FIXME items ?
        self.stdout.write('Processing item sets (%d)...' %
                len(result['item_sets']))

        for item_set in result['item_sets']:
            iset, created = models.ItemSet.objects.get_or_create(
                item_set=item_set['item_set'],
                name=item_set['name'],
                store_bundle=item_set['store_bundle'],
                )
            if created and verbose:
                self.stdout.write('created item set name %s' %(
                    iset.name,)
                    )

    def process_kill_eater_ranks(self, result, verbose):
        self.stdout.write('Processing item kill eater ranks (%d)...' %
                len(result['kill_eater_ranks']))

        for kill_eater_rank in result['kill_eater_ranks']:
            rank, created = models.KillEaterRank.objects.get_or_create(
                name=kill_eater_rank['name'],
                required_score=kill_eater_rank['required_score'],
                level=kill_eater_rank['level'],
                )
            if created and verbose:
                self.stdout.write('created kill eater rank name %s level %d' %(
                    rank.name,
                    rank.level)
                    )


    def process_item_levels(self, result, verbose):
        self.stdout.write('Processing item levels (%d)...' %
                len(result['item_levels']))

        for item_level in result['item_levels']:
            level, created = models.ItemLevel.objects.get_or_create(
                name=item_level['name'],
                required_score=item_level['required_score'],
                level=item_level['level'],
                )
            if created and verbose:
                self.stdout.write('created item level name %s level %d' %(
                    level.name,
                    level.level,)
                    )


    def process_kill_eater_score_types(self, result, verbose):
        self.stdout.write('Processing kill eater score types (%d)...' %
                len(result['kill_eater_score_types']))

        for kill_eater_score_type in result['kill_eater_score_types']:
            score_type, created = models.KillEaterScoreType.objects.get_or_create(
                type=kill_eater_score_type['type'],
                type_name=kill_eater_score_type['type_name'],
                )
            if created and verbose:
                self.stdout.write(
                    'created item kill eater score type name %s type %d' %(
                    score_type.type_name,
                    score_type.type,)
                    )


    def handle(self, *args, **options):
        verbose = options.get('verbosity')
        self.stdout.write('Fetching item schema...')
        schema = SteamWrapper.get_schema()
        if schema['result']['status']:
            self.stdout.write('Successfully fetched item schema.')
            result = schema['result']

            self.process_origin_names(result, verbose)
            self.process_item_particles(result, verbose)
            self.process_item_quality(result, verbose)
            self.process_item_attributes(result, verbose)
            self.process_item_sets(result, verbose)
            self.process_item_levels(result, verbose)
            self.process_kill_eater_ranks(result, verbose)
            self.process_kill_eater_score_types(result, verbose)

            self.stdout.write('Processing items (%d)...' %
                    len(result['items']))
            for val, item in enumerate(result['items']):
                quality, created = models.ItemQuality.objects.get_or_create(value=item['item_quality'], name='qualitemp')
                try:
                    obj = models.Item.objects.get(defindex=item['defindex'])
                    #print 'obj already existing !', [(field.name, field.value) for field in obj._meta.fields()]
                except models.Item.DoesNotExist:
                    item_infos = {
                        'defindex': item['defindex'],
                        'name': item['name'],
                        'description_token': item['item_name'],
                        'type_token': item['item_type_name'],
                        'proper_name': item['proper_name'],
                        'quality': quality,
                        'item_class': item['item_class'],
                        'image': item['image_url'],
                        'image_large': item['image_url_large'],
                        'min_ilevel': item['min_ilevel'],
                        'max_ilevel': item['max_ilevel'],
                    }
                    obj = models.Item(**item_infos)
                    # obj.save()
                    print 'obj defindex', obj.defindex, obj.name
                if val > 9: #only creating 10 for now -- testing
                    break
        else:
            self.stderr.write('Error fetching schema. Result status value: %d' % schema['result']['status'])
