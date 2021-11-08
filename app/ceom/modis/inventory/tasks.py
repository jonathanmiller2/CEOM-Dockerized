import numpy as np
import os, glob
from osgeo import gdal
from ceom.celery import app

@app.task()
def assemble_mosaic():
    year = 2001
    day = 113
    files_to_mosaic = glob.glob(f'/data/satellite/modis/version006/products_006/MOD09A1/geotiff/evi/{year}/h*v*/*{year}{day}*.evi.tif')
    files_string = " ".join(files_to_mosaic)

    if not os.path.exists("/code/app/ceom/media/raster_mosaics/evi/"):
        os.makedirs("/code/app/ceom/media/raster_mosaics/evi/")

    command = "gdal_merge.py -o /code/app/ceom/media/raster_mosaics/evi/2001112.tif -of gtiff " + files_string
    print(os.popen(command).read())
