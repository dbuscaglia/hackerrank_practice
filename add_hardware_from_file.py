import csv
from datetime import datetime

from optparse import make_option
from django.core.management.base import BaseCommand
from django.db import transaction

from core.models.partner import Partner
from livelyhubs.models.hubs import Sensor, SensorCategory, Hub
from livelyhubs.models.placements import SensorPlacement

MISSING = '-1'

"""
Read a PCH format inventory file and write resulting Hubs and Sensors to the DB.

For now, the sensor_group field is silently ignored.

Entire file is treated as one transaction, so written all or none.  Mostly rely on the DB for
data validation - do some simple code checks just to avoid waste of starting then rolling back
transactions.
"""


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('-f', '--file-name', dest='file_name', help='name of input inventory file'),
    )

    HEADER = 'SKU,product_code,serial_code,firmware,manufacture_date,partner,ICCID,BT ID,Sensor Group ID\n'
    FIELDS = ['sku', 'product_code', 'serial_code', 'build', 'manufacture_date', 'partner',
        'ICCID','sensor_id','sensor_group']
    FIELDS_SET = set(FIELDS)

    HUB_FIELDS = ['sku', 'ICCID', 'product_code', 'serial_code','build', 'manufacture_date',
        'partner']
    HUB_OPTIONAL_FIELDS = []

    SENSOR_FIELDS = ['sku', 'build', 'manufacture_date', 'sensor_id', 'partner']
    SENSOR_OPTIONAL_FIELDS = ['product_code']

    #  SKU -> Defining data
    SENSORS = {
        'S1000PB1': {
            'placement': 'Pillbox 1',
            'sensor_type': 'accelerometer',
            'category': 'Pillbox 1'
        },
        'S1000REF': {
            'placement': 'Refrigerator',
            'sensor_type': 'accelerometer',
            'category': 'Refrigerator'
        },
        'S1000PB2': {
            'placement': 'Pillbox 2',
            'sensor_type': 'accelerometer',
            'category': 'Pillbox 2'
        },
        'S1000CUS':{
            'placement': 'Custom',
            'sensor_type': 'accelerometer',
            'category': 'Custom'
        },
        'W1000b': {
            'placement': 'Watch',
            'sensor_type': 'persw',
            'category': 'Watch'
        },
        'W1000w': {
            'placement': 'Watch',
            'sensor_type': 'persw',
            'category': 'Watch'
        }
    }

    HUBS = ('H1000',)

    def __init__(self):
        super(Command, self).__init__()
        self.sensors = []
        self.hubs = {}
        self.partner_map = dict(Partner.objects.all().values_list('name', 'id'))
        self.category_map = dict(SensorCategory.objects.all().values_list('name', 'id'))
        self.placement_map = dict(SensorPlacement.objects.all().values_list('name', 'id'))

    def extract_row(self, row, fields, optional_fields):
        """
        Extract requested data from the row.

        Raises on any unexpectedly populated fields, or required fields that are not populated.
        """
        data = {k: row[k] for k in fields}
        data.update({k: row[k] for k in optional_fields if row[k] != MISSING})

        assert all(row[i] == MISSING for i in self.FIELDS_SET.difference(fields + optional_fields)
            ), 'Value in field where value is not allowed '
        assert MISSING not in data.values(), 'Missing required field '

        data['manufacture_date'] = datetime.strptime(data['manufacture_date'], "%Y/%m/%d %H:%M")
        del data['sku']
        return data

    def parse_hub(self, row):
        """
        Create, but do not save, a hub instance from a file row.
        """
        data = self.extract_row(row, self.HUB_FIELDS, self.HUB_OPTIONAL_FIELDS)
        data['partner_id'] = self.partner_map[data['partner']]
        data['serial_code'] = int(data['serial_code'])
        del data['partner']
        return Hub(**data)

    def parse_sensor(self, row):
        """

        Create, but do not save, a sensor instance from a file row.

        If a sensor is linked to a hub, that hub must have been already read.
        """
        data = self.extract_row(row, self.SENSOR_FIELDS, self.SENSOR_OPTIONAL_FIELDS)
        sku_info = self.SENSORS[row['sku']]
        data.update({
            'sensor_id': data['sensor_id'].replace(':', ''),
            'sensorcategory_id': self.category_map[sku_info['category']],
            'placement_id': self.placement_map[sku_info['placement']],
            'sensor_type': sku_info['sensor_type']
        })
        if data['product_code']:
            data['hub'] = self.hubs[data['product_code']]
            del data['product_code']
        del data['partner']
        return Sensor(**data)


    @transaction.atomic
    def save_items(self):
        """
        Save all the new items to the DB.

        Cannot use bulk methods due to all the model.save() logic.  Need to do something about
        this if files get at all large.
        """
        for h in self.hubs.itervalues():
            h.save()

        for s in self.sensors:
            s.hub_id = s.hub.id  #  Otherwise will not assign
            s.save()

    def handle_file(self, infile):
        """
        Do all the command's work based on the open input file.
        """
        assert infile.readline() == self.HEADER, 'Unexpected file format per header row'
        reader = csv.DictReader(infile, fieldnames=self.FIELDS)
        try:
            for row in reader:
                sku = row['sku']
                if sku in self.SENSORS.keys():
                    self.sensors.append(self.parse_sensor(row))
                elif sku in self.HUBS:
                    hub = self.parse_hub(row)
                    assert hub.product_code not in self.hubs, 'Duplicate hub ' + hub.product_code
                    self.hubs[hub.product_code] = hub
                else:
                    raise Exception('Invalid SKU: ' + sku)
        except csv.Error as e:
            raise Exception('CSV error line {}: {}'.format(reader.line_num + 1, e))
        except AssertionError as e:
            raise Exception('{} line {}'.format(e, reader.line_num + 1))

        self.save_items()

    def handle(self, *args, **options):
        with open(options['file_name'], 'r') as kit_file:
            self.handle_file(kit_file)