from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from ceom.projects.models import Project

def index(request):
    project = Project.objects.all().extra(select={'null_start': "end_date is null"},order_by=['null_start', '-end_date'])
	#wrote extra in above queryset for putting NULL values to the last in the list.
    
    return render_to_response(
        'projects/projects.html',
        {
            'project': project
        },
        context_instance = RequestContext(request)
    )
    
    