# Create your views here.
from models import User, Place, Checkin, get_distance_hav_by_lat_lng, get_lat_lng_range, get_id_rank_list, get_rank_by_id
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
   
   
    return HttpResponse(json.dumps(respone),mimetype='application/json')

def place(request,id):
    lat = request.GET.get('lat',None)
    lng = request.GET.get('lng',None)

    p = Place.objects.get(id=id)
    address = p.address
    checkins_count= p.checkin_set.count()
    checkins = p.checkin_set.all()[:2]
    res = []
    print '2'
    for c in checkins:
        c_id = c.id
        c_time = c.time.hour
        c_user_id = c.user.id
        c_user_name = c.user.username
        res.append(
                    dict(
                    id = c_id,
                    time = c_time,
                    user = dict(
                            id = c_user_id,
                            username = c_user_name
                    )))
    result = dict(
            response = dict(
                    meta = dict(),
                    errors = dict(),
                    data = dict(
                            id = id,
                            name = p.name,
                            lat = p.lat,
                            lng = p.lng,
                            distance = get_distance_hav_by_lat_lng(lat,lng,p.lat,p.lng),
                            checkins_count = checkins_count,
                            checkins = res,
                        
                        )
                )
        )
    

    return HttpResponse(json.dumps(result))

def checkins(request,id):
    limit = request.GET.get('limit',10)
    offset = request.GET.get('offser',0)

    p = Place.objects.get(id=id)
    res = []
    if p:
        checkins = p.checkin_set.all()[offset:limit+offset]
        for c in checkins:
            res.append(
                    dict(
                        id = c.id,
                        time = c.time.hour,
                        user = dict(
                                id = c.user.id,
                                name = c.user.username,
                            )
                        
                        )
                    )
    result = dict(
            meta = dict(),
            errors = dict(),
            data = res,
            )
    return HttpResponse(json.dumps(result))



def checkin(request,id):
    p = Place.objects.get(id=id)
    u = User.objects.all()[-1]
    c = Checkin(place=p,user=u)
    c.save()
    result = dict(
                response = dict(
                        meta = dict(),
                        errors = dict(),
                        status = 'success',
                        data = dict(
                                checkin = dict(
                                        id = c.id,
                                        time = c.time,
                                        user = dict(
                                                id = u.id,
                                                username = u.username,
                                            )
                                    )
                            )
                    )
            )
   return HttpResponse(json.dumps(result)) 

def user(request):
    limit = request.GET.get('limit',10)
    offset = request.GET.get('offset',0)
    check_count = []
    for u in User.objects.all():
        check_count.append([u.id,u.checkin_set.count()])
    rank = get_id_rank_list(limit,offset)
    res = []
    for r in rank:
        _user = User.objects.get(id=r[0])
        res.append(dict(
                id = r[0],
                rank = r[1],
                username = _user.username,
                checkins = _user.checkin_set.count(),
            ))
    result = dict(
                response = dict(
                        meta = dict(
                                limit = limit,
                                offset = offset,
                                sort = 'rank',
                                count = 1,
                            ),
                        errors = dict(),
                        data = res,
                    )
            )
    return HttpResponse(json.dumps(result)) 
    


def users(request,id):
    u = User.objects.get(id=id)
    rank = get_rank_by_id(id)
    result = dict(
                response = dict(
                        meta = dict(),
                        errors = dict(),
                        data = dict(
                                id = id,
                                username = u.username,
                                rank = rank,
                                checkin_count = u.checkin_set.count(),
                            )
                    )
            )
    return HttpResponse(json.dumps(result)) 

