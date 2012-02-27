# Create your views here.
from models import User, Place, Checkin
from utils import get_distance_hav_by_lat_lng, get_lat_lng_range, get_id_rank_list, get_rank_by_id
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404

def index(request):
    return render_to_response('index.htm', {})


def places(request):
    lat = request.GET.get('lat', None)
    lng = request.GET.get('lng', None)
    limit = request.GET.get('limit', 0)
    offset = request.GET.get('offset', 0)
    radius = request.GET.get('radius', 1)
    data = []
    error = []
    meta = {} 
    
    if not(lat and lng):
        error.append('no lat or lang!')

    try:
        limit, offset = map(int,[limit, offset])    
        radius = float(radius)
    except Exception,e:
        error.append(e.message)
    
    
    
    if not error:
        meta = dict(
                        lat = lat,
                        lng = lng,
                        limit = limit,
                        offset = offset,
                        radius = radius,
                    )

        lat1, lat2, lng1, lng2 = get_lat_lng_range(lat, lng, radius)
        places = Place.objects.filter(lat__gt=lat1).filter(lat__lt=lat2).filter(lng__gt=lng2).filter(lng__lt=lng1)
        
        
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
        else:
            error.append('out of range')
        
    
    respone = dict(respone = dict(meta = meta, error = error, data = data[offset:offset+limit]))
   
   
    return HttpResponse(json.dumps(respone),mimetype='application/json')

def place(request,id):
    lat = request.GET.get('lat',None)
    lng = request.GET.get('lng',None)
    errors = []
    res = []
    data = {}
    p = Place.objects.filter(id=id)
    
    if not(lat and lng):
        error.append('no lat or lang!')
    
    
    if p:
        p = p[0]
    else:
        errors.append('no such place!')
    
    
    if not errors:
        address = p.address
        checkins_count= p.checkin_set.count()
        checkins = p.checkin_set.all()[:2]
        
        
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
                                        )
                            )
                        )

        
        data = dict(
                        id = id,
                        name = p.name,
                        lat = p.lat,
                        lng = p.lng,
                        distance = get_distance_hav_by_lat_lng(lat,lng,p.lat,p.lng),
                        checkins_count = checkins_count,
                        checkins = res,
                    )

    
    result = dict(
                    response = dict(
                                    meta = dict(),
                                    errors = errors,
                                    data =  data,               
                                    )
                )
    

    return HttpResponse(json.dumps(result))



def checkins(request,id):
    limit = request.GET.get('limit',10)
    offset = request.GET.get('offset',0)
    errors = []
    res = []

    
    try:
        limit, offset = map(int,[limit, offset])    
    except Exception,e:
        errors.append(e.message)

    
    if not errors:
        p = Place.objects.filter(id=id)
        if p:
            p = p[0]
            checkins = p.checkin_set.all().order_by('-time')[offset:limit+offset]
            for i,c in enumerate(checkins):
                if i>2:
                    break
                res.append(
                        dict(
                            id = c.id,
                            time = '%d hours ago'%c.time.hour,
                            user = dict(
                                        id = c.user.id,
                                        name = c.user.username,
                                        )
                            
                            )
                        )
        else:
            errors.append('no such place!')


    result = dict(
                    meta = dict(),
                    errors = errors,
                    data = res,
                )

    return HttpResponse(json.dumps(result))



def checkin(request, id):
    p = Place.objects.filter(id=id)
    u = User.objects.all()[0]
    errors = []
    c_id = ''
    c_time = ''
    
    if p:
        p= p[0]
        c = Checkin(place=p,user=u)
        c_id = c.id
        c_time = c.time.hour
        c.save()
    else:
        errors.append('no such place')


    result = dict(
                    response = dict(
                                    meta = dict(),
                                    errors = errors,
                                    status = 'success' if not errors else 'fail',
                                    data = dict(
                                                checkin = dict(
                                                                id = c_id,
                                                                time = c_time,
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
    limit, offset = map(int,[limit, offset])    
    check_count = []
    errors = []
    res = []
    
    
    for u in User.objects.all():
        check_count.append([u.id,u.checkin_set.count()])
    
    
    rank = get_id_rank_list(limit,offset)
    
    
    for r in rank:
        _user = User.objects.get(id=r[0])
        
        
        res.append(dict(
                        id = r[0],
                        rank = r[1],
                        username = _user.username,
                        checkins = _user.checkin_set.count(),
                        )       
                    )
    
        
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
    id = int(id)
    errors = []
    username = '',
    rank = '',
    checkin_count = '',
    u = User.objects.filter(id=id)

    
    if u:
        u = u[0]
        rank = get_rank_by_id(id)
        username = u.username
        checkin_count = u.checkin_set.count()
        sex = None
    else:
        errors.append('user_id error')


    result = dict(
                    response = dict(
                                    meta = dict(),
                                    errors = errors,
                                    data = dict(
                                                id = id,
                                                username = username,
                                                rank = rank,
                                                checkin_count = checkin_count,
                                                )
                                    )
                    )
    
    
    return HttpResponse(json.dumps(result)) 

