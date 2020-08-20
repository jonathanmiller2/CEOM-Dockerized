from .celery import app as celery_app

__all__ = ("celery_app",)

from django.contrib.flatpages.models import FlatPage

p = FlatPage.objects.create(url="/", title="home", content="<div class=\"slideshow\">&nbsp;&nbsp;&nbsp;<img src=\"/media/images/Splash/1.png\">&nbsp;&nbsp;&nbsp; <img src=\"/media/images/Splash/2.png\" >&nbsp;&nbsp;&nbsp; <img src=\"/media/images/Splash/3.png\" >&nbsp;&nbsp;&nbsp; <img src=\"/media/images/Splash/4.png\" >&nbsp;&nbsp;&nbsp; <img src=\"/media/images/Splash/5.png\" >&nbsp;&nbsp;&nbsp; <img src=\"/media/images/Splash/6.png\" ></div>", enable_comments=false, template_name="home.html", registration_required=false)
