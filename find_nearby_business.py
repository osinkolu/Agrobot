import requests
import pandas as pd
import json
import os

gcloud_api_key = os.environ['gcloud_api_key']

def find_nearby_pest_shop(max_n, lat , lon):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + str(lat) +"%2C" + str(lon) + "&radius=50000"  + "&keyword=Pest Control Services" + "&key=" + str(gcloud_api_key)+ '"'
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
