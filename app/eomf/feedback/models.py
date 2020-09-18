from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth.models import User

class Feedback(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    url = models.CharField(max_length=255)
    subject = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=False, null=True)
    text = models.TextField()
    Photo = models.ImageField(upload_to = 'media/feedback', blank=True, null=True, default = 'media/feedback/image5.jpg')
    BUG_URGENT = 'BU'
    BUG_NOT_URGENT = 'BNU'
    FEATURE = 'FT'
    UI_CHANGE_URGENT = 'UX'
    type_ofbug_choices = (
    	(BUG_URGENT, 'Bug_urgent'),
    	(BUG_NOT_URGENT, 'Bug_not_urgent'),
    	(FEATURE, 'New feature'),
    	(UI_CHANGE_URGENT, 'UX_urgent'),
    	)
    Priority = models.CharField(max_length=3,choices=type_ofbug_choices, default=BUG_NOT_URGENT)
    feedback_date = models.DateField(auto_now=True)
    #Feedback_user = models.ForeignKey(User, blank=True, null=True)

    def __str__(self):
        return u'%s: %s' % (self.url, self.subject)

class Comment(models.Model):
	Comment_id = models.ForeignKey(Feedback, related_name='comment', on_delete=models.CASCADE)
	# Comment_user = models.ForeignKey(User)
	Comment_text = models.TextField(null=False, blank=True)

	def __str__ (self):
		return self.Comment_text


class Task_status(models.Model):
	feedback_track = models.OneToOneField(Feedback, primary_key=True, related_name='stats', on_delete=models.CASCADE)
	Bhargav_Kumar_Reddy_Bolla = 'BR'
	Xibei_jia = 'XJ'
	developer_choices = ((Bhargav_Kumar_Reddy_Bolla, 'Bhargav Bolla'),
		(Xibei_jia, 'Xibei Jia'))
	assigned_to = models.CharField(max_length=2, choices=developer_choices, default=Xibei_jia)
	Done = 'CO'
	Working = 'WR'
	NEW = 'NW'
	Need_more_information = 'NM'
	track_choices = ((Done, 'done'),
		(Working, 'working'),
		(Need_more_information, 'need more info'),
		(NEW, 'New'))
	task_status = models.CharField(max_length=2, choices=track_choices,default=NEW)

	def __str__ (self):
		return self.task_status



# Create your models here.
