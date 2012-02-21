# Create your views here.
from models import User, Place, Checkin, get_distance_hav_by_lat_lng, get_lat_lng_range
import json
from django.http import HttpResponse, HttpResponseRedirect

def index(request,home,name):
    print type(request)
    print request.GET.get('haha',None)
    return HttpResponse(json.dumps({'aa':'sada'}))


def places(request):
    lat = request.GET.get('lat',None)
    lng = request.GET.get('lng',None)
    limit = request.GET.get('limit',10)
    offset = request.GET.get('offset',0)
    radius = request.GET.get('radius',1)
    data = []
    error = []
    
    
    meta = dict(
                lat = lat,
                lng = lng,
                limit = limit,
                offset = offset,
                radius = radius,
                )

    lat1, lat2, lng1, lng2 = get_lat_lng_range(lat, lng, radius)
    places = Place.objects.filter(lat__gt=lat1).filter(lat__lt=lat2).filter(lng__gt=lng1).filter(lng__lt=lng2)
    if places: 
        for p in places:
            result = dict(
                            id = p.id,
                            name = p.name, 
                            address = p.address,
                            lat = p.lat, 
                            lng = p.lng,
                            distance = get_distance_hav_by_lat_lng(p.lat,p.lng,lat,lng)
                            )
            data.append(result)
    
    
    respone = dict(respone = dict(meta = meta, error = error, data = data))
   
   
    return HttpResponse(json.dumps(respone))

def place(request,id):
    pass


