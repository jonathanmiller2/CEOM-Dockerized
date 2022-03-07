from ceom.celery import app
from ceom.tropomi.models import *
from osgeo import gdal

import itertools, csv, os
import numpy as np
from datetime import date, timedelta


@app.task(bind=True)
def process_TROPOMI_single_site(self, csv_folder, x, y, years):
    print(csv_folder)
    output_file = os.path.join(csv_folder, 'TROPOMI_x' + x + "_y" + y + "_" + "_".join(years) + ".csv")

    if not os.path.exists(csv_folder):
        os.makedirs(csv_folder)
    
    headers = ['date']
    data = []

    for year in years:
        data_file_location = TROPOMIYearFile.objects.get(year=year).location
        ds = gdal.Open(data_file_location)
        subdatasets = ds.GetSubDatasets()
        file_data = np.empty((46, len(subdatasets)))

        for i in range(len(subdatasets)):
            subdataset_name = subdatasets[i][0].split(':')[2]
            if subdataset_name not in headers:
                headers.append(subdataset_name)

            measurement_ds = gdal.Open(subdatasets[i][0])
            measurement_data = measurement_ds.ReadAsArray(int(x), int(y), 1, 1)

            # Measurements are packed in a (46,1,1)D triple-list, need to collapse down into (46,)D single list
            subds_data = list(itertools.chain.from_iterable(itertools.chain.from_iterable(measurement_data)))
            file_data[:,i] = subds_data
        

        year_start = date.fromisoformat(year + '-01-01')
        for i in range(46):
            row_date = year_start + timedelta(days=i*8)
            data.append([row_date] + list(file_data[i]))
        

    with open(output_file, 'w+') as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(headers)

        for row in data:
            writer.writerow(row)

    return
    


@app.task(bind=True)
def process_TROPOMI_multiple_site(self, csv_folder, input_file, years):
    pass