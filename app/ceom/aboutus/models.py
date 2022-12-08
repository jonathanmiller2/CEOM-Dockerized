from django.db import models
import datetime
from django.core import validators
from django.core.exceptions import ValidationError
from time import strptime
from django.utils.translation import ugettext_lazy as _
# Create your models here.
NUM_COLUMNS = (
    ("1", _("One column image")),
    ("2", _("Two columns image")),
)
YEAR_INPUT_FORMATS = (
    '%Y',
)

class YearField(models.CharField):
    default_error_messages = {
        'invalid': ('Enter a valid year'),
    }

    def __init__(self, input_formats=None, *args, **kwargs):
        super(YearField, self).__init__(*args, **kwargs)
        self.input_formats = input_formats

    def clean(self, value,x):
        if value in validators.EMPTY_VALUES:
            return None
        if isinstance(value, datetime.datetime):
            return format(value, '%Y')
        if isinstance(value, datetime.date):
            return format(value, '%Y')
        for fmt in YEAR_INPUT_FORMATS:
            try:
                date = datetime.date(*strptime(value, fmt)[:3])
                return format(date, '%Y')
            except ValueError:
                continue
        raise ValidationError(self.error_messages['invalid'])

class Post(models.Model):
    title =models.TextField("Post Title",null=False, blank=False,)
    date = models.DateField("date", null=False)
    content = models.TextField("Content",null=False, blank=False,)
    image_column_number = models.CharField(" column images",max_length=1, choices=NUM_COLUMNS, default="1")
    def __str__(self):
        return self.date.strftime('%Y-%M-%D') + " [" + self.title + "]"

class PostImage(models.Model):
    description = models.CharField("Description", max_length=100)
    post = models.ForeignKey(Post, related_name="images", null=False, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(null=False)
    image = models.ImageField(null=True, upload_to="news")
   
    #We want the order for each image to be unique at the posts
    class Meta:
        unique_together = ('post', 'order')
    def __str__(self):
        return "Image  " + str(self.order) + ": " + str(self.post) 

class Category(models.Model):
    name = models.CharField(max_length=125)
    order = models.IntegerField()
    description = models.CharField(max_length=1000, null=True, blank=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "categories"


class Person(models.Model):
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=250, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    date = models.DateField('date published', null=True)
    headshot = models.ImageField(null=True, blank=True, upload_to='people/')
    order = models.IntegerField(null=False, default=9999)
    def __str__(self):
        return '%s %s %s' % (self.first_name, self.middle_name, self.last_name)
    class Meta:
        unique_together = ('first_name', 'middle_name','last_name')

class GalleryPhoto(models.Model):
    year = YearField(null=False, max_length=4,)
    order= models.IntegerField(null=False)
    title = models.CharField("Title", max_length=100)
    description = models.TextField("Description",null=True, blank=True,)
    picture = models.ImageField(null=False, upload_to='aboutus/group_photos/photos')
    
    #We want the order for each image and its order to be unique
    class Meta:
        unique_together = ('year', 'order')
    def __str__(self):
        return str(self.year) + "("+str(self.order)+"): " + self.title
        
PUBLICATION_CHOICES = (
    ('jour', 'Journal'),
    ('chap', 'Book and Book Chapters'),
    ('post', 'Posters'),
    ('pres', 'Presentations'),
)

class Publication(models.Model):
    pubtype = models.CharField(max_length=4, choices=PUBLICATION_CHOICES, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    authorship = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=250, null=True, blank=True)

    link = models.CharField(max_length=250, null=True, blank=True)
    file = models.FileField(upload_to="docs/upload", null=True, blank=True)
    date = models.DateField('date published', null=True)
    journal = models.CharField(max_length=125, null=True, blank=True)
    content = models.TextField(null=True, blank=True)

    venue = models.CharField(max_length=250, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    #Journal
    volume = models.CharField(max_length=56,null=True, blank=True)
    issue = models.CharField(max_length=56, null=True, blank=True)
    pages = models.CharField(max_length=56, null=True, blank=True)
    #Book
    editors = models.CharField(max_length=128, null=True, blank=True)
    book_title = models.CharField(max_length=128, null=True, blank=True)
    publisher = models.CharField(max_length=128, null=True, blank=True)

    issn = models.CharField(max_length=56, null=True, blank=True)
    doi = models.CharField(max_length=56, null=True, blank=True)
    keywords = models.TextField(null=True, blank=True)
    abstract = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title



# Gross and Net Primary Production -- Vegetation Photosynthesis Model (VPM)
# Agro-Ecosystem, Agriculture and Irrigation
# Forest Ecosystem and Forestry
# Land Cover and Land Use Change
# Biochemical and Biophysical Parameters -- Chlorophyll, Nitrogen and Leaf Area Index
# Land Surface Phenology
# Snow Cover
# Water fluxes and hydrology
# Infectious Disease Ecology, Epidemiology, and Global Health