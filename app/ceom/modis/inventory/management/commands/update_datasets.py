from django.core.management.base import BaseCommand, CommandError
from ceom.modis.inventory.models import File, Dataset, Tile
from django.db import IntegrityError
import os, datetime

class Command(BaseCommand):
    help = '''Removes database entries for .hdf files that no longer exist, and adds new entries for new .hdf files. Updates all of the datasets at once.
                This process requires that each dataset has the file location of the dataset specified.
                Fair warning, this command may take a while.'''

    def handle(self, *args, **options):
        print("Running update_datasets command at time:", datetime.datetime.now())

        datasets = Dataset.objects.all()
        
        for dataset in datasets:
            file_set = File.objects.filter(dataset=dataset)

            stale_files = [file.name for file in file_set if not os.path.isfile(file.absolute_path)]

            if len(stale_files) == 0:
                print(f"No stale files for dataset {dataset.name}")
                continue
            
            print(f"Removing {len(stale_files)} stale file entries from the database for dataset {dataset.name}.")
        
            File.objects.filter(name__in=stale_files).delete()    

            self.stdout.write(self.style.SUCCESS(f'Successfully deleted {len(stale_files)} files.'))


        for dataset in datasets:
            dir = dataset.location

            if not os.path.exists(dir):
                raise CommandError(f'Data location "{dir}" for dataset {dataset.name} does not exist.')

            for root, dirs, files in os.walk(dir):
                for filename in files:
                    if not filename.endswith('.hdf'):
                        continue

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
                    except Tile.DoesNotExist:
                        raise CommandError(f'Tile specified in filename {absolute_path} is not present in Tile list')

                    if File.objects.filter(name=filename).exists():
                        #print(f"File already exists in database: {absolute_path}")
                        pass
                    else:
                        File.objects.create(name=filename, tile=tile, year=year, day=day, timestamp=timestamp, dataset=dataset, absolute_path=absolute_path)
                        print(f"New file: {absolute_path}")

            self.stdout.write(self.style.SUCCESS(f'Ingesting successful: {dir}'))