from django.contrib import admin
from rest.models import Place, User, Checkin

class PlaceInline(admin.TabularInline):
    modle = Place
    extra = 2

admin.site.register(Checkin)
admin.site.register(Place)
admin.site.register(User)
