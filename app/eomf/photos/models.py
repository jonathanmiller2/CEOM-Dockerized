import os, sys
from django.contrib.gis.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils.encoding import force_text
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point
from django.urls import reverse
from dateutil import parser
import time
import datetime
try:
    import Image, ImageDraw, ImageFont
except:
    from PIL import Image, ImageDraw, ImageFont
from django.utils.translation import ugettext_lazy as _

class ContinentBuffered(models.Model):
    gid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=13, blank=True,db_column='continent')
    geometry = models.MultiPolygonField(null=True, blank=True)

    def __str__(self):
        return unicode(_(self.name))

    class Meta:
        db_table = u'continent_buffered'
        verbose_name = _(u'Continent')
        verbose_name_plural = _(u'Continents')

class Category(models.Model):
    id = models.IntegerField(null=False)
    id_prim = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=40, blank=True)
    order = models.IntegerField()
    def __str__(self):
        return unicode(_(self.name))

    class Meta:
        db_table = u'categories'
        verbose_name = _(u'Category')
        verbose_name_plural = _(u'Categories')


class Country(models.Model):
    gid = models.IntegerField(primary_key=True)
    fips_cntry = models.CharField(max_length=2, blank=True)
    gmi_cntry = models.CharField(max_length=3, blank=True)
    iso_2digit = models.CharField(max_length=2, blank=True)
    iso_3digit = models.CharField(max_length=3, blank=True)
    iso_num = models.IntegerField(null=True, blank=True)
    cntry_name = models.CharField(max_length=40, blank=True)
    long_name = models.CharField(max_length=40, blank=True)
    isoshrtnam = models.CharField(max_length=45, blank=True)
    unshrtnam = models.CharField(max_length=55, blank=True)
    locshrtnam = models.CharField(max_length=43, blank=True)
    loclngnam = models.CharField(max_length=74, blank=True)
    status = models.CharField(max_length=60, blank=True)
    pop2007 = models.BigIntegerField(null=True, blank=True)
    sqkm = models.FloatField(null=True, blank=True)
    sqmi = models.FloatField(null=True, blank=True)
    land_sqkm = models.IntegerField(null=True, blank=True)
    colormap = models.IntegerField(null=True, blank=True)
    _oid = models.IntegerField(null=True, blank=True)
    the_geom = models.MultiPolygonField(null=True, blank=True)

    class Meta:
        db_table = u'country'
        verbose_name = _(u'Country')
        verbose_name_plural = _(u'Countries')
    def __str__(self):
        return unicode(_(self.cntry_name))

class Region(models.Model):
    gid = models.IntegerField(primary_key=True)
    region = models.CharField(max_length=21, blank=True)
    sqmi = models.DecimalField(null=True, max_digits=999, decimal_places=999, blank=True)
    sqkm = models.DecimalField(null=True, max_digits=999, decimal_places=999, blank=True)
    _oid = models.IntegerField(null=True, blank=True)
    the_geom = models.MultiPolygonField(null=True, blank=True)

    class Meta:
        db_table = u'region'
        verbose_name = _(u'Region')
        verbose_name_plural = _(u'Regions')
    def __str__(self):
        return unicode(_(self.region)) 

class CountryBuffered(models.Model):
    gid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=40, blank=True, db_column='cntry_name')
    geometry = models.MultiPolygonField(null=True, blank=True)


    def __str__(self):
        return unicode(_(self.name)) 

    class Meta:
        db_table = u'country_buffered'
        verbose_name = _(u'Country')
        verbose_name_plural = _(u'Countries')

class Research(models.Model):
    name = models.CharField(max_length=16, blank=True)
    description = models.TextField(blank=True)
    class Meta:
        db_table = u'research'
        verbose_name = _(u'Research')
        verbose_name_plural = _(u'Researches')
    def __str__(self):
        return unicode(_(self.name)) 

class PhotoUser(models.Model):
    username = models.CharField(max_length=30, blank=True)
    password = models.CharField(max_length=32, blank=True)
    infoid = models.IntegerField(null=True, blank=True)
    roleid = models.IntegerField(null=True, blank=True)
    createdate = models.DateTimeField(null=True, blank=True)
    level = models.IntegerField(null=True, blank=True)
    email = models.CharField(max_length=50, blank=True)
    researchid = models.IntegerField(null=True, blank=True)
    timestamp = models.IntegerField(null=True, blank=True)
    sessid = models.CharField(max_length=32, blank=True)
    name = models.CharField(max_length=100, blank=True)
    affiliation = models.CharField(max_length=250, blank=True)
    telephone = models.CharField(max_length=20, blank=True)
    address1 = models.CharField(max_length=50, blank=True)
    address2 = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=80, blank=True)
    postal = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=50, blank=True)
    class Meta:
        db_table = u'users'
        verbose_name = _(u'Photo User')
        verbose_name_plural = _(u'Photo Users')

class Theme(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField()
    icon = models.ImageField(upload_to="photos/themes/")
    class Meta:
        verbose_name = _(u'Theme')
        verbose_name_plural = _(u'Themes')
    def __str__(self):
        return unicode(_(self.name)) 
STATUS_CHOICES = (
    (0, _("Deleted")),
    (1, _("Public")),
    (2, _("Private")),
)

DIR_CARD_CHOICES = (
    (u'N', _('North')),
    (u'NNE', _('NNE')),
    (u'NE', _('NE')),
    (u'ENE', _('ENE')),
    (u'E', _('East')),
    (u'ESE', _('ESE')),
    (u'SE', _('SE')),
    (u'SSE', _('SSE')),
    (u'S', _('South')),
    (u'SSW', _('SSW')),
    (u'SW', _('SW')),
    (u'WSW', _('WSW')),
    (u'W', _('West')),
    (u'WNW', _('WNW')),
    (u'NW', _('NW')),
    (u'NNW', _('NNW')),
)


#Store all files in a special place, currently on health /data1/
photo_storage = FileSystemStorage(
    location=os.path.join(settings.MEDIA_ROOT, "photos"),
    base_url=settings.MEDIA_URL + "photos/"
)


def photo_path(instance, filename):
    ts = time.strftime(settings.TIMESTAMP_FORMAT)
    path = u"%d/%s_%s" % (instance.user.id, ts, filename)
    #os.makedirs(os.path.dirname(dest))
    return path


class Photo(models.Model):
    #id = models.IntegerField(unique=True)
    file = models.ImageField(
        storage=photo_storage,
        upload_to=photo_path,
        max_length=300,
        blank=True,
        db_column="location"
    )
    user = models.ForeignKey(User, null=True, blank=True, db_column='userid', on_delete=models.CASCADE)
    theme = models.ForeignKey(Theme, null=True, blank=True, db_column='photogroupid', on_delete=models.CASCADE)
    notes = models.TextField(blank=True, db_column='description')
    _lon = models.FloatField(null=True, blank=True, db_column='long')
    _lat = models.FloatField(null=True, blank=True, db_column='lat')
    regionid = models.IntegerField(null=True, blank=True)
    takendate = models.DateField(null=True, blank=True)
    time = models.DateTimeField(null=True, blank=True)
    uploaddate = models.DateField(null=True, blank=True, auto_now_add=True)
    datum = models.CharField(max_length=8, blank=True)
    alt = models.FloatField(null=True, blank=True)
    category = models.ForeignKey(Category, null=True, blank=True, db_column='categoryid', on_delete=models.CASCADE)
    point = models.PointField(null=True, blank=True)
    dir_card = models.CharField(max_length=4, choices=DIR_CARD_CHOICES, db_column='dir',blank=True)
    dir_deg = models.FloatField(null=True, blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, null=True, blank=True, default=1)
    #idxfti = models.TextField(blank=True) # This field type is a guess.
    file_hash = models.CharField(max_length=32, blank=True, db_column='hash')
    source = models.CharField(max_length=100, blank=True)


    def __str__(self):
        return self.file.name

    def set_lon(self, lon):
        if self.point is None:
            self.point = Point(lon, 0)
        else:
            self.point.x = lon

    def get_lon(self):
        if self.point is None:
            return None
        else:
            return self.point.x

    def set_lat(self, lat):
        if self.point is None:
            self.point = Point(0, lat)
        else:
            self.point.y = lat

    def get_lat(self):
        if self.point is None:
            return None
        else:
            return self.point.y

    lon = property(get_lon, set_lon)
    lat = property(get_lat, set_lat)

    def editable(self, user):
        if self.user == user:
            return True
        #TODO: Group stuff
        return False

    def info(self):
        return "Test"

    def exif(self):
        #import EXIF
        from exifread import process_file
        f = open(self.file.path, "rb")
        tags = process_file(f)
        return tags

    def exifStringed(self):
        tags = self.exif()
        for k in tags.keys():
            if k != 'JPEGThumbnail':
                try:
                    tags[k] = force_unicode(tags[k])
                except:
                    del tags[k]

        return tags

    def exifTakenTime(self, tags=None):
        if tags is None:
            tags = self.exif()

        s = None

        search_tags = (
            'GPS GPSDate',
            'GPS Date Stamp',
            'EXIF DateTimeOriginal',
            'EXIF DateTimeDigitized',
            'EXIF DateTime',
            'GPS Date/Time',
            'Image DateTime',
        )

        for t in search_tags:
            if t in tags:
                s = tags[t].values
                break

        if s is None:
            return None
        else:
            if (':' in s[0:10]):
                s = s.replace(':', '-', 2)
            dt = parser.parse(s)
            return dt

    def exifPopulate(self):
        tags = self.exif()

        if 'GPS GPSLatitude' in tags:
            lat = dms2float(tags, 'GPS GPSLatitude')
            lon = dms2float(tags, 'GPS GPSLongitude')
            if 'GPS GPSLongitudeRef' in tags and tags['GPS GPSLongitudeRef'].values == 'W':
                lon *= -1
            if 'GPS GPSLatitudeRef' in tags and tags['GPS GPSLatitudeRef'].values == 'S':
                lat *= -1
            self.point = Point(lon, lat)

        if 'GPS GPSImgDirection' in tags:
            self.dir_deg = tf(tags['GPS GPSImgDirection'].values[0])
            self.dir_card = degCard(self.dir_deg)

        if 'GPS GPSAltitude' in tags:
            self.alt = tf(tags['GPS GPSAltitude'])

        try:
            dt = self.exifTakenTime(tags)
            self.time = dt
            self.takendate = dt.date()
        except:
            pass

    #def fieldPopulate(self, lat, lon, alt, dir_deg, taken_time):
    def fieldPopulate(self, lat, lon, alt, dir_deg, taken_time):
    	self.point = Point(lon, lat)
    	self.alt = alt
    	self.dir_deg = dir_deg
    	self.dir_card = degCard(dir_deg)
    	self.time = taken_time
    	self.takendate = taken_time.date()


    def basename(self):
        return os.path.basename(self.file.name)

    def get_absolute_url(self):
        return reverse('photo-view', kwargs={'pk': self.pk})

    def has_change_permission(self, request):
        if not request.user.is_authenticated():
            return False
        if self.user == request.user or request.user.is_superuser:
            return True
        return False

    def thumbnail(self, size, prefix=""):
        file = self.file

        if size == 'big':
            size = "800x800"
        elif size == 'small':
            size = "150x150"

        width, height = size.split('x')
        width = int(width)
        height = int(height)

        if hasattr(file, "path"):
            file_path = file.path
            file_name = file.name
        else:
            file_name = os.path.basename(file.name)
            file_path = file.name

        if hasattr(file, "url"):
            file_url  = file.url
        else:
            pre, post = file.name.split("media")
            file_url = "/media"+post

        name, extension = file_name.rsplit('.', 1)
        thumb = prefix + name + '_' + size + '.' + extension
        thumb_filename = os.path.join(os.path.dirname(file_path), thumb)
        thumb_url = os.path.join(os.path.dirname(file_url), thumb)

        if os.path.exists(thumb_filename):
            if os.path.getmtime(thumb_filename) < os.path.getmtime(file_path):
                create_new = True
                os.unlink(thumb_filename)
            else:
                create_new = False
        else:
            create_new = True

        if create_new:
            thumb_dir = os.path.dirname(thumb_filename)
            if not os.path.exists(thumb_dir):
                try:
                    os.makedirs(thumb_dir)
                except OSError as e:
                    if e.errno == 17:
                        pass
            try:
                image = Image.open(file_path)
                image.thumbnail([width, height], Image.ANTIALIAS)
            except:
                image = Image.new("RGBA",[width, height],(255, 255, 255))
                draw = ImageDraw.Draw(image)
                draw.text((0, 0), "Source image is corrupt", (50, 50, 50))
                draw = ImageDraw.Draw(image)

            image.save(thumb_filename, image.format)

        return thumb_url, thumb_filename

    def thumb_path(self, size):
        p = self.thumbnail(size)
        return p[1]

    class Meta:
        db_table = u'photos'
        verbose_name = _(u'Photo')
        verbose_name_plural = _(u'Photos')

def tf(f):
    if hasattr(f, 'num'):
        try:
            return float(f.num)/f.den
        except ZeroDivisionError:
            return 0
    else:
        try:
            return float(f.values[0].num)/f.values[0].den
        except ZeroDivisionError:
            return 0


def dms2float(t, k):
    if t[k].values[1].den == 0:
        return 0

    degrees = tf(t[k].values[0])
    minutes = float(tf(t[k].values[1]))/60
    seconds = float(tf(t[k].values[2]))/3600
    return degrees + minutes + seconds


def degCard(val):
    vals = ('N', 'NNE', 'NE', 'ENE',
            'E', 'ESE', 'SE', 'SSE',
            'S', 'SSW', 'SW', 'WSW',
            'W', 'WNW', 'NW', 'NNW',
    )
    return vals[int((((val + 11.25) / 22.5) % 16))]
