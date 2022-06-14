import json
import logging

from django.core.management.base import BaseCommand, CommandError

from WeatherApp.models import City


class Command(BaseCommand):
    help = 'It parses the list of cities in the json content in the given file location and saves it to the database.'

    def add_arguments(self, parser):
        parser.add_argument('file_path', nargs='+', type=str)

    def handle(self, *args, **options):
        try:
            file = open(options['file_path'][0])
            city_list = json.load(file)
        except FileNotFoundError:
            logging.error('File Not Found error on import_cities command.')
            raise CommandError('File %s does not exist' % options['file_path'])
        except json.JSONDecodeError:
            logging.error('JSON Decode error on import_cities command.')
            raise CommandError('JSON decode error on file %s' % options['file_path'])

        # Delete all existing city entities.
        # It will not reset auto_increment, so it avoids further conflicts.
        City.objects.all().delete()

        for city in city_list:
            # Filter Canadian cities only
            if city['country'] == 'CA':
                City(
                    wid=city['id'],
                    name=city['name'],
                    state=city['state'],
                    country=city['country'],
                    coord_lat=city['coord']['lat'],
                    coord_lon=city['coord']['lon']
                ).save()

        self.stdout.write(self.style.SUCCESS('Cities successfully imported.'))
