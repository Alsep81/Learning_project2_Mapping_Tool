import folium
import pandas
data = pandas.read_csv("Volcanoes.txt")

#Layer "Volcanoes"
fgv = folium.FeatureGroup(name = "Volcanoes")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data['ELEV'])
name = list(data["NAME"])

def color_producer(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'

html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""
map = folium.Map(location = [38.58, -99.09], zoom_start = 6, tiles='https://api.mapbox.com/styles/v1/mapbox/light-v10/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoiYWxleDgxMDUiLCJhIjoiY2tpcjJ6d3cxMjJvYjJ1cWprM2E1bGM4ZyJ9.4JWspnHPgTpbIoOrUdQ4OQ',
    attr='mapbox')
#for coordinates in [[38.2, -99.1],[38.9, -97.1]]:
#    fg.add_child(folium.Marker(location = coordinates, popup = "Hi, I am a Marker", icon = folium.Icon(color = 'green')))

for lt, ln, el, name in zip(lat, lon, elev, name):
    iframe = folium.IFrame(html = html % (name, name, el), width=200, height=100)
    #fg.add_child(folium.Marker(location = [lt, ln], popup = folium.Popup(iframe), icon = folium.Icon(color = color_producer(el))))
    fgv.add_child(folium.CircleMarker(location = [lt, ln], radius = 6, popup = folium.Popup(iframe),
    fill_color = color_producer(el), color = 'grey', fill_opacity = 0.7))
#Layer Population
fgp = folium.FeatureGroup(name = "Population")
#Add country borders
fgp.add_child(folium.GeoJson(data =(open('world.json', 'r', encoding = 'utf-8-sig').read()),
style_function = lambda x: {'fillColor':'green' if x['properties']['POP2005']<10000000 else
'orange' if 10000000 <=x['properties']['POP2005']<20000000 else 'red' }))
map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())
map.save("Map_html_popup_advanced.html")
