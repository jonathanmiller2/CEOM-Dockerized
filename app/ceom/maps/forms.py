from django.forms import ModelForm
from django.db import models
from django import forms
from ceom.maps.models import map_gallery, Comment, poi, roi


class map_gallery_form(ModelForm):
    class Meta:
        model = map_gallery
        fields = ['title','description','map_image','map_image_legend','name_uploader','email']

class CommentForm(forms.ModelForm):
    '''This is the Comment Box Majorly Text'''
    class Meta:
        model = Comment
        fields = ['name_comment', 'Comment_text']


class PoiForm(forms.ModelForm):
    # FOr POI
    class Meta:
        model = poi
        fields = ['category', 'Attribute', 'lon', 'lat']

class roiForm(forms.ModelForm):
    # FOr POI
    class Meta:
        model = roi
        fields = ['lon', 'lat', 'tile', 'col', 'row', 'category', 'description', 'pixelsize', 'points']