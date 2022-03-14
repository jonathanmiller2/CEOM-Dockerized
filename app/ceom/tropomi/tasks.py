from django.core.files import File

from osgeo import gdal
from datetime import datetime, date, timedelta
import itertools, csv, os
import pandas as pd

from ceom.celery import app
from ceom.tropomi.models import *

@app.task(bind=True)
def process_TROPOMI_single_site(self, media_root, csv_folder, x, y, years):
    job_obj = TROPOMISingleTimeSeriesJob.objects.get(task_id=self.request.id)
    job_obj.percent_complete = 0
    job_obj.working = True
    job_obj.save()

    try:
        rel_file = os.path.join(csv_folder, 'TROPOMI_x' + x + "_y" + y + "_" + "_".join(years) + ".csv")
        full_file = os.path.join(media_root, rel_file)
        nineteen_seventy = datetime.fromisoformat('1970-01-01')

        if not os.path.exists(csv_folder):
            os.makedirs(csv_folder)
        
        headers = ['date']
        data = []

        for year_index in range(len(years)):
            data_file_location = TROPOMIYearFile.objects.get(year=years[year_index]).location
            ds = gdal.Open(data_file_location)
            subdatasets = ds.GetSubDatasets()

            for i in range(len(subdatasets)):
                subdataset_name = subdatasets[i][0].split(':')[2]
                if subdataset_name not in headers:
                    headers.append(subdataset_name)

            file_df = pd.DataFrame(columns=headers)
            file_df.set_index('date', inplace=True)
            file_df.index = pd.to_datetime(file_df.index)

            for i in range(len(subdatasets)):
                subdataset_name = subdatasets[i][0].split(':')[2]
                measurement_ds = gdal.Open(subdatasets[i][0])
                measurement_data = measurement_ds.ReadAsArray(int(x), int(y), 1, 1)

                year_starting_percent = year_index / len(years)
                year_ending_percent = (year_index+1) / len(years)
                year_current_percent = (i+1) / len(subdatasets)
                job_obj.percent_complete = (1-year_current_percent) * year_starting_percent + year_current_percent * year_ending_percent
                job_obj.save()

                metadata = measurement_ds.GetMetadata_Dict()
                metadata_dates = metadata['NETCDF_DIM_time_VALUES'].strip('{}').split(',')
                fill_value = metadata.get(subdataset_name + '#_FillValue', -9999)

                new_dates = []

                for d in metadata_dates:
                    row_date = nineteen_seventy + timedelta(days=int(d))

                    if row_date not in file_df.index.array:
                        new_dates.append(row_date)
                
                new_dates_df = pd.DataFrame(fill_value, index=new_dates, columns=headers[1:])
                #new_dates_df.set_index('date', inplace=True)
                new_dates_df.index = pd.to_datetime(new_dates_df.index)
                file_df = pd.concat([file_df, new_dates_df])

                # Measurements are packed in a (46,1,1)D triple-list, need to collapse down into (46,)D single list
                subds_data = list(itertools.chain.from_iterable(itertools.chain.from_iterable(measurement_data)))
                file_df[subdataset_name] = subds_data

            data.append(file_df)
            
        final_df = pd.concat(data)

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
def process_TROPOMI_multiple_site(self, csv_folder, input_file, years):
    pass