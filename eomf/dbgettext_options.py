from dbgettext.registry import registry, Options
from dbgettext.lexicons import html
from aboutus.models import Post, Group, Person
from workshops.models import Workshop,WorkshopClass
from photos.models import Category as PhotoCategory

# PHOTOS
class PhotoCategoryOptions(Options):
    attributes = ('name',)

registry.register(PhotoCategory, PhotoCategoryOptions)

# ABOUTUS
class PostOptions(Options):
    attributes = ('title',)
    parsed_attributes = {'content': html.lexicon}

registry.register(Post, PostOptions)

class PersonOptions(Options):
    attributes = ('title',)

registry.register(Person, PersonOptions)

class GroupOptions(Options):
    attributes = ('name',)

registry.register(Group, GroupOptions)


# WORKSHOPS
class WorkshopOptions(Options):
    attributes = ('name','description')
    # parsed_attributes = {'content': html.lexicon}

registry.register(Workshop, WorkshopOptions)

class WorkshopClassOptions(Options):
    attributes = ('name',)

registry.register(WorkshopClass, WorkshopClassOptions)
