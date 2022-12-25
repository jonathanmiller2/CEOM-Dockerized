from osgeo import gdal
from datetime import datetime, date, timedelta
import itertools, csv, os, math, glob
import pandas as pd

from ceom.celery import app
from ceom.modis.models import *

@app.task(bind=True)
def process_MODIS_single_site(self, media_root, csv_folder, dataset_name, dataset_loc, h, v, x, y, years):
    job_obj = MODISSingleTimeSeriesJob.objects.get(task_id=self.request.id)
    job_obj.percent_complete = 0
    job_obj.working = True
    job_obj.save()

    try:
        filename = '{}_h_{:d}_v_{:d}_x_{:d}_y_{:d}'.format(dataset_name, h, v, x, y) + "_" + "_".join(years) + ".csv"
        rel_file = os.path.join(csv_folder, filename)
        full_file = os.path.join(media_root, rel_file)
        nineteen_seventy = date.fromisoformat('1970-01-01')
        tile = 'h' + str(h).zfill(2) + 'v' + str(v).zfill(2)

        os.makedirs(os.path.join(media_root, csv_folder), exist_ok=True)
        
        records = []

        for year_index in range(len(sorted(years))):
            day_files = glob.glob(os.path.join(dataset_loc, years[year_index], tile, dataset_name + '*.hdf'))

            for day_index, day_file_loc in enumerate(sorted(day_files)):
                day_file_basename = os.path.basename(day_file_loc)
                day_in_year = int(day_file_basename.split('.')[1][-3:])
                file_date = date.fromisoformat(str(years[year_index]) + '-01-01') + timedelta(days=day_in_year - 1)
                print(day_file_basename)

                ds = gdal.Open(day_file_loc)

                subdatasets = ds.GetSubDatasets()

                record = {
                    'date': file_date
                }

                for i in range(len(subdatasets)):
                    subdataset_name = subdatasets[i][0].split(':')[4]
                    measurement_ds = gdal.Open(subdatasets[i][0])
                    record[subdataset_name] = measurement_ds.ReadAsArray(int(x), int(y), 1, 1)[0][0]

                records.append(record)

                year_starting_percent = year_index / len(years)
                year_ending_percent = (year_index + 1) / len(years)
                year_current_percent = (day_index + 1) / len(day_files)
                job_obj.percent_complete = (1 - year_current_percent) * year_starting_percent + year_current_percent * year_ending_percent
                job_obj.save()

        final_df = pd.DataFrame.from_records(records, index="date")
        final_df = final_df[sort_columns(dataset_name, list(final_df.columns))]

        with open(full_file, 'w+') as csvfile:
            final_df.to_csv(csvfile)

        job_obj.working = False
        job_obj.completed = True
        job_obj.percent_complete = 1
        job_obj.result.name = rel_file
        job_obj.save()

    except Exception as e:
        job_obj.working = False
        job_obj.completed = False
        job_obj.error = True
        job_obj.percent_complete = 1
        job_obj.save()

        # Re-raise exception
        raise e

    return














@app.task(bind=True)
def process_MODIS_multiple_site(self, media_root, csv_folder, dataset_name, dataset_loc, input_file, years, userid):
    pass









@app.task(bind=True)
def MODIS_fetch_day()
    records = []








def sort_columns(dataset_name, column_list):
    starting_columns = []

    if 'site' in column_list:
        starting_columns.append('site') 
        column_list.remove('site') 

    desired_order = { 
        'MOD09A1': [
                'date'
                'sur_refl_b01'
                'sur_refl_b02'
                'sur_refl_b03'
                'sur_refl_b04'
                'sur_refl_b05'
                'sur_refl_b06'
                'sur_refl_b07'
                'sur_refl_qc_500m'
                'sur_refl_szen'
                'sur_refl_vzen'
                'sur_refl_raz'
                'sur_refl_state_500m'
                'sur_refl_day_of_year'
            ],
    }

    for item in desired_order[dataset_name]:
        if item not in column_list:
            print("Sorting columns for MODIS task failed, item: " + item + " not found in column list.")
            
            # The hard-coded sort has failed. Returning alphabetical order.
            return starting_columns + sorted(column_list)

    # The hard-coded sort has succeeded. Returning hard-coded sort.
    return starting_columns + desired_order