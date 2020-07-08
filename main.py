import os
import requests
import json
from flask import escape, abort
from urllib.parse import urlencode
from PIL import Image

def main(request):
    if request.method != 'GET':
        return abort(403)

    request_args = request.args

    latitude = request_args['lat']
    longitude = request_args['lng']
    zoom = request_args['zoom']

    water = is_water(get_rgb(latitude, longitude, zoom))

    res = {
        'latitude': latitude,
        'longitude': longitude,
        'zoom': zoom,
        'water': water
    }

    return json.dumps(res)

def get_rgb(latitude, longitude, zoom):
    request_url = make_url(latitude, longitude, zoom)

    image = Image.open(requests.get(request_url, stream=True).raw)

    image = image.convert('RGB')

    rgb = image.getpixel((0,0))

    return rgb

def is_water(rgb):
    r, g, b = rgb
    return b == 255


def make_url(latitude, longitude, zoom):
    BASE_URL = "https://maps.googleapis.com/maps/api/staticmap?"
    MAP_TYPE = "roadmap"
    SIZE = "1x1"
    API_KEY = os.environ.get('api-key')

    center = latitude + "," + longitude

    params = {
        'center': center,
        'zoom': zoom,
        'size': SIZE,
        'maptype': MAP_TYPE,
        'key': API_KEY
    }

    return BASE_URL + urlencode(params)


