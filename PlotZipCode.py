import numpy as np
import os
import geopandas as gpd
import plotly.express as px
import  plotly as py
import os

path = os.path.join(os.path.dirname(os.getcwd()), 'ABM-Simulator','input','ZIP','33613.geojson')


LG = gpd.read_file(path)

fig = px.scatter_mapbox(LG, lat="y", lon="x",
                        color_discrete_sequence=px.colors.qualitative.G10,
                        color="type",
                        zoom=10)
fig.update_layout(mapbox_style="open-street-map", title= "Hillsborough" + ' Location Graph', width=1000, height=800)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
py.offline.plot(fig, filename= "Pointcloud.html")
fig.show()
# print(len(LG[LG['type']=='house']))