import pandas as pd
import json

# Reading in the data, using Pandas, storing as a dataframe
populations = pd.read_csv("County Populations.csv")
populations["County"] = populations["County"].map(lambda x: x.rstrip("County"))

with open("ilcount.geojson") as f:
	geo_data = json.load(f)

boundaries = {}

for i in range(len(geo_data['features'])):
	boundaries[geo_data['features'][i]['properties']['name']] = geo_data['features'][i]['geometry']['coordinates']

ser = pd.Series(boundaries.values(), index = boundaries.keys(), name = "Borders")

'''
# Having trouble getting the boundaries series added to the populations dataframe.
populations = populations.join(ser, on = "County")
'''

'''
for i in range(len(data['features'])):
  print data['features'][i]['properties']['name']
  print data['features'][i]['geometry']['coordinates']
 '''

import IPython; IPython.embed()