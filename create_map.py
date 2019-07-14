import folium
import pandas as pd

df = pd.read_csv('./data_in/CZ_2010_META_DATA.csv')
location_values = df[['STATION', 'STATION_NBR', 'LAT', 'LNG']].values.tolist()

m = folium.Map(location=[36.778259, -119.417931],
               zoom_start=5,
               tiles='OpenStreetMap'
               )

for each in range(0, len(location_values)):
    folium.Marker(location_values[each][2:4],
                  popup='Station Number:' + ' ' + str(location_values[each][1]),
                  tooltip=location_values[each][0]).add_to(m).save('./templates/map.html')
