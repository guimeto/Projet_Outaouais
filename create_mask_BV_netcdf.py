# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 14:01:56 2020

@author: guillaume
"""
import xarray as xr
import warnings; warnings.filterwarnings(action='ignore')
from matplotlib import pyplot as plt
import numpy as np
from osgeo import ogr
import geopandas as gpd

ds = xr.open_mfdataset('J:/REANALYSES/ERA5/PR_1h/era5_edna_ea_197908_sfc.nc')
lat_bnd = [50, 43]
lon_bnd = [270, 300]

ds = ds.sel(longitude=slice(*lon_bnd), latitude=slice(*lat_bnd),)
ds = ds.assign_coords(longitude=(((ds.longitude + 180) % 360) - 180)).sortby('longitude')
ds
lat1d =  ds['latitude'].values
lon1d =  ds['longitude'].values
lon2d, lat2d = np.meshgrid(lon1d, lat1d)


tmpWGS84.to_file('K:/PROJETS/PROJET_OUTAOUAIS/BVOutaouais_WGS84.shp')
tmpWGS84

def get_mask(lons2d, lats2d, shp_path="", polygon_name=None):
    """
    Assumes that the shape file contains polygons in lat lon coordinates
    :param lons2d:
    :param lats2d:
    :param shp_path:
    :rtype : np.ndarray
    The mask is 1 for the points inside of the polygons
    """
    ds = ogr.Open(shp_path)
    """
    :type : ogr.DataSource
    """

    xx = lons2d.copy()
    yy = lats2d

    # set longitudes to be from -180 to 180
    xx[xx > 180] -= 360

    mask = np.zeros(lons2d.shape, dtype=int)
    nx, ny = mask.shape

    pt = ogr.Geometry(ogr.wkbPoint)

    for i in range(ds.GetLayerCount()):
        layer = ds.GetLayer(i)
        """
        :type : ogr.Layer
        """

        for j in range(layer.GetFeatureCount()):
            feat = layer.GetFeature(j)
            """
            :type : ogr.Feature
            """

            # Select polygons by the name property
            if polygon_name is not None:
                if not feat.GetFieldAsString("name") == polygon_name:
                    continue

            g = feat.GetGeometryRef()
            """
            :type : ogr.Geometry
            """

            assert isinstance(g, ogr.Geometry)

            for pi in range(nx):
                for pj in range(ny):
                    pt.SetPoint_2D(0, float(xx[pi, pj]), float(yy[pi, pj]))

                    mask[pi, pj] += int(g.Contains(pt))

    return mask

mask=get_mask(lon2d,lat2d,shp_path="Outaouais_WGS84.shp")
data = ds['tp'][1].where(mask==1)
data.plot()
data.to_netcdf('Outaouais_ERA5_Grid.nc')