from celery import Celery
from ceom.celery import app

@app.task
def add(x, y):
    inspect = app.control.inspect()
    print(inspect)
    print(inspect.scheduled())
    print(inspect.stats())
    print(inspect.report())
    print("THIS IS ADD")
    return x + y

@app.task(bind=True)
def get_modis_raw_data(self,csv_folder,media_base_url,lat,lon,dataset,years,dataset_npix,dataset_freq_in_days):
    print("FIND ME")
    # Get the list days we need to retreive its value, each one of
    # them will be send as an independent task to get their value
    time_ini = time.time() # Initial time to extract execution time
    metadata = get_location_metadata(lat,lon,dataset,dataset_npix,years) # metadata of the selected site
    # Set task initial state to started
    get_modis_raw_data.update_state(state=u'STARTED', meta={'completed': 0,'error':0,'total':0,'started':False,'metadata':metadata})
    num_tasks = len(years) # Number of tasks to perform
    multi_day = (int(dataset_freq_in_days)!=1)
    # Send all tasks to queue and store their queing id in a double dictionary (year-->day-->task_id) object
    params_lists = {}
    # Create parameter list for all years
    chunks = 12
    tasks_params = split_tasks_in_chunks(years,metadata,dataset_freq_in_days,multi_day,chunks)
    print("Sending tasks to queue:")
    tasks = send_tasks(get_modis_year_data.delay,tasks_params)
    print("Monitoring tasks")
    monitor_tasks(tasks,self,metadata)
    data  = get_data(tasks)
    print("Processing data")
    data = process_data(data,dataset)
    print("saving data")
    filename = save_data(data,csv_folder,get_modis_raw_data.request.id,metadata)
    try:
        db = database.pgDatabase()
        db.updateCompletedSingleTimeSeriestask(get_modis_raw_data.request.id,os.path.join(media_base_url,filename),)
    except Exception as e:
        print("Error : %s") % e.message
        pass
    return {'filename':filename,'metadata':metadata,}