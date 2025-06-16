import os
import sys
import requests
import polyline
from haversine import haversine

GOOGLE_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
if not GOOGLE_API_KEY:
    print('Missing GOOGLE_MAPS_API_KEY environment variable', file=sys.stderr)
    sys.exit(1)

if len(sys.argv) < 3:
    print('Usage: python wallapop_route.py "ORIGIN" "DESTINATION"', file=sys.stderr)
    sys.exit(1)

origin = sys.argv[1]
destination = sys.argv[2]


def get_route_points(origin, destination, api_key):
    url = 'https://maps.googleapis.com/maps/api/directions/json'
    params = {
        'origin': origin,
        'destination': destination,
        'key': api_key,
    }
    r = requests.get(url, params=params)
    r.raise_for_status()
    data = r.json()
    if not data.get('routes'):
        raise Exception('No route found')
    poly = data['routes'][0]['overview_polyline']['points']
    return polyline.decode(poly)


def search_wallapop(lat, lon, radius=1000):
    """Search Wallapop items near the given coordinate.

    This function uses Wallapop's public search endpoint. It may require
    additional authentication or parameters depending on Wallapop's API.
    """
    url = 'https://api.wallapop.com/api/v3/general/search'
    params = {
        'latitude': lat,
        'longitude': lon,
        'distance': radius,
        'order': 'distance',
    }
    headers = {'Accept': 'application/json'}
    r = requests.get(url, params=params, headers=headers)
    r.raise_for_status()
    return r.json()


points = get_route_points(origin, destination, GOOGLE_API_KEY)

print(f'Route has {len(points)} points')

# Query Wallapop along the route roughly every 5 km
STEP_KM = 5
results = []
last_point = points[0]
for point in points:
    if haversine(last_point, point) >= STEP_KM:
        lat, lon = point
        try:
            data = search_wallapop(lat, lon)
            results.append({
                'point': point,
                'items': data.get('search_objects', []),
            })
        except Exception as e:
            print(f'Failed to query Wallapop at {point}: {e}', file=sys.stderr)
        last_point = point

for segment in results:
    print('Location:', segment['point'])
    for item in segment['items']:
        title = item.get('title')
        price = item.get('price')
        url = item.get('web_slug')
        print(f' - {title} ({price} €) [{url}]')
    print()
