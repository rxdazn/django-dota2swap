from optparse import make_option, OptionParser

from django.core.management.base import BaseCommand, CommandError
from django.core.management.base import NoArgsCommand

from dota2swap.utils.api import SteamWrapper
from shop import models


class Command(NoArgsCommand):
    help = 'Fetches the item schema and updates items'

    def process_origin_names(self, result):
        self.stdout.write('Processing item origins (%d)...' %
                len(result['originNames']))
        for origin_name in result['originNames']:
            origin, created = models.ItemOrigin.objects.get_or_create(
                    value=origin_name['origin'],
                    name=origin_name['name']
                    )

            if created and self.verbosity:
                self.stdout.write('created origin %s value %d' %(
                    origin.name,
                    origin.value)
                    )


    def process_item_particles(self, result):
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
            if created and self.verbosity:
                self.stdout.write('created particle %s value %d' %(
                    origin.name,
                    origin.value)
                    )


    def process_item_quality(self, result):
        self.stdout.write('Processing item qualities (%d)...' %
                len(result['qualities']))

        for quality_name, item_quality in result['qualities'].items():
            quality, created = models.ItemQuality.objects.get_or_create(
                    value=item_quality,
                    name=quality_name,
                    )
            if created and self.verbosity:
                self.stdout.write('created quality %s value %d' %(
                    quality.name,
                    quality.value)
                    )


    def process_item_attributes(self, result):
        self.stdout.write('Processing item attributes (%d)...' %
                len(result['attributes']))

        for item_attribute in result['attributes']:
            attribute, created = models.Attribute.objects.get_or_create(
                defindex=item_attribute['defindex'],
                name=item_attribute['name'],
                attribute_class=item_attribute['attribute_class'],
                min_value=item_attribute['min_value'],
                max_value=item_attribute['max_value'],
                description=item_attribute.get('description_string'),
                description_format=item_attribute.get('description_format'),
                effect_type=item_attribute['effect_type'],
                hidden=item_attribute['hidden'],
                stored_as_integer=item_attribute['stored_as_integer'],
                )
            if created and self.verbosity:
                self.stdout.write('created attribute name %s index %d' %(
                    attribute.name,
                    attribute.defindex,)
                    )

    def process_kill_eater_ranks(self, result):
        self.stdout.write('Processing item kill eater ranks (%d)...' %
                len(result['kill_eater_ranks']))

        for kill_eater_rank in result['kill_eater_ranks']:
            rank, created = models.KillEaterRank.objects.get_or_create(
                name=kill_eater_rank['name'],
                required_score=kill_eater_rank['required_score'],
                level=kill_eater_rank['level'],
                )
            if created and self.verbosity:
                self.stdout.write('created kill eater rank name %s level %d' %(
                    rank.name,
                    rank.level)
                    )


    def process_item_levels(self, result):
        self.stdout.write('Processing item levels (%d)...' %
                len(result['item_levels']))

        for item_levels in result['item_levels']:
                try:
                    level_list = models.ItemLevels.objects.get(name=item_levels['name'])
                except models.ItemLevels.DoesNotExist: 
                    levels = []
                    for level in item_levels['levels']:
                        lvl, created = models.ItemLevel.objects.get_or_create(
                                name=level['name'],    
                                required_score=level['required_score'],
                                level=level['level'],)
                        levels.append(lvl)
                        if created and self.verbosity:
                            self.stdout.write('created item level named %s req score %d lvl %d' %
                                              (lvl.name, lvl.required_score, lvl.level))

                    level_list = models.ItemLevels(
                        name=item_levels['name'],
                        )
                    level_list.save() # save is needed before adding m2m related objects
                    level_list.levels.add(*levels)
                    
                    if self.verbosity:
                        self.stdout.write('created item level list named %s' % level_list.name)


    def process_kill_eater_score_types(self, result):
        self.stdout.write('Processing kill eater score types (%d)...' %
                len(result['kill_eater_score_types']))

        for kill_eater_score_type in result['kill_eater_score_types']:
            score_type, created = models.KillEaterScoreType.objects.get_or_create(
                type=kill_eater_score_type['type'],
                type_name=kill_eater_score_type['type_name'],
                )
            if created and self.verbosity:
                self.stdout.write(
                    'created item kill eater score type name %s type %d' %(
                    score_type.type_name,
                    score_type.type,)
                    )

    def process_items(self, result):
        self.stdout.write('Processing items (%d)...' %
                len(result['items']))

        for val, item in enumerate(result['items']):
            quality = models.ItemQuality.objects.get(value=item['item_quality'])
            capabilities = None
            if 'capabilities' in item:
                capabilities, created = models.ItemCapabilities.objects.get_or_create(
                        can_craft_mark = item.get('can_craft_mark'),
                        nameable = item.get('nameable'),
                        can_gift_wrap = item.get('can_gift_wrap'),
                        can_be_restored = item.get('can_be_restored'),
                        decodable = item.get('decodable'),
                        paintable_unusual = item.get('paintable_unusual'),
                        strange_parts = item.get('strange_parts'),
                        usable_gc = item.get('usable_gc'),
                        usable_out_of_game = item.get('usable_out_of_game'),
                        )
            attributes = []
            if 'attributes' in item:
                for attr in item['attributes']:
                    base_attribute = models.Attribute.get(description_format=attr['class'])
                    attribute = models.ItemAttribute(attribute=base_attribute, value=attr['value'])
                    attribute.save()
                    attributes.append(attribute)
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
                    'item_set': item.get('item_set'),
                    'min_ilevel': item['min_ilevel'],
                    'max_ilevel': item['max_ilevel'],
                }
                obj = models.Item(**item_infos)
                if capabilities:
                    obj.capabilities = capabilities
                obj.save()
                obj.attributes.add(*attributes)
                if self.verbosity:
                    self.stdout.write('obj defindex %d: %s' % (obj.defindex, obj.name))
            if val > 9: #only creating 10 for now -- testing
                break

    def process_item_sets(self, result):
        # FIXME items ?
        self.stdout.write('Processing item sets (%d)...' %
                len(result['item_sets']))

        for item_set in result['item_sets']:
            try:
                models.ItemSet.objects.get(name=item_set['name'])
            except models.ItemSet.DoesNotExist:
                attributes = []
                if 'attributes' in item_set:
                    for attr in item_set['attributes']:
                        base_attribute = models.Attribute.objects.get(description_format=attr['class'])
                        attribute = models.ItemAttribute(attribute=base_attribute, value=attr['value'])
                        attribute.save()
                        attributes += attribute

                items = [models.Item.objects.get(name=item_name) for item_name in item_set['items']]

                iset = models.ItemSet(
                    item_set=item_set['item_set'],
                    name=item_set['name'],
                    store_bundle=item_set.get('store_bundle'),
                    )
                iset.save()
                iset.items.add(*items)
                iset.attributes.add(*attributes)
                if self.verbosity:
                    self.stdout.write('created item set name %s' %(
                        iset.name,)
                        )


    def handle(self, *args, **options):
        self.verbosity = options.get('verbosity')
        self.stdout.write('Fetching item schema...')
        schema = SteamWrapper.get_schema()
        if schema['result']['status']:
            self.stdout.write('Successfully fetched item schema.')
            result = schema['result']

            self.process_origin_names(result)
            self.process_item_particles(result)
            self.process_item_quality(result)
            self.process_item_attributes(result)
            self.process_item_levels(result)
            self.process_kill_eater_ranks(result)
            self.process_kill_eater_score_types(result)
            self.process_items(result)
            self.process_item_sets(result)

        else:
            self.stderr.write('Error fetching schema. Result status value: %d' % schema['result']['status'])
