from math import sin, asin, cos, radians, fabs, sqrt, degrees
from models import User

EARTH_RADIUS = 6371.0

def hav(theta):
    s = sin(theta / 2)
    return s*s

def get_distance_hav_by_lat_lng(lat0, lng0, lat1, lng1):
    lat0, lng0, lat1, lng1 = map(float, [lat0, lng0, lat1, lng1])
    lat0, lng0, lat1, lng1 = map(radians, [lat0, lng0, lat1, lng1])

    dlng = fabs(lng0 - lng1)
    dlat = fabs(lat0 - lat1)
    h = hav(dlat) + cos(lat0) * cos(lat1) * hav(dlng)
    distance = 2 * EARTH_RADIUS * asin(sqrt(h))
    return distance


def get_lat_lng_range(lat0, lng0, distance=1.0):
    lat0, lng0 = map(float, [lat0, lng0])

    dlng = distance/(30.887*cos(lat0))
    #dlng = 2 * asin(sin(distance / (2 * EARTH_RADIUS)) / cos(lat0))
    #dlng = degrees(dlng)

    dlat = distance / EARTH_RADIUS
    dlat = degrees(dlat)
    
    lat1 = lat0 - dlat
    lat2 = lat0 + dlat

    lng1 = lng0 - dlng
    lng2 = lng0 + dlng

    return lat1, lat2, lng1, lng2




def get_id_rank_list(limit=10,offset=0):
    check_count = []
    rank = []
    for u in User.objects.all():
        check_count.append([u.id, u.checkin_set.count()])
    if check_count:
        check_count.sort(key=lambda x:x[1],reverse=True)
        _rank = set([i[1] for i in check_count ])
        _rank = [i for i in _rank]
        _rank = [(i, len(_rank)-1-_rank.index(i)) for i in _rank]
        rank = {}
        for i,j in _rank:
            rank.update({i:j+1})
        rank = [ [i,rank[j]] for i, j in check_count]
        rank.sort(key=lambda x:x[1],reverse=True)
    return rank[offset:offset+limit]



def get_rank_by_id(id):
    rank_list = get_id_rank_list()
    return dict(rank_list).get(id)

