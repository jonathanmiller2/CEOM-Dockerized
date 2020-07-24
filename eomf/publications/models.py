from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=125)

    def __unicode__(self):
        return self.name


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

    def __unicode__(self):
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
