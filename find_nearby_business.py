from msilib.schema import Class
import requests
import geocoder
import pandas as pd
import json


def track_me():
    g = geocoder.ip('me')
    loc = g.latlng
    lat = loc[0]
    lon = loc[1]
    return(lat, lon)

def find_nearby_pest_shop(max_n):
    lat, lon = track_me()
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + str(lat) +"%2C" + str(lon) + "&radius=1500"  + "&keyword=Pest Control Services" + "&key=AIzaSyAdqGSasNl5j98V7i8y9mZHlXU5uM1GTeg"
    print(url)
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    places_data = pd.DataFrame((json.loads(response.text))["results"])
    places_data.fillna("Unknown")
    business_names = places_data["name"].to_list()[:max_n]
    business_status = places_data["business_status"].to_list()[:max_n]
    geometry = places_data["geometry"].to_list()[:max_n]
    longitudes = [geometry[i]["location"]["lng"] for i in range(len(geometry))]
    latitudes = [geometry[i]["location"]["lat"] for i in range(len(geometry))]
    address = places_data["vicinity"].to_list()[:max_n]
    return([business_names, business_status, address, latitudes, longitudes])
