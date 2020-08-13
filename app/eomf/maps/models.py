from django.db import models

# Create your models here.
from django.contrib.auth.models import User

import time
import csv

import json
from django.core.exceptions import ValidationError
from django import forms

#Category model from photos
from eomf.photos.models import Category


class roi(models.Model):
	#to save rois collected
	#maps_roi : table name in DB
	lon = models.FloatField(blank=False, null=False)
	lat = models.FloatField(blank=False, null=False)
	user =  models.ForeignKey(User, null=False, blank=False, default=1096, on_delete=models.CASCADE)
	tile = models.CharField(max_length=6,blank=True, null=True)
	image = models.ImageField(upload_to = 'media/roi', blank=True, null=True, default = 'media/feedback/image5.jpg')#this image5 says " Image unavailable"
	score = models.IntegerField(blank=True, null=True)
	description = models.TextField()
	classification = models.CharField(max_length=255,blank=True, null=True)
	created = models.DateTimeField('created', auto_now_add=True)
	modified = models.DateTimeField('modified', auto_now=True)
	pixelsize = models.IntegerField(blank=False, null=False)
	col = models.IntegerField(blank=True, null=True)
	row = models.IntegerField(blank=True, null=True)
	category = models.ForeignKey(Category, null=True, blank=True, db_column='categoryid', related_name='rois', on_delete=models.CASCADE)
	# Region as a collection of points
	# For now considering region will always be a rectangle! improve later to support any polygon
	# Get it as a string and parse it later.
	points = models.TextField()


	def __unicode__(self):
		return str(self.user)+' ['+str(self.created)+']'


class poi(models.Model):
	#to save rois collected
	#maps_roi : table name in DB
	lon = models.FloatField(blank=False, null=False)
	lat = models.FloatField(blank=False, null=False)
	user =  models.ForeignKey(User, null=False, blank=False, default=1829, on_delete=models.CASCADE)
	score = models.IntegerField(blank=True, null=True)
	Attribute = models.TextField(blank=False, null=False, verbose_name="Attributes")
	classification = models.CharField(max_length=500,blank=True, null=True, verbose_name="Site Category")
	created = models.DateTimeField('created', auto_now_add=True)
	modified = models.DateTimeField('modified', auto_now=True)
	category = models.ForeignKey(Category, null=True, blank=True, db_column='categoryid', related_name='pois', on_delete=models.CASCADE)
	# pixelsize = models.IntegerField(blank=False, null=False)

	def __unicode__(self):
		return str(self.user)+' ['+str(self.created)+']'


class map_gallery(models.Model):
	#To save the uploaded map 
	map_image = models.ImageField(upload_to = 'media/map_gallery', verbose_name = "Upload Map", blank=False, null=False, default = 'media/feedback/image5.jpg')#Image not available.
	user = models.ForeignKey(User, null=False, blank=False, default=1829, on_delete=models.CASCADE)
	email = models.EmailField(blank=False,verbose_name = "Email",  null=True)
	description = models.TextField(null=False,verbose_name = "Description",  blank=False)
	title = models.CharField(max_length=3000, verbose_name = "Title of your map", blank=False, null=False)
	name_uploader = models.CharField(max_length=3000, verbose_name = "Your Name", blank=False, null=False)
	created = models.DateTimeField('created', auto_now_add=True)
	modified = models.DateTimeField('modified', auto_now=True)
	validated = models.BooleanField()# for consent or for validation in admin page.
	map_image_legend = models.ImageField(upload_to = 'media/map_gallery', verbose_name = "Legend", blank=False, null=False, default = 'media/feedback/image5.jpg')#Image not available.

	def __unicode__(self):
		return str(self.user)+' : '+str(self.title)+'| |'


class Comment(models.Model):
	Comment_id = models.ForeignKey(map_gallery, related_name='comment', on_delete=models.CASCADE)
	name_comment = models.CharField(max_length=3000, verbose_name = "Your Name", blank=False, null=False)
	Comment_text = models.TextField(null=False, verbose_name = "Enter Comment here", blank=False)
	created = models.DateTimeField('created', auto_now_add=True)
	
	def __unicode__ (self):
		return self.Comment_text