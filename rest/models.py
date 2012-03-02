from __future__ import division
from django.db import models
import datetime
from django.contrib.auth.models import User



class UserProfile(models.Model):
    user = models.OneToOneField(User)
    sex = models.CharField(max_length=1, choices=(
                                                    ('M','Male'),
                                                    ('F','Female')), 
                                                    default='M',
                                                )
    



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
        return str(self.id)
    
    class Meta:
        ordering = ['-time']
