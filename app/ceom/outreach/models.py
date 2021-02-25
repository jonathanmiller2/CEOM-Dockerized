from django.db import models
from django.contrib.auth.models import User
from tinymce import models as tinymce_models
from django.contrib.gis.db import models
from phonenumber_field.modelfields import PhoneNumberField as InternationalPhone


CHOICES = (
    ("U", "University / Non-Profit"),
    ("P", "Private industry / For Profit"),
)

SIZES = (
    ("UK", "Unkown"),
    ("S", "Small"),
    ("M", "Medium"),
    ("L", "Large"),
    ("XL", "Extra Large"),
    ("2XL", "Extra Extra Large"),
)

class Sponsor(models.Model):
    name = models.CharField(max_length=160, null=True, blank=True)
    contact_person_name = models.CharField(max_length=160, null=True, blank=True)
    contact_person_phone = models.CharField(max_length=15, null=True, blank=True)
    contact_person_mail = models.CharField(max_length=160, null=True, blank=True)
    link=models.CharField(max_length=300, null=True, blank=True)
    
    logo = models.FileField(null=False, max_length=300,upload_to="outreach/sponsors/")

    def __str__(self):
        return str(self.name)
    
    class Meta:
        unique_together = (('name',),)

class Year(models.Model):
    date = models.DateField(null=False,blank=False)
    registration_closed=models.BooleanField(default=False)
    address = models.CharField(null=True, blank=True,max_length = 300)
    hidden = models.BooleanField(default=False)
    time_ini= models.TimeField(null=False, blank=False)
    time_end= models.TimeField(null=False, blank=False)
    summary_hidden = models.BooleanField(default=True)
    agenda_hidden = models.BooleanField(default=True)
    photo_contest_hidden = models.BooleanField(default=True)
    poster_contest_hidden = models.BooleanField(default=True)
    image_gallery_hidden = models.BooleanField(default=True)
    photo_gallery_hidden = models.BooleanField(default=True)
    facebook_link =  models.CharField(null=True, blank=True,max_length = 300)
    twitter_link =  models.CharField(null=True, blank=True,max_length = 300)
    survey_open = models.BooleanField(default=True)
    def __str__(self):
        return str(self.date)
class Booth(models.Model):
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    non_profit = models.BooleanField()
    institution = models.CharField(max_length=128)
    department = models.CharField(max_length=128)
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    address_1 = models.CharField(max_length=128)
    address_2 = models.CharField(null=True, blank=True, max_length=128)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    zipcode = models.CharField(max_length=30)
    phone = models.CharField(max_length=30)
    email = models.EmailField(max_length=60)
    names = models.TextField("Aditional atendees",  null=True, blank=True)
    permits = models.CharField("No. of parking permits needed", null=True, blank=True, max_length=128)
    oversized = models.NullBooleanField("Do you have a oversized exhibit or display?", null=True, blank=True)
    comment = models.TextField(
        "Questions & comments", null=True, blank=True,
    )
    tshirt_size_1 = models.CharField(
        max_length=3, choices=SIZES,
    )
    tshirt_size_2 = models.CharField(max_length=3, choices=SIZES)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    validated = models.BooleanField()

    def __str__(self):
        return str(self.last_name + ", "+self.first_name)
    
    class Meta:
       unique_together = (("year","institution","department"),)

    def obf_email(self):
        email = str(self.email)
        nick, domain = email.split('@')
        return nick[:-4]+"****@"+domain


class Visitor(models.Model):
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=30)
    institution = models.CharField(max_length=100)
    comment = models.TextField(
        "Questions & comments",null=True, blank=True,
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    validated = models.BooleanField()

    class Meta:
       unique_together = (("year","email"),)
    def __str__(self):
        return self.first_name + " " + self.last_name


class PhotoContestParticipant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    last_name = models.CharField("Last name", max_length=50)
    first_name = models.CharField("First name", max_length=50)
    email = models.EmailField("email", max_length=60)
    comment = models.TextField(
        "Questions & comments",null=True, blank=True,
    )
    validated = models.BooleanField()

    def __str__(self):
        return self.first_name + " " + self.last_name

class PosterCategory(models.Model):
    name = models.CharField(max_length=100,null=False)
    description = models.CharField(max_length=200,null=False)
    def __str__(self):
        return self.name 
class Poster(models.Model):
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    institution = models.CharField(max_length=128)
    department = models.CharField(max_length=128)
    category = models.ForeignKey(PosterCategory,null=False, on_delete=models.CASCADE)
    email = models.EmailField(max_length=30)
    title = models.CharField(max_length=200)
    authors = models.TextField("Poster author list",null=True, blank=True)
    abstract = models.TextField("Poster abstract",null=False, blank=False)
    comment = models.TextField(
        "Questions & comments",null=True, blank=True,
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    validated = models.BooleanField()
    preview = models.FileField(null=True, max_length=300,upload_to="outreach/posters/", blank=True)

    def __str__(self):
        return self.first_name + " " + self.last_name
    class Meta:
       unique_together = (("year","email"),)

class AboutUsGroup(models.Model):
    name = models.CharField(max_length=125)
    order = models.IntegerField(null=False)
    
    def __str__(self):
        return self.name

class AboutUsPerson(models.Model):
    first_name = models.CharField(max_length=100, null=True, blank=True)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=16, null=True, blank=True)
    headshot = models.ImageField(null=True, upload_to='outreach/aboutus/', default='outreach/aboutus/dummy_headshot222.jpg')

    def __str__(self):
        return '%s %s %s' % (self.first_name, self.middle_name, self.last_name)

class PersonInGroup(models.Model):
    group = models.ForeignKey(AboutUsGroup, related_name="pvsgInGroup", on_delete=models.CASCADE)
    person = models.ForeignKey(AboutUsPerson, related_name="pvsgInPerson", on_delete=models.CASCADE)
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    highlight = models.BooleanField(default=False)

class SponsorCategory(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    min_inversion = models.IntegerField(null=False)
    max_inversion = models.IntegerField(null=False)
    logo = models.ImageField(null=True, upload_to='outreach/sponsors/')
    def __str__(self):
       return '%s %s %s' % (self.name, self.min_inversion, self.max_inversion)



class SponsorInYear(models.Model):
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE)
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    category = models.ForeignKey(SponsorCategory, related_name="categoryOfSponsorInYear", on_delete=models.CASCADE)
    money = models.IntegerField(null=False)
    class Meta:
       unique_together = (("sponsor","year"),)
    def __str__(self):
        return str("Year: "+str(self.year)+" Name: "+str(self.sponsor))

class ItemDonor(models.Model):
    name = models.CharField(max_length=160, null=True, blank=True)
    link = models.CharField(max_length=300, null=True, blank=True)
    logo = models.ImageField(null=True, upload_to='outreach/item_donors/')
    def __str__(self):
        return '%s' % (self.name)

class ItemInYear(models.Model):
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    name = models.CharField(max_length=160, null=True, blank=True) 
    donor = models.ForeignKey(ItemDonor, on_delete=models.CASCADE)
    value = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    link = models.CharField(max_length=160, null=True, blank=True)
    def __str__(self):
        return '%s %s' % (self.name, self.value)

class GisDayPhoto(models.Model):
    picture = models.ImageField(null=True, upload_to='outreach/gallery/')
    year = models.ForeignKey(Year, on_delete=models.CASCADE)

class Agenda(models.Model):
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    entry_name = models.CharField(max_length=100, null=True, blank=True)
    time_ini = models.TimeField(null=False,blank=False)
    time_end = models.TimeField(blank=True,null=True)
    speaker = models.CharField(max_length=160, null=True, blank=True)
    
    def __str__(self):
        return '%s %s' % (self.year, self.entry_name)
    class Meta:
       unique_together = (("year","entry_name"),)

class Announcement(models.Model):
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    position = models.PositiveIntegerField(null=False,blank=False)
    entry_name = models.CharField(max_length=100, null=True, blank=True)
    content = tinymce_models.HTMLField(null=True,blank=True)
    date = models.DateField(null=True,blank=True)
    image = models.ImageField(null=True,blank=True, upload_to='outreach/announcements/')
    
    def __str__(self):
        return '%s %s' % (self.year, self.entry_name)
    class Meta:
       unique_together = (("year","position"),)

class SummaryContent(models.Model):
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    content = tinymce_models.HTMLField(null=True,blank=True)
    class Meta:
        unique_together = (("year",),)
class PosterContestContent(models.Model):
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    content = tinymce_models.HTMLField(null=True,blank=True)
    registration_message = tinymce_models.HTMLField(null=True,blank=True)
    registration_recipients = models.CharField(max_length=600,null=False,blank=False,default="gisday@ou.edu")
    class Meta:
        unique_together = (("year",),)
class PhotoContestContent(models.Model):
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    content = tinymce_models.HTMLField(null=True,blank=True)
    class Meta:
        unique_together = (("year",),)
class LogisticsContent(models.Model):
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    content = tinymce_models.HTMLField(null=True,blank=True)
    class Meta:
        unique_together = (("year",),)
class VisitorRegistrationContent(models.Model):
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    content = tinymce_models.HTMLField(null=True,blank=True)
    registration_message = tinymce_models.HTMLField(null=True,blank=True)
    registration_recipients = models.CharField(max_length=600,null=False,blank=False,default="gisday@ou.edu")
    class Meta:
        unique_together = (("year",),)
class SponsorsContent(models.Model):
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    content = tinymce_models.HTMLField(null=True,blank=True)
    class Meta:
        unique_together = (("year",),)
class CommitteeContent(models.Model):
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    content = tinymce_models.HTMLField(null=True,blank=True)
    class Meta:
        unique_together = (("year",),)
class BoothContent(models.Model):
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    content = tinymce_models.HTMLField(null=True,blank=True)
    max_booths = models.PositiveIntegerField(null=False, blank=False, default=30)
    registration_message_non_profit = tinymce_models.HTMLField(null=True,blank=True)
    registration_message_profit = tinymce_models.HTMLField(null=True,blank=True)
    registration_recipients = models.CharField(max_length=600,null=False,blank=False,default="gisday@ou.edu")
    class Meta:
        unique_together = (("year",),)

class OverviewContent(models.Model):
    content = tinymce_models.HTMLField(null=True,blank=True)

class OverviewImage(models.Model):
    image = models.ImageField(null=False,blank=False, upload_to='outreach/overview/')
    order = models.IntegerField(null=False,blank=False)
    title = models.CharField(max_length=300,null=True,blank=True)
    description = models.CharField(max_length=300,null=True,blank=True)

    class Meta:
        unique_together = (("order",),)

INSTITUTION_CHOICES=(
    ("Oklahoma State University","Oklahoma State University"),
    ("Samuel Roberts Noble Foundation","Samuel Roberts Noble Foundation"),
    ("University of Oklahoma","University of Oklahoma"),
    ("University of Tulsa","University of Tulsa"),
    ("Other","Other please specify"),
)

PARTICIPANT_POSITION_CHOICES=(
    ("Community College Faculty","Community College Faculty"),
    ("Doctoral Student","Doctoral Student"),
    ("EPSCoR Staff","EPSCoR Staff"),
    ("Government Staff","Government Staff"),
    ("Graduate Faculty","Graduate Faculty"),
    ("Higher Education Faculty","Higher Education Faculty"),
    ("K-12 Administrator","K-12 Administrator"),
    ("K-12 Teacher","K-12 Teacher"),
    ("K-12 Student","K-12 Student"),
    ("Master's Student","Master's Student"),
    ("Other Pre-College Teachers","Other Pre-College Teachers"),
    ("Post-Doctoral Researcher","Post-Doctoral Researcher"),
    ("Researcher","Researcher"),
    ("REU Participant","REU Participant"),
    ("Technical School Faculty","Technical School Faculty"),
    ("Technical School Student","Technical School Student"),
    ("Staff - Technical","Staff - Technical"),
    ("Staff - Non-Technical","Staff - Non-Technical"),
    ("Undergraduate Faculty","Undergraduate Faculty"),
    ("Undergraduate Student","Undergraduate Student"),
    ("Other","Other please specify"),
)

HIGHEST_DEGREE_CHOICES=(
    ("High School","High School"),
    ("Associate","Associate"),
    ("Bachelor's","Bachelor's"),
    ("Master's","Master's"),
    ("Doctoral","Doctoral"),
)
GENDER_CHOICES=(
    ("Female","Female"),
    ("Male","Male"),
    ("NR","Prefer not to respond"),
)
ETHNICITY_CHOICES=(
    ("Hispanic/Latino","Hispanic/Latino"),
    ("Not Hispanic/Latino","Not Hispanic/Latino"),
    ("NR","Prefer not to respond"),
)
CITIZENSHIP_CHOICES=(
    ("US Citizen","US Citizen"),
    ("Permanent Resident","Permanent Resident"),
    ("Non-Us Citizen","Non-Us Citizen"),
    ("NR","Prefer not to respond"),
)
RACE_CHOICES=(
    ("American Indian or Alaskan Native","American Indian or Alaskan Native"),
    ("Asian","Asian"),
    ("Black or African American ","Black or African American "),
    ("Native Hawaiian or Pacific Islander","Native Hawaiian or Pacific Islander"),
    ("White","White"),
    ("Prefer not to respond","Prefer not to respond"),
    ("Other","Other (please specify)"),
)
SURVEY_CHOICES=(
    ("Hearing Impairment","Hearing Impairment"),
    ("Mobility/Orthopedic impairment","Mobility/Orthopedic impairment"),
    ("Visual Impairment","Visual Impairment"),
    ("None","None"),
    ("Prefer not to respond","Prefer not to respond"),
    ("Other","Other (please specify)"),
)
DISABILITY_CHOICES = (
    ("Hearing Impairment","Hearing Impairment"),
    ("Mobility/Orthopedic impairment","Mobility/Orthopedic impairment"),
    ("Visual Impairment","Visual Impairment"),
    ("None","None"),
    ("Prefer not to respond","Prefer not to respond"),
    ("Other","Other (please specify)"),
)
PARENTS_DEGREE_CHOICES=(
    ("Neither","Neither my mother or father (neither of my guardians)"),
    ("Both","Both my mother and father (both my guardians)"),
    ("Father","Only my father (male guardian)"),
    ("Mother","Only my mother (female guardian)"),
    ("Don't know","I do not know"),
    ("NR","Prefer not to respond"),
)
class DemographicSurvey(models.Model):
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    institution = models.CharField("Participant Institution", max_length=80,choices=INSTITUTION_CHOICES,null=False)
    other_institution = models.CharField('If other, please specify',max_length=80,null=True,blank=True)

    position = models.CharField("Participant Position", max_length=80,choices=PARTICIPANT_POSITION_CHOICES,null=False)
    other_position = models.CharField('If other, please specify',max_length=80,null=True,blank=True)

    highest_degree = models.CharField("Highest Degree Obtained", max_length=20,choices=HIGHEST_DEGREE_CHOICES,null=False)

    gender = models.CharField("Gender", max_length=20,choices=GENDER_CHOICES,null=False)

    ethnicity = models.CharField("Ethnicity", max_length=20,choices=ETHNICITY_CHOICES,null=False)

    citizenship = models.CharField("Citizenship", max_length=30,choices=CITIZENSHIP_CHOICES,null=False)
    
    race = models.CharField("Race", max_length=50,choices=RACE_CHOICES,null=False)
    other_race = models.CharField('If other, please specify',max_length=50,null=True,blank=True)

    disability = models.CharField("Disability", max_length=50,choices=DISABILITY_CHOICES,null=False)
    other_disability = models.CharField('If other, please specify',max_length=50,null=True,blank=True)

    parents_degree = models.CharField("In your family, which of your parents/guardians received college degrees?", max_length=80,choices=PARENTS_DEGREE_CHOICES,null=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
ROLES_CHOICES = (
    ("Organizing Committee","Organizing Committee"),
    ("Faculty Poster Judge","Faculty Poster Judge"),
    ("Student Poster Contestant","Student Poster Contestant"),
    ("Booth Exhibitor","Booth Exhibitor"),
    ("Poster Exhibitor","Poster Exhibitor"),
    ("Student Facilitator/Volunteer","Student Facilitator/Volunteer"),
    ("Staff Facilitator","Staff Facilitator"),
    ("Other","Other (please specify)"),
)
class Survey(DemographicSurvey):
    participate_again = models.BooleanField("I would like to participate in the event again")
    role = models.CharField("What was you primary role in the event?",max_length=50,choices=ROLES_CHOICES,null=False)
    other_role = models.CharField('If other, please specify',max_length=80,null=True,blank=True)
    beneficial_aspects = models.TextField('What was the most beneficial or interesting aspect of the event?',null=False,blank=False)
    comments_and_suggestions = models.TextField('Please provide any additional comments or suggestions:',null=True,blank=True)
    # def __str__(self):
    #     if self.role="Other":
    #         return '%s Other(%s) created: %s' % (self.year, self.uther_role,created)
    #     else 
class SurveyContents(models.Model):
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    content = tinymce_models.HTMLField(null=True,blank=True) 
    class Meta:
        unique_together = (("year",),)


class Workshop(models.Model):
    name = models.CharField(max_length=500,null=False,blank=False)
    category = models.ForeignKey('WorkshopClass', on_delete=models.CASCADE)
    date_start = models.DateField(null=False,blank=False)
    date_end = models.DateField(null=False,blank=False)
    password = models.CharField(max_length=20,null=True, blank=True,help_text="Enter a password if the user needs a password to register (eg: Closed workshops)")
    content = tinymce_models.HTMLField(null=True,blank=True)
    address = models.CharField(max_length=300,blank=True,null=True)
    city = models.CharField(max_length=300,blank=True,null=True)
    country = models.CharField(max_length=300,blank=True,null=True)
    registration_open = models.BooleanField(default=False, null=False)
    description = models.TextField(null=True)
    admin_emails = models.CharField(max_length=1000,null=False,blank=False, default = 'gisday@ou.edu')
    registration_message = tinymce_models.HTMLField(null=True,blank=True)
    agenda = models.FileField(null=True, max_length=300,upload_to="outreach/agendas/", blank=True)

    extra_boolean_field1 = models.CharField(max_length=100, null=True, blank=True)
    extra_boolean_field2 = models.CharField(max_length=100, null=True, blank=True)
    extra_boolean_field3 = models.CharField(max_length=100, null=True, blank=True)

    extra_text_field1 = models.CharField(max_length=100, null=True, blank=True)
    extra_text_field2 = models.CharField(max_length=100, null=True, blank=True)
    extra_text_field3 = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return '%s (%d)' % (self.name, self.date_start.year)
    class Meta:
        unique_together = (('name',),)

class SponsorInWorkshop(models.Model):
    workshop = models.ForeignKey('Workshop', on_delete=models.CASCADE)
    sponsor = models.ForeignKey('Sponsor', on_delete=models.CASCADE)
    def __str__(self):
        return '%s' % (self.sponsor)
    class Meta:
        unique_together = (('workshop','sponsor'),)


    
class WorkshopClass(models.Model):
    name = models.CharField(max_length=200,null=False,blank=False)
    image = models.ImageField(upload_to="outreach/categories", null=False)
    class Meta:
        unique_together = (('name',),)
    def __str__(self):
        return '%s' % (self.name)

class WorkshopRegistration(models.Model):
    workshop = models.ForeignKey(Workshop, related_name='workshop', related_query_name='workshop', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100,null=False,blank=False)
    last_name = models.CharField(max_length=100,null=False,blank=False)
    position = models.CharField(max_length=300,null=False,blank=False)
    institution = models.CharField(max_length=200,null=False,blank=False)
    address = models.CharField(max_length=200,null=False,blank=False)
    email = models.EmailField(null=False,blank=False)
    phone = InternationalPhone(null=True, blank = True)
    area_of_expertise = models.CharField(max_length=300,null=False,blank=False)
    # Migrated to exta_boolean_field1
    # requests_travel_assistance = models.BooleanField(null=False, default=False)
    
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    validated = models.BooleanField()


    extra_boolean_field1 = models.BooleanField(default=False)
    extra_boolean_field2 = models.BooleanField(default=False)
    extra_boolean_field3 = models.BooleanField(default=False)

    extra_text_field1 = models.CharField(max_length=100, null=True, blank=True)
    extra_text_field2 = models.CharField(max_length=100, null=True, blank=True)
    extra_text_field3 = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        unique_together = (('workshop','email'),)
    def __str__(self):
        return '%s, %s (%s)' % (self.last_name,self.first_name,self.workshop)


class WorkshopPhoto(models.Model):

    workshop = models.ForeignKey('Workshop',related_name='workshop_images', on_delete=models.CASCADE)
    image = models.FileField(upload_to="outreach/photos", null=True, blank=True)
    priority = models.PositiveIntegerField(default=99999)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = (('workshop','image'),)
    @property
    def filename(self):
        return self.image.name.rsplit('/', 1)[-1]
class Institution(models.Model):
    name = models.CharField(max_length=200,null=False,blank=False)
    link = models.CharField(max_length=300,null=False,blank=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = (('name',),)
    def __str__(self):
        return '%s' % (self.name)


class Presentation(models.Model):
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    title = models.CharField(max_length=200,null=False,blank=False)
    first_name = models.CharField(max_length=100,null=False,blank=False)
    last_name = models.CharField(max_length=100,null=False,blank=False)
    other_presenters = models.CharField(max_length=200,null=False,blank=True)
    content = models.FileField(null=True, max_length=300,upload_to="outreach/presentations/", blank=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    time_ini = models.DateTimeField(null=False)
    time_end = models.DateTimeField(null=True) 
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = (('workshop','time_ini'),)
    def __str__(self):
        return '%s (%s)' % (self.title, self.workshop)