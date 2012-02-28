from django.contrib import admin
from rest.models import Place, UserProfile, Checkin

class PlaceInline(admin.TabularInline):
    modle = Place
    extra = 3 

admin.site.register(Checkin)
admin.site.register(Place)
admin.site.register(UserProfile)

