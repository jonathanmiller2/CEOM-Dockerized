from osgeo import gdal
from datetime import datetime, timedelta
import itertools, csv, os, math
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
        lon = ((360 / 1440) * float(x) - 180) + 0.125
        lat = (-(180 / 720) * float(y) + 90) - 0.125
        filename = 'TROPOMI_lat_{:.3f}_lon_{:.3f}'.format(lat, lon) + "_" + "_".join(years) + ".csv"
        rel_file = os.path.join(csv_folder, filename)
        full_file = os.path.join(media_root, rel_file)
        nineteen_seventy = datetime.fromisoformat('1970-01-01')

        os.makedirs(os.path.join(media_root, csv_folder, exist_ok=True))
        
        columns = []
        data = []

        for year_index in range(len(years)):
            data_file_location = TROPOMIYearFile.objects.get(year=years[year_index]).location
            ds = gdal.Open(data_file_location)
            subdatasets = ds.GetSubDatasets()

            for i in range(len(subdatasets)):
                subdataset_name = subdatasets[i][0].split(':')[2]
                if subdataset_name not in columns:
                    columns.append(subdataset_name)
            
            columns = sort_columns(columns)

            file_df = pd.DataFrame(columns=columns)
            file_df.rename_axis('date', inplace=True)
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
                
                new_dates_df = pd.DataFrame(fill_value, index=new_dates, columns=columns)
                new_dates_df.index = pd.to_datetime(new_dates_df.index)
                file_df = pd.concat([file_df, new_dates_df])

                # Measurements are packed in a (46,1,1)D triple-list, need to collapse down into (46,)D single list
                subds_data = list(itertools.chain.from_iterable(itertools.chain.from_iterable(measurement_data)))
                file_df[subdataset_name] = subds_data

            data.append(file_df)
            
        final_df = pd.concat(data)
        final_df.rename_axis('Date', inplace=True)

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
def process_TROPOMI_multiple_site(self, media_root, csv_folder, input_file, years, userid):
    job_obj = TROPOMIMultipleTimeSeriesJob.objects.get(task_id=self.request.id)
    job_obj.percent_complete = 0
    job_obj.working = True
    job_obj.save()

    try:
        filename = 'TROPOMI_Output_uid' + str(userid) + "_" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".csv"
        rel_file = os.path.join(csv_folder, filename)
        full_file = os.path.join(media_root, rel_file)
        nineteen_seventy = datetime.fromisoformat('1970-01-01')

        if not os.path.exists(os.path.join(media_root, csv_folder)):
            os.makedirs(os.path.join(media_root, csv_folder))
        
        columns = ['site']
        data = []
        locations = []

        # Populate locations list
        with open(os.path.join(media_root, input_file)) as input_file:
            reader = csv.reader(input_file, delimiter=',')
            
            for row in reader:
                site_id = int(row[0])
                lat = float(row[1])
                lon = float(row[2])

                x = math.floor(((lon + 180) * 1440) / 360)
                y = math.floor(((-lat + 90) * 720) / 180)

                locations.append((site_id, x, y))
        
        # Start requesting data for each year
        for year_index in range(len(years)):
            data_file_location = TROPOMIYearFile.objects.get(year=years[year_index]).location
            ds = gdal.Open(data_file_location)
            subdatasets = ds.GetSubDatasets()

            # Populate header list if new file has any new headers
            for i in range(len(subdatasets)):
                subdataset_name = subdatasets[i][0].split(':')[2]
                if subdataset_name not in columns:
                    columns.append(subdataset_name)
            
            columns = sort_columns(columns)

            # Set up site dataframes for this year
            file_dfs = [] 
            for i in range(len(locations)):
                file_dfs.append(pd.DataFrame(columns=columns))
                file_dfs[i].rename_axis('date', inplace=True)
                file_dfs[i].index = pd.to_datetime(file_dfs[i].index)

            # Fill in dataframes
            for i in range(len(subdatasets)):
                subdataset_name = subdatasets[i][0].split(':')[2]
                measurement_ds = gdal.Open(subdatasets[i][0])

                # Update job progress on Django object
                year_starting_percent = year_index / len(years)
                year_ending_percent = (year_index+1) / len(years)
                year_current_percent = (i+1) / len(subdatasets)
                job_obj.percent_complete = (1-year_current_percent) * year_starting_percent + year_current_percent * year_ending_percent
                job_obj.save()

                # Get fill value for missing data from metadata (defaults to -9999)
                metadata = measurement_ds.GetMetadata_Dict()
                metadata_dates = metadata['NETCDF_DIM_time_VALUES'].strip('{}').split(',')
                fill_value = metadata.get(subdataset_name + '#_FillValue', -9999)

                # Populate list of new dates found in subdataset
                new_dates = []
                for d in metadata_dates:
                    row_date = nineteen_seventy + timedelta(days=int(d))
                    is_new = False
                    for file_df in file_dfs:
                        if row_date not in file_df.index.array:
                            is_new = True
                            break
                    if is_new:        
                        new_dates.append(row_date)
                
                # Set up blank rows in our file dataframes for all the new dates found
                new_dates_df = pd.DataFrame(fill_value, index=new_dates, columns=columns)
                new_dates_df.index = pd.to_datetime(new_dates_df.index)
                for i in range(len(file_dfs)):
                    file_dfs[i] = pd.concat([file_dfs[i], new_dates_df])

                # Request specific pixel data for each site
                for i in range(len(locations)):
                    site_id = locations[i][0]
                    x = locations[i][1]
                    y = locations[i][2]
                    
                    measurement_data = measurement_ds.ReadAsArray(int(x), int(y), 1, 1)
                
                    # Measurements are packed in a (46,1,1)D triple-list, need to collapse down into (46,)D single list
                    subds_data = list(itertools.chain.from_iterable(itertools.chain.from_iterable(measurement_data)))
                    file_dfs[i][subdataset_name] = subds_data

            # Set site id column for all of this year's dataframes
            for i in range(len(locations)):
                file_dfs[i] = file_dfs[i].assign(site=locations[i][0])
            
            # Store away all of this year's dataframes
            data.extend(file_dfs)
            
        final_df = pd.concat(data)
        final_df = final_df.rename_axis('date').sort_values(by=['site', 'date'])

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


def sort_columns(column_list):
    starting_columns = []

    if 'site' in column_list:
        starting_columns.append('site') 
        column_list.remove('site') 

    desired_order = ['Mean_TOA_RAD_743',
                    'SIF_743',
                    'SIF_Corr_743',
                    'REF_665',
                    'REF_781',
                    'NDVI',
                    'NIRv',
                    'NIRv_Rad',
                    'cloud_fraction_L2',
                    'Mean_TOA_RAD_743_std',
                    'SIF_743_std',
                    'SIF_Corr_743_std',
                    'SIF_ERROR_743',
                    'SIF_ERROR_743_std',
                    'REF_665_std',
                    'REF_781_std',
                    'NDVI_std',
                    'NIRv_std',
                    'NIRv_Rad_std',
                    'cloud_fraction_L2_std',
                    'n']

    for item in desired_order:
        if item not in column_list:
            print("Sorting columns for TROPOMI task failed, item: " + item + " not found in column list.")
            
            # The hard-coded sort has failed. Returning alphabetical order.
            return starting_columns + sorted(column_list)

    # The hard-coded sort has succeeded. Returning hard-coded sort.
    return starting_columns + desired_order