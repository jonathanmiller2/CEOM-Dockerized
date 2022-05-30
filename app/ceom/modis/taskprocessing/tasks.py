from celery import shared_task
from celery import states
import time
import random
import os, sys
import re, glob
import math
import datetime


from ceom.modis.taskprocessing import products, process, band_names, headers
from ceom.modis.taskprocessing.aux_functions import latlon2sin
from ceom.modis.taskprocessing.process import get_pixel_value,get_band_names,gap_fill
from ceom.modis.models import MODISSingleTimeSeriesJob
from ceom.modis.taskprocessing.headers import get_modis_header
from collections import OrderedDict

from celery import group
from django.conf import settings
from ceom.celery import app

def get_location_metadata(lat,lon,dataset,dataset_npix,years):
    ih, iv, xi, yi, folder = latlon2sin(float(lat), float(lon), dataset, dataset_npix)
    metadata = {
        'lat': lat,
        'lon': lon,
        'tile': 'h%02dv%02d' % (ih,iv),
        'dataset':dataset,
        'col':xi,
        'row':yi,
        'years':years
    }
    return metadata

def monitor_tasks(tasks,fun,metadata):
    MAX_ERRORS = 3
    MAX_SECONDS= 1000 # seconds
    TIME_CHECK = 1 # seconds
    NUM_STEPS = int(MAX_SECONDS/TIME_CHECK)

    for i in range(0,NUM_STEPS):
        num_tasks = 0
        finished = started = retry = error = pending = 0
        for year,chunks in tasks.items():
            for chunk, task in chunks.items():
                num_tasks+=1
                state = task.state
                finished += state=='SUCCESS' # When task finished
                started += state=='STARTED'  # When task is started
                retry += state=='RETRY'      # When task failed to send
                error +=  state=='FAILURE'   # Task had an error
                pending += state=='PENDING'  # Task is pending to be processed from the queue
                # if state==u'FAILURE':
                #     if curret_year_errors < MAX_ERRORS:
                #         tasks[year][day] =  get_modis_year_data.delay(ih, iv, xi, yi,folder,dataset,year,dataset_freq_in_days,vi,multi_day)
                #         num_errors[year][day] += 1
                #     elif not fatal_failures[year][day]:
                #         fatal_failures[year][day] = 1
                #         fatal_failures_counter+=1
        progress = int((float(finished + error)/num_tasks)*100)
        print(("Progress: %d Finished: %d Errors: %d Retry: %d Started %d Pending %d ") % (progress,finished, error, retry, started, pending))
        fun.update_state(state='STARTED',  meta={'completed': finished,'error':error,'total':num_tasks,'metadata':metadata})
        if finished + error == num_tasks:
            break
        time.sleep(TIME_CHECK)

def get_data(tasks):
    data = {}
    for year,chunks in tasks.items():
        data[year]={}
        for chunk, task in chunks.items():
            state = task.state
            if state!='SUCCESS':
                # data[year].update{''}
                # Should set to none or error the days of this tasks
                pass
            else:
                bands_dict={}

                for day, day_data_list in list(task.result[str(year)].items()):
                    if day_data_list:
                        bands_dict [day] = OrderedDict(day_data_list)
                    else:
                        bands_dict [day] = None
                data[year].update(bands_dict) #Merge the partial year dict into the global year dict
                task.forget() #Remove partial info from backend because it is no longer necessary

    return data
 
def send_tasks(function, params_dict):
    tasks =  {}
    for year,chunks in params_dict.items():
        tasks[year]={}
        for chunk, param_dict in chunks.items():
            tasks[year][chunk] = function(*[param_dict])
    return tasks

def split_tasks_in_chunks(years,metadata,dataset_freq_in_days,multi_day,num_chunks=5):
    task_params = dict([(year,{}) for year in years])
    current_year = datetime.datetime.now().year
    current_day = datetime.datetime.now().timetuple().tm_yday
    for year in years:
        days = [i+1 for i in range(0,366) if i % dataset_freq_in_days==0]
        if year not in list(range(2000,current_year+1)):
            continue
        if year == 2000:
            days = [day for day in days if day > 56 ] # Modis has no days before this date
        elif year == current_year:
            days = [day for day in days if day <= current_day ] # Cannot get future dates
        for day in days:
            chunk = ((day-1)/dataset_freq_in_days) % num_chunks
            if chunk not in task_params[year]:
                task_params[year][chunk] = {
                    'col' :     metadata['col'],
                    'row' :     metadata['row'],
                    'tile':     metadata['tile'],
                    'dataset':  metadata['dataset'],
                    'year':     year,
                    'dataset_freq_in_days': dataset_freq_in_days,
                    'multi_day': multi_day,
                    'days': [day,]
                }
            else:
                task_params[year][chunk]['days']+=[day]
    return task_params

def get_header(data,dataset):
    if dataset.upper()=='MOD09A1' or dataset.upper()=='MYD11A2':
        return get_modis_header(dataset,True)
    for year in data:
        for day in sorted(data[year]):
            if data[year][str(day)]:
                header=[]
                for band in data[year][str(day)]:
                    if band:
                        header+=[(band,band)]
                return header
    raise Exception ('Error getting header')

def save_data(data,full_path,task_id,metadata):
    full_dir = os.path.dirname(full_path)
    if not os.path.exists(full_dir):
        os.makedirs(full_dir)
    f = open(full_path,'w')
    header = get_header(data,metadata['dataset'])
    f.write(','.join([h[1] for h in header])+'\n')
    for year in data:
        for day in sorted([int(day) for day in data[year]]):
            if data[year][str(day)] and len(data[year][str(day)]) == len(header):   
                line=[]
                for x in range(0,len(header)):
                    if data[year][str(day)][header[x][0]]:
                        line+=[str(data[year][str(day)][header[x][0]])]
                f.write(','.join(line)+'\n')          
            else:
                current_date = datetime.date(int(year),1,1) + datetime.timedelta(int(day) - 1)
                current_date = current_date.strftime("%m/%d/%Y")
                current_line = [current_date] + ['NA' for x in range(1,len(header))]
                f.write(','.join(current_line)+'\n')
    f.close()
    return


@app.task(bind=True)
def get_modis_raw_data(self, media_root, csv_folder, lat,lon,dataset,years,dataset_npix,dataset_freq_in_days):
    # Get the list days we need to retreive its value, each one of
    # them will be send as an independent task to get their value
    time_ini = time.time() # Initial time to extract execution time
    metadata = get_location_metadata(lat,lon,dataset,dataset_npix,years) # metadata of the selected site
    # Set task initial state to started
    get_modis_raw_data.update_state(state=states.STARTED, meta={'completed': 0,'error':0,'total':0,'started':False,'metadata':metadata})
    num_tasks = len(years) # Number of tasks to perform
    multi_day = (int(dataset_freq_in_days)!=1)
    # Send all tasks to queue and store their queing id in a double dictionary (year-->day-->task_id) object
    params_lists = {}
    # Create parameter list for all years
    chunks = 12
    tasks_params = split_tasks_in_chunks(years,metadata,dataset_freq_in_days,multi_day,chunks)
    tasks = send_tasks(get_modis_year_data.delay,tasks_params)
    monitor_tasks(tasks,self,metadata)
    data = get_data(tasks)
    data = gap_fill(data,dataset)

    years = ",".join([str(year) for year in metadata['years']])
    filename = metadata['dataset']+"_lat_"+str(str(metadata['lat']))+"_lon_"+str(str(metadata['lon']))+'_years_'+years+'.csv'
    rel_path = os.path.join(csv_folder, filename)
    full_path = os.path.join(media_root, rel_path)

    save_data(data, full_path, get_modis_raw_data.request.id, metadata)

    job = MODISSingleTimeSeriesJob.objects.get(task_id=get_modis_raw_data.request.id)
    job.completed = True
    job.result.name = rel_path
    job.save()

    return {'filename':filename,'metadata':metadata,}

# ------------------------------------- PROCESSING SCRIPT PART ----------------------------

import multiprocessing as mp
def make_serializable_dict(mydict):
    serialized_dict = OrderedDict()
    for key,value in list(mydict.items()):
        serialized_dict[key] = str(value)
    return serialized_dict

def extract_day_data(col,row,dataset,year,day,tile):
    try:
        multi_day = True
        r = re.compile(".*A(?P<year>\d{4})(?P<day>\d{3}).*.hdf$")
        items = (dataset, year, tile, year, day)
        search = os.path.join(settings.MODIS_DATASETS_PATH, "%s/%d/%s/*%d%03d*.hdf" % items)
        flist = glob.glob(search)
        data = {}
        if len(flist) > 0 and r.match(flist[0]) is not None:
            fn = flist[0]
            pixel_values = None
            try:
                pixel_values = get_pixel_value(fn,col,row)
            except Exception as e:
                print(("Error retrieving pixel values for file: %s %s " % (fn,e)))
            
            if dataset.upper() == "MYD11A2":
                data = process.get_dates(pixel_values,year,day,False)
            else:
                data = process.get_dates(pixel_values,year,day,multi_day)
            if products.dataset_is_available(dataset):
                vegetation_indexes = products.get_vegetation_indexes(dataset,pixel_values)
                data = dict(list(data.items())+list(vegetation_indexes.items()))
            data = make_serializable_dict(data)
            data = [(k,v) for k,v in list(data.items()) ]
        else:
            data = None
        return data
    except Exception as e:
        print(("Exception at year %d day %d: %s" % (year,day,e)))
        return None

@app.task()
def get_modis_year_data(params_dict):
    p = params_dict
    results = {p['year']:{}}
    for day in p['days']:
        results[p['year']][day] = extract_day_data(p['col'],p['row'],p['dataset'],p['year'],day,p['tile'])
    return results

def terminate_task(task_id):
    app.control.revoke(task_id, terminate=True)
