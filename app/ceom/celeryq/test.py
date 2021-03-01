from .tasks import get_modis_raw_data

# lat =  42.587495
# lon = -104.828119
# dataset= 'mod09a1'
# years = [year for year in range (2001,2014)]
# vi = True
# dataset_npix = 2400
# pixel_val = []
# for i in range(0,1):
#     pixel_val.append(get_modis_raw_data.delay(lat,lon,dataset,years,dataset_npix,vi))

# while True:
#     for i in range(0,1):
#         print pixel_val[i].result
task_id = '6b997fef-5bb7-4141-99cd-4899c1ccb176'
result = get_modis_raw_data.AsyncResult(task_id)
print(result.result)