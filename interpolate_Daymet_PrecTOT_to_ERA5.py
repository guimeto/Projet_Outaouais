# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 13:53:00 2020
Script to interpolate Daymet grid to ERA5 grid using cKDTree from scipy
@author: guillaume
"""
#for Netcdf manipulation
import xarray as xr
#for array manipulation
import numpy as np
#for interpolation
from scipy.spatial import cKDTree
path_source = './Daymet_Month_Indices/PrecTOT/'

variable = 'Monthly_PrecTOT'
yi = 1990
yf = 2019


target = xr.open_dataset('Outaouais_ERA5_Grid.nc')
lat_target=target.latitude
lon_target=target.longitude
lat_target.shape

lon_target2d, lat_target2d = np.meshgrid(lon_target, lat_target)

source = xr.open_dataset(path_source + 'Daymet_v3_Monthly_PrecTOT_199001_OUTAOUAIS.nc')
lat_source = source.variables['lat'][:]
lon_source = source.variables['lon'][:]


def lon_lat_to_cartesian(lon, lat):
    # WGS 84 reference coordinate system parameters
    A = 6378.137 # major axis [km]   
    E2 = 6.69437999014e-3 # eccentricity squared 
    
    lon_rad = np.radians(lon)
    lat_rad = np.radians(lat)
    # convert to cartesian coordinates
    r_n = A / (np.sqrt(1 - E2 * (np.sin(lat_rad) ** 2)))
    x = r_n * np.cos(lat_rad) * np.cos(lon_rad)
    y = r_n * np.cos(lat_rad) * np.sin(lon_rad)
    z = r_n * (1 - E2) * np.sin(lat_rad)
    return x,y,z

xs, ys, zs = lon_lat_to_cartesian(lon_source.values.flatten(), lat_source.values.flatten())
xt, yt, zt = lon_lat_to_cartesian(lon_target2d.flatten(), lat_target2d.flatten())

tree = cKDTree(np.column_stack((xs, ys, zs)))

d, inds = tree.query(np.column_stack((xt, yt, zt)), k = 10)
w = 1.0 / d**2

def interpolate(source, target, d, inds):         
    w = 1.0 / d**2
    pcp_idw = np.sum(w * source.prcp.values.flatten()[inds], axis=1) / np.sum(w, axis=1)
    pcp_idw.shape = target.shape
    return pcp_idw

for year in range(yi,yf+1):
    for i in range (1,13,1):  
        source = xr.open_dataset(path_source + 'Daymet_v3_' + variable + '_'+str(year)+'{:02d}'.format(i)+'_OUTAOUAIS.nc')
        pcp_idw = interpolate(source,lon_target2d, d, inds)
        
        data_set = xr.Dataset( coords={'lon': ([ 'lon'], lon_target),
                                             'lat': (['lat',], lat_target)})
        data_set["PrecTOT"] = (['lat', 'lon'],  pcp_idw)
        
        data_set.to_netcdf(path_source + 'Daymet_v3_' + variable + '_'+str(year)+'_'+'{:02d}'.format(i)+'_OUTAOUAIS_ERA5grid.nc')

