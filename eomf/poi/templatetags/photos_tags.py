import os
try:
    import Image, ImageDraw, ImageFont
except:
    from PIL import Image, ImageDraw, ImageFont
from django import template
from django.conf import settings
from django.utils.safestring import SafeString

register = template.Library()

@register.inclusion_tag('photos/tags/next_in_gallery.html')
def next_in_gallery(photo, gallery):
    return {'photo': photo.get_next_in_gallery(gallery)}

@register.inclusion_tag('photos/tags/prev_in_gallery.html')
def previous_in_gallery(photo, gallery):
    return {'photo': photo.get_previous_in_gallery(gallery)}

@register.filter
def thumbnail(file, size, prefix=""):
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
        file_url = u"/media"+post

    name, extension = file_name.rsplit('.', 1)
    thumb = prefix + name + u'_' + size + '.' + extension
    thumb_filename = os.path.join(os.path.dirname(file_path), thumb)
    thumb_url = os.path.join(os.path.dirname(file_url), thumb)

    if os.path.exists(thumb_filename):
        try:
            if os.path.getmtime(thumb_filename) < os.path.getmtime(file_path):
                create_new = True
                os.unlink(thumb_filename)
            else:
                create_new = False
        except OSError, e:
            #something wrong with source file
            create_new = False
    else:
        create_new = True

    if create_new:
        thumb_dir = os.path.dirname(thumb_filename)
        if not os.path.exists(thumb_dir):
            try:
                os.makedirs(thumb_dir)
            except OSError, e:
                if e.errno == 17:
                    pass
        try:
            image = Image.open(file_path)
            image.thumbnail([width, height], Image.ANTIALIAS)
        except:
            image = Image.new("RGBA",[width, height],(255,255,255))
            draw = ImageDraw.Draw(image)
            draw.text((0, 0), "Source image is corrupt", (50,50,50))
            draw = ImageDraw.Draw(image)
            
        image.save(thumb_filename, image.format)

    return thumb_url

@register.filter
def tablecols(data, cols):
    rows = []
    row = []
    index = 0
    for user in data:
        row.append(user)
        index = index + 1
        if index % cols == 0:
            rows.append(row)
            row = []
    # Still stuff missing?
    if len(row) > 0:
        rows.append(row)
    return rows
   
@register.filter 
def point2str(point):
    lon = round(point.x,4)
    lat = round(point.y,4)
    
    if lon < 0:
        s = str(lon * -1) + ' &deg;W, '
    else:
        s = str(lon) + ' &deg;E, ';

    if lat < 0:
        s += str(lat * -1) + ' &deg;S';
    else:
        s += str(lat) + ' &deg;N';
    
    return SafeString(s)
