from __future__ import division
from django.db import models
import datetime


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=200)
    email = models.EmailField()
    sex = models.CharField(max_length=1, choices=(('M','Male'),('F','Female')), default='M')

    def __unicode__(self):
        return self.username


class Place(models.Model):
    name = models.CharField(max_length=200)
    lat = models.FloatField(db_index = True)
    lng = models.FloatField(db_index = True)
    address = models.TextField()

    def __unicode__(self):
        return self.name

class Checkin(models.Model):
    user = models.ForeignKey(User)
    place = models.ForeignKey(Place)
    time = models.DateTimeField(default=datetime.datetime.now())

    def __unicode__(self):
        return self.user

from math import sin, asin, cos, radians, fabs, sqrt, degrees

EARTH_RADIUS = 6371.0

def hav(theta):
    s = sin(theta / 2)
    return s*s

def get_distance_hav_by_lat_lng(lat0, lng0, lat1, lng1):
    lat0,lng0,lat1,lng1 = map(float,[lat0,lng0,lat1,lng1])
    lat0,lng0,lat1,lng1 = map(radians,[lat0,lng0,lat1,lng1])

    dlng = fabs(lng0 - lng1)
    dlat = fabs(lat0 - lat1)
    h = hav(dlat) + cos(lat0) * cos(lat1) * hav(dlng)
    distance = 2 * EARTH_RADIUS * asin(sqrt(h))
    return distance

def get_lat_lng_range(lat0, lng0, distance=1.0):
    lat0, lng0 = map(float, [lat0,lng0])
    dlng = 2 * asin(sin(distance / (2 * EARTH_RADIUS)) / cos(lat0))
    dlng = degrees(dlng)

    dlat = distance / EARTH_RADIUS
    dlat = degrees(dlat)
    
    lat1 = lat0 - dlat
    lat2 = lat0 + dlat

    lng1 = lng0 - dlng
    lng2 = lng0 + dlng

    return lat1, lat2, lng1, lng2

