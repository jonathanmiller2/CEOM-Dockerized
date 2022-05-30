The MODIS directory for this website is split into two sub-directories, inventory and visualization.
I have no idea why it was constructed this way.

Furthermore, the relevant celery tasks for this modis directory are not located anywhere in ceom/modis.
Rather, they are located in ceom/celeryq/modis.
I also have no idea why that was constructed that way.

An active #TODO: is to merge these two folders, prune the unnescessary celery tasks, and move the core modis tasks to the ceom/modis directory.