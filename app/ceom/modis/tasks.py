from osgeo import gdal
from datetime import datetime, date, timedelta
from celery import chain, group
import itertools, csv, os, math, glob
import pandas as pd

from ceom.celery import app
from ceom.modis.models import *

# This funcion isn't a celery task, but rather is an intermediary between the view and the celery tasks.
def process_MODIS_single_site(task_id, media_root, csv_folder, dataset_name, dataset_loc, h, v, x, y, years):
    job_obj = MODISSingleTimeSeriesJob.objects.get(task_id=task_id)
    job_obj.percent_complete = 0
    job_obj.working = True
    job_obj.save()

    try:
        filename = '{}_h{:d}_v{:d}_x{:d}_y{:d}'.format(dataset_name, h, v, x, y) + "_" + "_".join(years) + ".csv"
        rel_file = os.path.join(csv_folder, filename)
        full_file = os.path.join(media_root, rel_file)
        tile = 'h' + str(h).zfill(2) + 'v' + str(v).zfill(2)

        os.makedirs(os.path.join(media_root, csv_folder), exist_ok=True)
        
        subtask_params = []

        for year_index in range(len(sorted(years))):
            day_files = glob.glob(os.path.join(dataset_loc, years[year_index], tile, dataset_name + '*.hdf'))

            for day_file_loc in sorted(day_files):
                subtask_params.append([task_id, day_file_loc, x, y])

        # Now that we have the full list of subtask params, we know how many total subtasks there are
        # Knowing this, we can calculate the % of the total task that each subtask comprises, and pass that value as another param
        for subtask_param in subtask_params:
            subtask_param.append(1 / len(subtask_params))
        
        # Chunking vs. non-chunking.
        # chain(MODIS_fetch_day.chunks(subtask_params, 20).group(), finish_MODIS_single_site.s(task_id, dataset_name, full_file, rel_file)).delay()
        chain(group(MODIS_fetch_day.s(a, b, c, d, e) for a, b, c, d, e in subtask_params), finish_MODIS_single_site.s(task_id, dataset_name, full_file, rel_file)).delay()

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
def MODIS_fetch_day(self, task_id, day_file_loc, x, y, job_completion_fraction):
    day_file_basename = os.path.basename(day_file_loc)
    file_year = int(day_file_basename.split('.')[1][1:5])
    file_day = int(day_file_basename.split('.')[1][5:])
    file_date = date.fromisoformat(str(file_year) + '-01-01') + timedelta(days=file_day - 1)

    ds = gdal.Open(day_file_loc)

    subdatasets = ds.GetSubDatasets()

    record = {
        'date': file_date.strftime('%Y-%m-%d')
    }

    for i in range(len(subdatasets)):
        subdataset_name = subdatasets[i][0].split(':')[4]
        measurement_ds = gdal.Open(subdatasets[i][0])
        record[subdataset_name] = measurement_ds.ReadAsArray(int(x), int(y), 1, 1)[0][0].item()

    job_obj = MODISSingleTimeSeriesJob.objects.get(task_id=task_id)
    job_obj.percent_complete = job_obj.percent_complete + job_completion_fraction
    job_obj.save()

    return record


@app.task(bind=True)
def finish_MODIS_single_site(self, records, task_id, dataset_name, full_file, rel_file):
    # Unpack required if chunking subtasks
    # records = [item for sublist in records for item in sublist]

    job_obj = MODISSingleTimeSeriesJob.objects.get(task_id=task_id)

    final_df = pd.DataFrame.from_records(records, index="date")
    final_df = final_df[sort_columns(dataset_name, list(final_df.columns))]

    with open(full_file, 'w+') as csvfile:
        final_df.to_csv(csvfile)

    job_obj.working = False
    job_obj.completed = True
    job_obj.percent_complete = 1
    job_obj.result.name = rel_file
    job_obj.save()

    return


def sort_columns(dataset_name, column_list):
    starting_columns = []

    if 'site' in column_list:
        starting_columns.append('site') 
        column_list.remove('site') 

    DESIRED_ORDER = { 
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

    for item in DESIRED_ORDER[dataset_name]:
        if item not in column_list:
            print("Sorting columns for MODIS task failed, item: " + item + " not found in column list.")
            
            # The hard-coded sort has failed. Returning alphabetical order.
            return starting_columns + sorted(column_list)

    # The hard-coded sort has succeeded. Returning hard-coded sort.
    return starting_columns + desired_order