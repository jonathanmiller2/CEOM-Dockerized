from ceom.celery import app
from django.db import IntegrityError
import os, glob, datetime, random, time
from datetime import datetime, timedelta

from django.conf import settings

@app.task
def update_datasets():
    #This import has to be done when this function gets called, as it requires that the Django apps be loaded, which isn't completed when the above imports run.
    from ceom.modis.models import File, Dataset, Tile

    with open('celerybeat.log', 'a') as f:
        f.write(f"Running update_datasets command at time: {datetime.now()}\n")

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



@app.task(soft_time_limit=7*24*60*60, time_limit=7*24*60*60)
def update_rasters():
    #TODO: Add entries to database for all products, layers, dates, and let celery process them
    #note, this will take 600,000 years

    #This import has to be done when this function gets called, as it requires that the Django apps be loaded, which isn't completed when the above imports run.
    from raster.models import RasterProduct, RasterLayer

    with open('celerybeat.log', 'a') as f:
        products = RasterProduct.objects.all()

        for product in products:
            #Ensure product location ends with a slash
            product_location = os.path.join(product.location, '')

            #Get unique datecodes (e.g. 2012049)
            product_filepaths = glob.glob(f"{product_location}*/*/*{product.name.lower()}.tif")
            datecodes = set()

            for product_filepath in product_filepaths:
                product_filename = os.path.basename(product_filepath)
                #MOD09A1.A2010073.h12v13.006.2015206114038.evi.tif
                
                datecode = product_filename.split('.')[1]
                #A2010073

                datecode = "".join(filter(str.isdigit, datecode)) # (filters all non-numerics)
                #2010073

                datecodes.add(datecode)
            
            for datecode in datecodes:
                year = datecode[:4]
                day = datecode[4:]
                
                mosaic_name = f"{product.name.lower()}-{datecode}.tif"
                mosaic_dir = os.path.join(settings.MEDIA_ROOT, "raster_mosaics/", product.name + "/" + year + "/")
                mosaic_location = f"{mosaic_dir}{mosaic_name}"

                if not RasterLayer.objects.filter(product=product, year=year, day=day).exists():
                    f.write(f"New layer for product {product.name},  year: {year},  day: {day}")
                    new_layer = RasterLayer.objects.create(product=product, year=year, day=day, location=mosaic_location, max_zoom=settings.RASTER_MAP_MAX_ZOOM, store_reprojected=False)

                time.sleep(60 * 5) #Give the raster time to process. This could be done better by using threading and waiting for the raster to be done processing, but a simple delay works for this script

@app.task
def clear_modis_csvs():
    from ceom.modis.models import MODISSingleTimeSeriesJob, MODISMultipleTimeSeriesJob
    from django.conf import settings

    week_ago = datetime.now() - timedelta(days=7)
    outdated_jobs = MODISMultipleTimeSeriesJob.objects.filter(modified__lt=week_ago)
    for outdated_job in outdated_jobs:
        try:
            res_path = os.path.join(settings.MEDIA_ROOT, outdated_job.result.path)
            if os.path.exists(res_path):
                os.remove(res_path)

            inp_path = os.path.join(settings.MEDIA_ROOT, outdated_job.points.path)
            if os.path.exists(inp_path):
                os.remove(inp_path)

        except ValueError:
            # Job never finished and has no file associated
            pass

        outdated_job.delete()
    
    outdated_jobs = MODISSingleTimeSeriesJob.objects.filter(modified__lt=week_ago)
    for outdated_job in outdated_jobs:
        try:
            res_path = os.path.join(settings.MEDIA_ROOT, outdated_job.result.path)
            if os.path.exists(res_path):
                os.remove(res_path)
        except ValueError:
            # Job never finished and has no file associated
            pass

        outdated_job.delete()