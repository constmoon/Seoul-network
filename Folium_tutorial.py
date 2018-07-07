import os
import folium
import pandas as pd
import numpy as np

# get latitude, longitude: https://www.latlong.net/
skku = (37.293004, 126.975303)
skku_ccb = (37.295982, 126.975850)    # Coorporate Collaboration Building

# 기준점 설정
std_point = (np.array(skku) + np.array(skku_ccb)) / 2

map_osm = folium.Map(location=tuple(std_point), zoom_start=13)

# draw node
folium.Circle(
    location=skku,
    radius=20,
    color='white',
    weight=1,
    fill_opacity=0.6,
    opacity=1,
    fill_color='red',
    fill=True,  # gets overridden by fill_color
    # popup=str(row['Id'])
).add_to(map_osm)

folium.Circle(
    location=skku_ccb,
    radius=20,
    color='white',
    weight=1,
    fill_opacity=0.6,
    opacity=1,
    fill_color='red',
    fill=True,  # gets overridden by fill_color
    # popup=str(row['Id'])
).add_to(map_osm)

# draw link
kw = {'opacity': 0.5, 'weight': 2}
start = skku
end = skku_ccb
folium.PolyLine(
    locations=[start, end],
    color='blue',
    line_cap='round',
    **kw,
).add_to(map_osm)
map_osm.save('osm_skku.html')