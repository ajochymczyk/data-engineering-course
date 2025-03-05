import geopandas as gpd
from shapely.geometry import Point, LineString
import pandas as pd
import json
import osmnx as ox
import matplotlib.pyplot as plt
import contextily as ctx

# 2.1 Exercise 1: Loading data and basic operations
with open('proj4_params.json', 'r') as f:
    params = json.load(f)

print("params:\n", params)
gdf = gpd.read_file('proj4_points.geojson')
print("gdf:\n", gdf)
buffered_points = gdf.copy()
buffered_points['geometry'] = buffered_points.geometry.buffer(100)
print("buffered_points:\n", buffered_points)
print("buffered_points['geometry']:\n", buffered_points['geometry'])
join_result = gpd.sjoin(gdf, buffered_points, predicate='intersects', how='left', lsuffix="")
print("join_result:\n", join_result)
counts = join_result.groupby("lamp_id_").size().reset_index(name='count')
counts = counts.rename(columns={'lamp_id_': params['id_column']})
print(counts)

counts.to_csv('proj4_ex01_counts.csv', index=False)

# longitude latitude:
gdf = gpd.read_file('proj4_points.geojson')
gdf = gdf.to_crs("EPSG:4326")
gdf['lat'] = gdf.geometry.y
gdf['lon'] = gdf.geometry.x
gdf[['lamp_id', 'lat', 'lon']].to_csv('proj4_ex01_coords.csv', index=False)

print(gdf[['lamp_id', 'lat', 'lon']])

# 2.2 Exercise 2: Loading data from OpenStreetMap
pd.set_option('display.max_columns', None)

road = ox.geometries_from_place('Kraków, Poland', tags={'highway': 'tertiary'})
road = road.reset_index()
road = road[['osmid', 'name', 'geometry']]
road = road.rename(mapper={'osmid': 'osm_id'}, axis=1)
road.to_file('proj4_ex02_roads.geojson', driver='GeoJSON')

print(road)

# 2.3 Exercise 3: Spatial joins

road = gpd.read_file('proj4_ex02_roads.geojson')
road = road.to_crs("EPSG:3857")
print(road)
buffer_distance = 50

road['buffer'] = road['geometry'].buffer(buffer_distance, cap_style=2)

gdf_points = gpd.read_file('proj4_points.geojson')

print("Number of streets:", len(road))
print("Number of points:", len(gdf_points))

street_point_counts = {'name': [], 'point_count': []}

for index, road in road.iterrows():
    road_line = LineString(road['geometry'])
    road_buffer = road_line.buffer(buffer_distance, cap_style=2)
    points_within_buffer = gdf_points[gdf_points.geometry.within(road_buffer)]
    point_count = len(points_within_buffer)
    if point_count > 0:
        street_point_counts['name'].append(road['name'])
        street_point_counts['point_count'].append(point_count)

df_street_point_counts = pd.DataFrame(street_point_counts)
df_street_point_counts = df_street_point_counts.groupby('name')['point_count'].sum().reset_index()

df_street_point_counts.to_csv('proj4_ex03_streets_points.csv', index=False)

print("df_street_point_counts:\n", df_street_point_counts)






# 2.4 Exercise 4: Drawing maps

gdf = gpd.read_file('proj4_countries.geojson')
print(gdf)
fig, ax = plt.subplots(figsize=(10, 6))
gdf.plot(ax=ax, edgecolor='black', facecolor='none', aspect='equal')

ctx.add_basemap(ax, crs=gdf.crs.to_string(), source=ctx.providers.OpenStreetMap.Mapnik)

ax.axis('off')
gdf['geometry'] = gdf['geometry'].boundary
print(gdf)
gdf.to_pickle('proj4_ex04_gdf.pkl')

for index, row in gdf.iterrows():
    country_name = row['name'].lower().replace(' ', '_')
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.set_title(row['name'])
    gdf[gdf['name'] == row['name']].plot(ax=ax, edgecolor='black', facecolor='none', aspect='equal')
    ctx.add_basemap(ax, crs=gdf.crs.to_string(), source=ctx.providers.OpenStreetMap.Mapnik)
    ax.axis('off')
    plt.savefig(f'proj4_ex04_{country_name}.png', bbox_inches='tight')
    plt.close()
