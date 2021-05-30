#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from shapely.geometry import shape, Point
from travel.resources.postcode import code2img

_geojson_data = {}
image_path = "/static/city/"

# 经纬度坐标地址解析，返回行政区划
def coordinate2address(longitude,latitude):
    point = Point(longitude, latitude)
    address = {
        'province': "",
        'city': "",
        'county': "",
        'image': code2img("00") 
    }

    _dfs('china', point, address)
    address['image'] = image_path + address['image']
    return address


def _dfs(id_, point, result={}):
    map_data = _geojson_data.get(id_)

    if map_data is None:
        if id_ == 'china':
            map_file_str = './travel/resources/mapdata/china.json'
        elif len(id_) == 2:
            map_file_str = './travel/resources/mapdata/geometryProvince/%s.json' % id_
        elif len(id_) == 4:
            map_file_str = './travel/resources/mapdata/geometryCouties/%s00.json' % id_
        else:
            return

        try:
            with open(map_file_str, encoding='UTF-8-SIG') as f:
                map_data = json.load(f)
                _geojson_data[id_] = map_data
        except Exception as e:
            print(e)
            return

    for feature in map_data['features']:
        polygon = shape(feature['geometry'])

        if polygon.contains(point):
            id_ = feature['properties']['id']
            name = feature['properties']['name']

            if len(id_) == 2:
                level = 'province'
            elif len(id_) == 4:
                level = 'city'
            elif len(id_) == 6:
                level = 'county'
            else:
                return
            
            result[level] = name

            img_path = code2img(id_)
            if img_path:
                result['image'] = img_path

            _dfs(id_, point, result)

            return

# 返回城市印象图
def coordinate2image(latitude, longitude):
    if ((latitude==None) or (longitude==None)):
        return '.' + image_path+code2img("00")
    address = coordinate2address(float(longitude),float(latitude))
    return "." + address['image']

def emptydict():
    address = {
        'province': "",
        'city': "",
        'county': "",
        'image': image_path + code2img("00") 
    }
    return address


if __name__ == '__main__':
    print("Input latitude,longitude :")
    latitude, longitude = input().split(',')
    longitude=float(longitude)
    latitude=float(latitude)
    address = coordinate2address(latitude, longitude)
    print(address)
