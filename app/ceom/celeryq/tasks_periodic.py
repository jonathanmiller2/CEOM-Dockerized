from celery import shared_task
from django.db import IntegrityError
import os, datetime, random

from django.conf import settings

@shared_task
def update_datasets():
    #This import has to be done when this function gets called, as it requires that the Django apps be loaded, which isn't completed when the above imports run.
    from ceom.modis.inventory.models import File, Dataset, Tile

    with open('celerybeat.log', 'a') as f:
        f.write(f"Running update_datasets command at time: {datetime.datetime.now()}\n")

        datasets = Dataset.objects.all()
        
        for dataset in datasets:
            file_set = File.objects.filter(dataset=dataset)

            stale_files = [file.name for file in file_set if not os.path.isfile(file.absolute_path)]

            if len(stale_files) == 0:
                f.write(f"No stale files for dataset {dataset.name}\n")
                continue
            
            f.write(f"Removing {len(stale_files)} stale file entries from the database for dataset {dataset.name}.\n")
        
            File.objects.filter(name__in=stale_files).delete()    

            f.write(f'Successfully deleted {len(stale_files)} files.\n')


        for dataset in datasets:
            dir = dataset.location

            if not dir or len(dir) == 0:
                f.write(f"No specified location for dataset {dataset.name}\n")
                continue

            if not os.path.exists(dir):
                f.write(f'Data location "{dir}" for dataset {dataset.name} does not exist.')
                raise Exception(f'Data location "{dir}" for dataset {dataset.name} does not exist.')

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
                        f.write(f'Either day {day} or year {year} is non-numeric: {absolute_path}')
                        raise Exception(f'Either day {day} or year {year} is non-numeric: {absolute_path}')

                    try:
                        dataset = Dataset.objects.get(name=file_parts[0])
                    except Dataset.DoesNotExist:
                        f.write(f'Dataset {file_parts[0]} specified in filename is not present in Dataset list: {absolute_path}')
                        raise Exception(f'Dataset {file_parts[0]} specified in filename is not present in Dataset list: {absolute_path}')

                    try:
                        tile = Tile.objects.get(name=file_parts[2])
                    except Tile.DoesNotExist:
                        f.write(f'Tile specified in filename {absolute_path} is not present in Tile list')
                        raise Exception(f'Tile specified in filename {absolute_path} is not present in Tile list')

                    if File.objects.filter(name=filename).exists():
                        #f.write(f"File already exists in database: {absolute_path}\n")
                        pass
                    else:
                        File.objects.create(name=filename, tile=tile, year=year, day=day, timestamp=timestamp, dataset=dataset, absolute_path=absolute_path)
                        f.write(f"New file: {absolute_path}\n")

            f.write(self.style.SUCCESS(f'Ingesting successful: {dir}\n'))
