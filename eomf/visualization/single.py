#######################################################################
#	This is an adaptation from:
# 
# 
#	This perl makes tile detail pages for IDS web site.
#
#	Written by Dr. A. Prusevich
#
#	January, 2005
#	Updated -
#
#######################################################################


prod = 'MOD09A1'
sat_ver = 'Terra_C5'

def day_8(year, julian_day,increment):
    my @dir = (-1,1,0);

    year = substr($date,0,4);
    day  = substr($date,4,3);
    if (increment==True):
        day += 8;
    else:
   	    day -= 9

    if (day < 1):
        year--
        day=361
    else if (day > 365):
        year++
        day=1
    else:
        day=int(day/8)*8+1
    return str(year)+str(day)