import os
import folium    # 위치정보를 시각화하기 위한 라이브러리
import pandas as pd
import numpy as np
import networkx as nx    # Python에서 네트워크 관련 기능을 사용할 수 있도록 구현한 라이브러리

nodes = pd.read_csv('Seoul_node.csv')
links = pd.read_csv('Seoul_link.csv')

nodes = nodes[['Id','NODE_NAME','latitude','longitude']]
links = links[['Source','Target']]

print(links.head())

source_in = links['Source'].apply(lambda x : x in list(nodes['Id'])) # check Sources are in seoul_id
target_in = links['Target'].apply(lambda x : x in list(nodes['Id'])) # check Targets are in seoul_id
# source_in and target_in are boolean type pandas.Series which contains True or False
seoul_links = links[source_in & target_in] # contain if both target and source are contained in seoul_id

G = nx.Graph()
R = 6371e3    # R is the Earth's radius

for idx, row in nodes.iterrows():
    # add node to Graph G
    G.add_node(row['Id'], Label=row['NODE_NAME'], latitude=row['latitude'], longitude=row['longitude'])

for idx, row in seoul_links.iterrows():
    ## Calculate the distance between Source and Target Nodes
    lon1 = float(nodes[nodes['Id'] == row['Source']]['longitude'] * np.pi / 180)
    lat1 = float(nodes[nodes['Id'] == row['Source']]['latitude'] * np.pi / 180)
    lon2 = float(nodes[nodes['Id'] == row['Target']]['longitude'] * np.pi / 180)
    lat2 = float(nodes[nodes['Id'] == row['Target']]['latitude'] * np.pi / 180)
    d_lat = lat2 - lat1
    d_lon = lon2 - lon1
    a = np.sin(d_lat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(d_lon / 2) ** 2
    c = 2 * np.arctan2(a ** 0.5, (1 - a) ** 0.5)
    d = R * c

    # Link attribute : 'Source', 'Target' and weight = 'Length between them'
    G.add_edge(row['Source'], row['Target'], weight=d)

#print(nx.info(G))

# Positioning the Standard Point for our Folium Map
std_point = tuple(nodes.head(1)[['latitude','longitude']].iloc[0])
print(std_point)

# location : 기준이 되는 점, zoom_start : 지도 상의 zoom level 을 나타냄.
map_osm = folium.Map(location=std_point, zoom_start=10)

for ix, row in nodes.iterrows():
    location = (row['latitude'], row['longitude']) # 위도, 경도 튜플
    folium.Circle(
        location=location,
        radius=G.degree[row['Id']] * 30, # 지름이 degree에 비례하도록 설정
        color='white',
        weight=1,
        fill_opacity=0.6,
        opacity=1,
        fill_color='red',
        fill=True,  # gets overridden by fill_color
        # popup = str(row['Id'])
    ).add_to(map_osm)
    # folium.Marker(location, popup=row['NODE_NAME']).add_to(map_osm)
print(map_osm)