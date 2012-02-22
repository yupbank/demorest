from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
  #  url(r'^(\w+)/(\w+)','index',name=('home','name')),
    #url(r'^api/v1/places','places'),
    #url(r'^api/vi/places/(\d+)','place',name='id'),
    url(r'^$','rest.views.index'),
    url(r'^api/v1/',include('rest.urls')),
    # url(r'^$', 'restdemo.views.home', name='home'),
    # url(r'^restdemo/', include('restdemo.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)
