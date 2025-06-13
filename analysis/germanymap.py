# source: https://towardsdatascience.com/the-easiest-way-to-plot-data-from-pandas-on-a-world-map-1a62962a27f3

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd


countries = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
germany = countries[countries["name"] == "Germany"]
data = pd.read_csv('cities.dat', sep='\t')
data['count'] *= 50

fig, ax = plt.subplots(figsize=(6,6))
ax.set_xlim(5,16)
ax.set_ylim(46,56)

germany.plot(color="lightgrey", ax=ax)
data.plot(x="longitude", y="latitude", kind="scatter", c="count", s="count", 
          colormap="YlOrRd", title=f"cities in SPP-2451", ax=ax)

for i in data.index:
  city = data.iloc[i]
  ax.text(city['longitude']+np.power(city['count'], 1./2)/50+0.2, city['latitude'], city['city'], va='center', ha='left', alpha=.5, fontsize=8)
  # ax.text(city['longitude'], city['latitude']-0.2, city['city'], va='top', ha='center', alpha=.5, fontsize=8)

plt.savefig('cities_map.png', dpi=500)