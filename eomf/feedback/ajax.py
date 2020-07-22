from eomf.feedback.models import Task_status, Feedback, Comment
import json
from dajaxice.decorators import dajaxice_register
from django.core.mail import send_mail

@dajaxice_register(method='GET')
def updateDB(request,feed_id,new_val,aors):
	if aors == 1:
		x = Task_status.objects.get(feedback_track = Feedback.objects.get(id=feed_id))
		x.assigned_to = new_val
		x.save()
		# v = Task_status(feedback_track = Feedback.objects.get(id=feed_id),assigned_to = new_val)
		# v.save()
		return json.dumps({'message':"Success"})
	elif aors == 2:
		x = Task_status.objects.get(feedback_track = Feedback.objects.get(id=feed_id))
		x.task_status = new_val
		x.save()
		# v = Task_status(feedback_track = Feedback.objects.get(id=feed_id),task_status = new_val)
		# v.save()
		return json.dumps({'message':"Success"})
	else:
		return json.dumps({'message':"Failure"})


@dajaxice_register(method='GET')
def updateComment(request,feed_id,new_val):
	x = Comment(Comment_id = Feedback.objects.get(id=feed_id),Comment_text = new_val)
	x.save()
	send_mail('New Comment added!', 'Form_id : '+str(x.Comment_id.id)+'\n'+'Details: '+'\n'+'subject:'+str(x.Comment_id.subject)+'\n'+'Comment : '+str(x.Comment_text)+'\n'+'Link : '+'eomf.ou.edu/feedback/comment/'+str(x.Comment_id.id)+'\n', 'admin@eomf.ou.edu', ['bhargavreddy.bolla@ou.edu','bhargavreddy.bolla@gmail.com','Xibei.Jia-1@ou.edu'], fail_silently=True)
	return json.dumps({'message':"Success"})




