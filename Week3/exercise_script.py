import geopandas as gpd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
import matplotlib.patches as mpatches


# ---------------------------------------------------------------------------------------------------------------------
# in this section, write the script to load the data and complete the main part of the analysis.
# Load the counties and wards data
counties = gpd.read_file('data_files/Counties.shp')
wards = gpd.read_file('data_files/Wards.shp')

# Ensure both datasets are in the same projection (UTM projection for consistency)
wards = wards.to_crs(epsg=32629)
counties = counties.to_crs(epsg=32629)

# Perform spatial join to associate wards with counties
wards_county = gpd.sjoin(wards, counties, how='inner', predicate='intersects')

# Summarize total population by county
population_by_county = wards_county.groupby('CountyName')['Population'].sum().reset_index()

# Print county with highest and lowest population
max_county = population_by_county.loc[population_by_county['Population'].idxmax()]
min_county = population_by_county.loc[population_by_county['Population'].idxmin()]

print("County with highest population: {} - {} residents".format(max_county['CountyName'], max_county['Population']))
print("County with lowest population: {} - {} residents".format(min_county['CountyName'], min_county['Population']))
# try to print the results to the screen using the format method demonstrated in the workbook

# load the necessary data here and transform to a UTM projection

# your analysis goes here...

# ---------------------------------------------------------------------------------------------------------------------
# below here, you may need to modify the script somewhat to create your map.
# create a crs using ccrs.UTM() that corresponds to our CRS
ni_utm = ccrs.UTM(29)

# create a figure of size 10x10 (representing the page size in inches
fig, ax = plt.subplots(1, 1, figsize=(10, 10), subplot_kw=dict(projection=ni_utm))

# add gridlines below
gridlines = ax.gridlines(draw_labels=True,
                         xlocs=[-8, -7.5, -7, -6.5, -6, -5.5],
                         ylocs=[54, 54.5, 55, 55.5])
gridlines.right_labels = False
gridlines.bottom_labels = False

# to make a nice colorbar that stays in line with our map, use these lines:
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1, axes_class=plt.Axes)

# plot the ward data into our axis, using gdf.plot()
ward_plot = wards.plot(column='Population', ax=ax, vmin=1000, vmax=8000, cmap='viridis',
                       legend=True, cax=cax, legend_kwds={'label': 'Resident Population'})

# add county outlines in red using ShapelyFeature
county_outlines = ShapelyFeature(counties['geometry'], ni_utm, edgecolor='r', facecolor='none')
ax.add_feature(county_outlines)

county_handles = generate_handles([''], ['none'], edge='r')

# add a legend in the upper left-hand corner
ax.legend(county_handles, ['County Boundaries'], fontsize=12, loc='upper left', framealpha=1)

# save the figure
fig.savefig('sample_map.png', dpi=300, bbox_inches='tight')
print("Map saved as population_map.png")