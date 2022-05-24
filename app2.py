import folium
from streamlit_folium import st_folium
import streamlit as st
import folium


m = folium.Map(location = [39.949,-75.150282], zoom_start = 16)

folium.Marker([39.949,-75.150282], popup="Liberty Bell", tooltip="Liberty Bell").add_to(m)
st_data = st_folium(m, width = 725)