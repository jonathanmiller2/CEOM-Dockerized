from django.contrib import admin
from ceom.feedback.models import Feedback, Comment

#admin.site.register(Feedback)

class CommentInline(admin.TabularInline):
	model = Comment

class FeedbackAdmin(admin.ModelAdmin):
	inlines = [
		CommentInline,
	]

admin.site.register(Feedback, FeedbackAdmin)
# vim: et sw=4 sts=4
