# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 20:29:59 2020

@author: guillaume
"""
import xarray as xr 
import numpy as np
import regionmask
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from osgeo import ogr
import warnings; warnings.filterwarnings(action='ignore')
from shapely.geometry import LineString, mapping,  Polygon

PATH_TO_SHAPEFILE = 'K:/PROJETS/PROJET_OUTAOUAIS/BV/Outaouais_WGS84.shp'
shape_mask = gpd.read_file(PATH_TO_SHAPEFILE)

shape_mask.loc[:, 'geometry'].plot()



t_in = 'J:/REANALYSES/ERA5/PR_1h/era5_edna_ea_197908_sfc.nc'        
ds = xr.open_mfdataset(t_in, chunks = {'time': 10})

lat_bnd = [70, 50]
lon_bnd = [250, 310]
ds = ds.sel( longitude=slice(*lon_bnd), latitude=slice(*lat_bnd),)

strlist = ['1' for x in shape_mask.FID_BV_Out]
intlist = [1 for x in shape_mask.FID_BV_Out]

strlist = ['1','1']
intlist = [1,1]

polygons = [Polygon(cham_geom), Polygon(neighbor_geom)]
boundary = cascaded_union(polygons)  # results in multipolygon sometimes
if shape_mask.geom_type == 'MultiPolygon':
   # extract polygons out of multipolygon
   list = []
   for polygon in boundary:
       list.append(polygon)
       

mask_poly = regionmask.Regions_cls(name = 'FID_BV_Out', numbers = intlist, names = strlist, abbrevs = strlist, outlines = list(shape_mask.geometry.values[i] for i in range(0,len(shape_mask.FID_BV_Out))))
mask_poly = regionmask.Regions_cls(name = 'FID_BV_Out', numbers = intlist, names = strlist, abbrevs = strlist, outlines = list(shape_mask.geometry[0])[1])

outlines = list(shape_mask.geometry.values[i] for i in range(0,len(shape_mask.FID_BV_Out)))
list(shape_mask.geometry[0])[1]

mask = mask_poly.mask(ds.isel(time = 0), lat_name='lat', lon_name='lon')

mask.to_netcdf('./mask.nc') 

plt.figure(figsize=(15,8))
ax = plt.axes()
mask.plot(ax = ax)
mask.plot(ax = ax, alpha = 0.8, facecolor = 'none', lw = 1)