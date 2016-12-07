"""
Introduction to Web Science
Assignment 5
Question 3
Team : golf

Script used to read the csv file and plot it in a thematic map
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from geonamescache import GeonamesCache #used to import country names
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from mpl_toolkits.basemap import Basemap

filename = 'dataset.csv'
# importing shp file containing the country borders
shapefile = 'shp/countries/ne_10m_admin_0_countries'
num_colors = 12
year = '2012'
cols = ['code','count','star','name']
title = "Geographic distribution of famous people's origin (simple wikipedia)"
imgfile = 'img/{}.png'.format("foast")

descripton = "Geographic distribution of famous people's \
origin (simple wikipedia), we notice that, clearly, \
the United states is the most dominant country of origin. \
Countries without data are shown in grey."


gc = GeonamesCache()
iso3_codes = list(gc.get_dataset_by_key(gc.get_countries(), 'iso3').keys())

df = pd.read_csv(filename,  usecols=cols)
print(df)
df.set_index('code', inplace=True)
df = df.ix[iso3_codes].dropna() # Filter out non-countries and missing values.
#df.drop('USA', inplace=True)
values = df['count']
cm = plt.get_cmap('Blues')
scheme = [cm(i / num_colors) for i in range(num_colors)]
bins = np.linspace(values.min(), values.max(), num_colors)
df['bin'] = np.digitize(values, bins) - 1
df.sort_values('bin', ascending=False).head(10)

fig = plt.figure(figsize=(22, 12))

ax = fig.add_subplot(111, axisbg='w', frame_on=False)
fig.suptitle(title)

m = Basemap(lon_0=0, projection='robin')
m.drawmapboundary(color='w')

m.readshapefile(shapefile, 'units', color='#444444', linewidth=.2)
for info, shape in zip(m.units_info, m.units):
    iso3 = info['ADM0_A3']
    if iso3 not in df.index:
        color = '#dddddd'
    else:
        color = scheme[df.ix[iso3]['bin']]

    patches = [Polygon(np.array(shape), True)]
    pc = PatchCollection(patches)
    pc.set_facecolor(color)
    ax.add_collection(pc)

# Cover up Antarctica so legend can be placed over it.
ax.axhspan(0, 1000 * 1800, facecolor='w', edgecolor='w', zorder=2)

# Draw color legend.
ax_legend = fig.add_axes([0.35, 0.14, 0.3, 0.03], zorder=3)
cmap = mpl.colors.ListedColormap(scheme)
cb = mpl.colorbar.ColorbarBase(ax_legend, cmap=cmap, ticks=bins, 
                               boundaries=bins, orientation='horizontal')
cb.ax.set_xticklabels([str(round(i, 1)) for i in bins])

# Set the map footer.
plt.annotate(descripton, xy=(-.8, -3.2), size=14, xycoords='axes fraction')

plt.savefig('map.png')
