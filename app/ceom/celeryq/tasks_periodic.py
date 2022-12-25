from ceom.celery import app
from django.db import IntegrityError
import os, glob, datetime, random, time
from datetime import datetime, timedelta

from django.conf import settings


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