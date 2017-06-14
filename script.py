import pandas as pd
import json
import plotly.plotly as py
import plotly.graph_objs as go

df = pd.read_csv("City Populations.csv")

with open("IL Cities.geojson") as f:
    cities = json.load(f)

import IPython; IPython.embed()


geo_dict = {}
not_in = 0

for i in range(len(geos['features'])):
    name = cities['features'][i]['properties']['name'][:-4]
    if name in df["City"]:
        geo_dict[name] = cities['features'][i]
    else:
        not_in += 1
print "Not in:", not_in

ser = pd.Series(geo_dict.values(), index = geo_dict.keys())
ser.name = "Location"

df = df.join(ser, on="City")
df = df.drop(df.index[0])

colors = ['#ffffe0','#fffddb','#fffad7','#fff7d1','#fff5cd','#fff2c8',
          '#fff0c4','#ffedbf','#ffebba','#ffe9b7','#ffe5b2','#ffe3af',
          '#ffe0ab','#ffdda7','#ffdba4','#ffd9a0','#ffd69c','#ffd399',
          '#ffd196','#ffcd93','#ffca90','#ffc88d','#ffc58a','#ffc288',
          '#ffbf86','#ffbd83','#ffb981','#ffb67f','#ffb47d','#ffb17b',
          '#ffad79','#ffaa77','#ffa775','#ffa474','#ffa172','#ff9e70',
          '#ff9b6f','#ff986e','#ff956c','#fe916b','#fe8f6a','#fd8b69',
          '#fc8868','#fb8567','#fa8266','#f98065','#f87d64','#f77a63',
          '#f67862','#f57562','#f37261','#f37060','#f16c5f','#f0695e',
          '#ee665d','#ed645c','#ec615b','#ea5e5b','#e85b59','#e75859',
          '#e55658','#e45356','#e35056','#e14d54','#df4a53','#dd4852',
          '#db4551','#d9434f','#d8404e','#d53d4d','#d43b4b','#d2384a',
          '#cf3548','#cd3346','#cc3045','#ca2e43','#c72b42','#c52940',
          '#c2263d','#c0233c','#be213a','#bb1e37','#ba1c35','#b71933',
          '#b41731','#b2152e','#b0122c','#ac1029','#aa0e27','#a70b24',
          '#a40921','#a2071f','#a0051c','#9d0419','#990215','#970212',
          '#94010e','#91000a','#8e0006','#8b0000', '#8b0000']

scl = dict(zip(range(0, 101), colors))

def get_scl(obj):
    frac = obj / 10000
    return scl[frac]

df['Color'] = df['Population'].apply(get_scl)

layers_ls = []
for i in df.index:
    item_dict = dict(sourcetype = 'geojson',
                     source = df.loc[i]['Location'],
                     type = 'fill',
                     color = df.loc[i]['Color'])
    layers_ls.append(item_dict)

mapbox_access_token = "pk.eyJ1Ijoiam9uZXNqcDYiLCJhIjoiY2ozcWc1aTY2MDFlZDMzbnVpa3hiN2I2ZSJ9.CdLfET8OqcoZkCUVVeplwg"

colorscl = [[i * .01, v] for i,v in enumerate(colors)]

data = go.Data([
            go.Scattermapbox(
                    lat = [0],
                    lon = [0],
                    marker = go.Marker(
                                  cmax=101,
                                  cmin=0,
                                  colorscale = colorscl,
                                  showscale = True,
                                  autocolorscale=False,
                                  color=range(0,101),
                                  colorbar= go.ColorBar(
                                                 len = .89
                                                        )
                                       ),
                    mode = 'markers')
                     ])

layout = go.Layout(
    title = 'City Populations',
    height=1050,
    width=800,
    autosize=True,
    hovermode='closest',
    mapbox=dict(
        layers= layers_ls,
        accesstoken=mapbox_access_token,
        bearing=0,
        center=dict(
            lat=39.03,
            lon=-105.7
        ),
        pitch=0,
        zoom=5.5,
        style='light'
    ),
)

fig = dict(data = data, layout=layout)
py.image.save_as(fig, filename='image/test.jpeg',
                 width = 750, height= 575)
from IPython.display import Image
Image('image/test.jpeg')

py.image.ishow("image/test.jpeg")