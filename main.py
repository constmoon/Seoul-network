import os
import folium    # 위치정보를 시각화하기 위한 라이브러리
import pandas as pd
import numpy as np
import networkx as nx    # Python에서 네트워크 관련 기능을 사용할 수 있도록 구현한 라이브러리

nodes = pd.read_csv('Seoul_node.csv')
nodes = nodes[['Id','NODE_NAME','STNL_REG','latitude','longitude']]
seoul_id = dict()
for i in nodes['Id'] :
    seoul_id[i] = 0
print("nodes: ", len(nodes))

links = pd.read_csv('Seoul_link.csv')
links = links[['Source','Target']]
print(links.head())

source_in = links['Source'].apply(lambda x : x in seoul_id) # check Sources are in seoul_id
target_in = links['Target'].apply(lambda x : x in seoul_id) # check Targets are in seoul_id
# source_in and target_in are boolean type pandas.Series which contains True or False
seoul_links = links[source_in & target_in] # contain if both target and source are contained in seoul_id

for ix, row in seoul_links.iterrows():
    seoul_id[row['Source']] += 1
    seoul_id[row['Target']] += 1

# Positioning the Standard Point for out Folium Map
std_point = tuple(nodes.head(1)[['latitude','longitude']].iloc[0])
print("-----nodes.head-----")
print(nodes.head())

# Using Networkx
G = nx.Graph()
for idx,row in nodes.iterrows():
    G.add_node(row['Id'],Label=row['NODE_NAME'],latitude=row['latitude'], longitude=row['longitude'])
for idx,row in seoul_links.iterrows():
    G.add_edge(row['Source'],row['Target'])
print(nx.info(G))

# location : 기준이 되는 점, zoom_start : 지도 상의 zoom level 을 나타냄.
map_osm = folium.Map(location=std_point, zoom_start=10)
#
# # draw node
# for ix, row in nodes.iterrows():
#     location = (row['latitude'], row['longitude'])
#     folium.Circle(
#         location=location,
#         radius=seoul_id[row['Id']] * 30,
#         color='white',
#         weight=1,
#         fill_opacity=0.6,
#         opacity=1,
#         fill_color='red',
#         fill=True,  # gets overridden by fill_color
#         popup=str(row['Id'])
#     ).add_to(map_osm)
#
# map_osm.save('osm_seoul.html')

kw = {'opacity': 0.5, 'weight': 2}
for ix, row in seoul_links.iterrows():
    start = tuple(nodes[nodes['Id']==row['Source']][['latitude','longitude']].iloc[0])
    end = tuple(nodes[nodes['Id']==row['Target']][['latitude','longitude']].iloc[0])
    folium.PolyLine(
        locations=[start, end],
        color='blue',
        line_cap='round',
        **kw,
    ).add_to(map_osm)

map_osm.save('osm_seoul_link.html')