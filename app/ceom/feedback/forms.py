#!/usr/bin/env python
from django import forms
from django.contrib.sites.models import Site

import ceom.feedback.models

class FeedbackForm(forms.ModelForm):
    '''The form shown when giving feedback'''
    '''Name = forms.CharField(label='Your name', max_length=100)
    Description = forms.CharField(widget=forms.Textarea)
    url = forms.URLField()'''
    class Meta:
        model = ceom.feedback.models.Feedback
        fields = ['url','site','subject', 'email', 'text','Priority','Photo']


class CommentForm(forms.ModelForm):
	'''This is the Comment Box Majorly Text'''
	class Meta:
		model = ceom.feedback.models.Comment
		fields = ['Comment_text']

class TrackStatusForm(forms.ModelForm):
    class Meta:
        model = ceom.feedback.models.Task_status
        fields = ['assigned_to','task_status']
# vim: et sw=4 sts=4
