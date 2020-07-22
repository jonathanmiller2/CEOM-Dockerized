from django.db import models

class Project(models.Model):
    project_title = models.CharField(max_length=250)
    funding_agency = models.CharField(max_length=250, null=True, blank=True)
    start_date = models.DateField('project start date', null=True, blank=True)
    end_date = models.DateField('project end date', null=True, blank=True)
    fund = models.IntegerField('total amount of fund', null=True, blank=True)

    def __unicode__(self):
        return self.project_title
