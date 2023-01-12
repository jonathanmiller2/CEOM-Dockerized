This README relates to tasks.py, and how the MODIS single-site and multi-site timeseries requests are handled.
Written by Jonathan Miller, 12/31/2022

The initial idea was relatively simple. The view starts a celery task and redirects to a status page, the
celery task slowly writes out a CSV, you get the CSV from the status page.

That design was functional, but was a little too slow to be usable. It took 2m45s per year requested.
Most of this time was spent waiting on IO as osgeo/GDAL took forever to load the .hdf file into memory.

So, I needed to optimize. The obvious approach would be leverage celery to further parallelize the process.
The process involved reading in about 50 files per year requested, and so the idea was that each file read
could be broken out into an individual tiny subtask, and then celery could intelligently handle all of 
those subtasks in it's internal queue.

The design was to keep the central celery task that manages the CSV stuff and all of the stuff
with managing the associated database object, but instead of doing the actual osgeo/GDAL reads, it would
just set up a bunch of subtask, and then wait for Celery to chew through those subtasks.

I whipped up this design and was immediately yelled at by Celery. Apparently, Celery noticed that I was
"Launching synchronous subtasks" and immediately errored out, directing me a doc page on the subject.
(At time of writing: https://docs.celeryq.dev/en/stable/userguide/tasks.html#avoid-launching-synchronous-subtasks)

So, new design. This time I am going to do what Celery says and no longer have a central task, but instead
have a driver function that calls a chain. It will be terrible, complex, and messy, but my hands are tied.