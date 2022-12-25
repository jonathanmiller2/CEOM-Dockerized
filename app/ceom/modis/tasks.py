from ceom.celery import app

@app.task(bind=True)
def process_MODIS_single_site(self, media_root, csv_folder, dataset, h, v, x, y, years):
    # I probably need to pass the dataset too
    pass


@app.task(bind=True)
def process_MODIS_multiple_site(self, media_root, csv_folder, dataset, input_file, years, userid):
    pass