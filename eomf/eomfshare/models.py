from django.db import models

# Create your models here.
class uploadfile(models.Model):
	FileNew = models.FileField(upload_to = 'media/eomfshare')