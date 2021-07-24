from django.core.management.base import BaseCommand, CommandError
from ceom.modis.inventory.models import File, Dataset
from django.db import IntegrityError
import os

class Command(BaseCommand):
    help = 'Removes File entries for given dataset if the entrys absolute path cannot be found on disk. HIGHLY DANGEROUS!'

    def add_arguments(self, parser):
        parser.add_argument('dataset', nargs=1, type=str)

    def handle(self, *args, **options):
        try:
            dataset = Dataset.objects.get(name=options['dataset'][0])
        except Dataset.DoesNotExist:
            raise CommandError(f'Dataset {options["dataset"][0]} does not exist')

        file_set = File.objects.filter(dataset=dataset)

        stale_files = [file.name for file in file_set if not os.path.isfile(file.absolute_path)]

        response = input(f"This will remove {len(stale_files)} file entries from the database. Are you sure you want to delete these entries? (y/n)")
        if response[0].lower() != "y":
            return
        
        File.objects.filter(name__in=stale_files).delete()    

        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {len(stale_files)} files.'))