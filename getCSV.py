import shapefile  # the pyshp module
import pandas as pd
from pyproj import Proj, transform

shp_path_node = './nodelink/MOCT_NODE.shp'
sf_node = shapefile.Reader(shp_path_node)
shp_path_link = './nodelink/MOCT_LINK.shp'
sf_link = shapefile.Reader(shp_path_link)

# construct pandas dataframe
# grab the shapefile's field names
# node
fields_node = [x[0] for x in sf_node.fields][1:]
records_node = sf_node.records()
shps = [s.points for s in sf_node.shapes()] # node has coordinate data.
# link
fields_link = [x[0] for x in sf_link.fields][1:]
records_link = sf_link.records()

# write the records into a dataframe
# node
node_dataframe = pd.DataFrame(columns=fields_node, data=records_node)
# add the coordinate data to a column called "coords"
node_dataframe = node_dataframe.assign(coords=shps)
#print(node_dataframe[1:5])    # show first 5 items

# link
link_dataframe = pd.DataFrame(columns=fields_link, data=records_link)


'''
광역/특별시의 권역코드(STNL_REG)는 다음과 같다.
서울 : 100 ~ 124
부산 : 130 ~ 145
대구 : 150 ~ 157
인천 : 161 ~ 170
광주 : 175 ~ 179
대전 : 183 ~ 187
울산 : 192 ~ 196
'''

# Data restriction
range_STNL_REG=range(100,124) # STNL_REG for Seoul
df_node = pd.DataFrame()
df_link = pd.DataFrame()
for ii in range_STNL_REG:
    res_node = node_dataframe[node_dataframe['STNL_REG'] == str(ii) ]
    res_link = link_dataframe[link_dataframe['STNL_REG'] == str(ii) ]
    df_node = pd.concat([df_node,res_node],ignore_index=True) # marge data
    df_link = pd.concat([df_link,res_link],ignore_index=True)

# Change node name in korean
for idx,row in df_node.iterrows():
    if type(row['NODE_NAME']) == bytes :
        # row['NODE_NAME'] = row['NODE_NAME'].decode('euc_kr')
        row['NODE_NAME'] = row['NODE_NAME'].decode('cp949')

# Change coordinate system: 데이터의 좌표계를 사용하기 편한 위도/경도 좌표계로 변경
# 표준 노드/링크 데이터에서는 korea 2000(epsg:5186) 좌표계를 사용하고 있다.
# 이 좌표계를 위도와 경도 좌표계인 wgs84(epsg:4326) 좌표계로 변환해야 한다.
inProj = Proj(init = 'epsg:5186')
outProj= Proj(init = 'epsg:4326')
latitude = []
longitude= []
for idx,row in df_node.iterrows():
    x,y  = row.coords[0][0],row.coords[0][1]  # korea 2000 좌표계
    nx,ny = transform(inProj,outProj,x,y)     # 새로운 좌표계
    latitude.append(ny)
    longitude.append(nx)
df_node['latitude'] = latitude
df_node['longitude']= longitude
del df_node['coords'] # delete coords

# 후에 Gephi(visualization tool)를 사용하기 위해 column 이름을 수정
# Change column name to draw network in Gephi
df_node.rename(columns={'NODE_ID':'Id'},inplace = True)
df_link.rename(columns={'F_NODE':'Source','T_NODE':'Target'},inplace = True)

print(df_node.head())

# export to csv
df_node.to_csv('Seoul_node.csv') # node list
df_link.to_csv('Seoul_link.csv') # edge(=link) list
