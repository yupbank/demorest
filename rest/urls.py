
from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('rest.views',
        url(r'^places/(\d+)/checkins','checkins',name='id'),
        url(r'^places/(\d+)/checkin','checkin',name='id'),
        url(r'^places/(\d+)','place',name='id'),
        url(r'^places','places'),
        url(r'^users/(\d+)','users',name='id'),
        url(r'^users','user'),
        
        )
