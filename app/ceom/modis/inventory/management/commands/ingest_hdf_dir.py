from django.core.management.base import BaseCommand, CommandError
from ceom.modis.inventory.models import File, Dataset, Tile
from django.db import IntegrityError
import os

class Command(BaseCommand):
    help = 'Populates Files table with files from a specified directory that contains .hdf files'

    def add_arguments(self, parser):
        parser.add_argument('dir', nargs=1, type=str)

    def handle(self, *args, **options):
        dir = options['dir'][0]

        if not os.path.exists(dir):
            raise CommandError('Directory "%s" does not exist' % dir)

        for root, dirs, files in os.walk(dir):
            for filename in files:
                if filename.endswith('.hdf'):
                    absolute_path = os.path.join(root, filename)
                    file_parts = filename.split(".")
                    
                    year = file_parts[1][1:5]
                    day = file_parts[1][5:]
                    timestamp = file_parts[4]

                    if not day.isnumeric() or not year.isnumeric():
                        raise CommandError(f'Either day {day} or year {year} is non-numeric: {absolute_path}')

                    try:
                        dataset = Dataset.objects.get(name=file_parts[0])
                    except Dataset.DoesNotExist:
                        raise CommandError(f'Dataset {file_parts[0]} specified in filename is not present in Dataset list: {absolute_path}')

                    try:
                        tile = Tile.objects.get(name=file_parts[2])
                    except Dataset.DoesNotExist:
                        raise CommandError(f'Tile specified in filename is not present in Tile list: {absolute_path}')

                    try:
                        File.objects.create(name=filename, tile=tile, year=year, day=day, timestamp=timestamp, dataset=dataset, absolute_path=absolute_path)
                        print(f"New file: {absolute_path}")
                    except IntegrityError:
                        print(f"File already exists in database: {absolute_path}")

        self.stdout.write(self.style.SUCCESS(f'Ingesting successful: {dir}'))