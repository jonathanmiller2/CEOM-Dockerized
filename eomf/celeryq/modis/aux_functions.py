import math
# CONVERTS FROM GEOGRAPHIC TO TILED SINUSOIDAL EQUAL AREA
#                                  ^NOT INTERGERIZED
# GIVES NEAREST MODIS PIXEL LOCATION TO A SPECIFIC LAT AND LON
# INPUT lat and lon, npix (1200 or 2400 or 4800)
# RETURNS SIN TILE INF
# OUTPUT ARE h,v,x,y
# KEYWORD resolution = 0.25, 0.5(default), or 1.0 IN KILOMETERS
def latlon2sin(lat,lon,modis='mod09a1',npix=2400.0):

    const =(36.*npix)/(2.*math.pi)
    folder = ''
    yg = 9.*npix - math.radians(const*lat)
    xg = math.radians(const*lon*math.cos(math.radians(lat))) + 18.*npix

    ih = int(xg/npix)
    iv = int(yg/npix)

    x = xg-ih*npix
    y = yg-iv*npix
 
    xi = int(x)
    yi = int(y)
    folder = u'h%02dv%02d' % (ih,iv) 
    return ih,iv,xi,yi,folder

def denary2binary(i):
    if i<0:
        u16 = i%2**16
        b16 = bin(u16)
    if i == 0:
        b16 = '0b0000000000000000'
    if i >0:
        b16 = bin(i)
    b16 = b16[2:]
    while(len(b16)<16):
        b16 ='0'+b16
    return b16