# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 14:18:55 2020
Script to compute spearman correlation 
@author: guillaume
"""

import xarray as xr 
####https://uoftcoders.github.io/studyGroup/lessons/python/cartography/lesson/
from scipy import stats
import numpy as np

#variable = 'Monthly_PrecTOT'
variable = 'Monthly_Mean_Prcp'
yi = 1990
yf = 2020
out = 'K:/PROJETS/PROJET_OUTAOUAIS/Daymet_Month_Indices/Correlations/'
for month in ['01','02','03','04','05','06','07','08','09','10','11','12']:  
    # lecture de la serie d ERA5
    path_era5 = 'J:/REANALYSES/ERA5/Month_Mean_PR_Outaouais/'
    file = path_era5 + 'ERA5_Outaouais_Monthly_Mean_PR_CAN_'
    multi_file = [f'{file}{year}{month}_BV.nc' for year in range(yi,yf,1)]
    era5_all = xr.concat([xr.open_dataset(f) for f in multi_file], 'day')
    
    # lecture de la serie daymet sur la grille era5
    path_daymet = 'K:/PROJETS/PROJET_OUTAOUAIS/Daymet_Month_Indices/MOY/'
    
    file = path_daymet + 'Daymet_v3_'+variable + '_'
    multi_file = [f'{file}{year}_{month}_OUTAOUAIS_ERA5grid_BV.nc' for year in range(yi,yf,1)]
    daymet_all = xr.concat([xr.open_dataset(f) for f in multi_file], 'time')
    
    #rhowT,pvalT=stats.spearmanr(daymet_all.Mean_tasmax.values, era5_all.t2m.values,axis=0) # Calcule les corrélations pour chaque point grille
    # for Prectot
    corr_spearman_ERA5 = np.zeros((era5_all['tp'].shape[1],era5_all['tp'].shape[2]),dtype=float)    
    for ni in range(0,era5_all['tp'].shape[2]):   # loop over longitudes
        for nj in range(0, era5_all['tp'].shape[1]):  # loop over latitudes
            
             r, p = stats.spearmanr(era5_all.isel(latitude=[nj], longitude=[ni]).tp.values[:,0,0] ,
                                   daymet_all.isel(lat=[nj], lon=[ni]).Mean_Prcp.values[:,0,0] ) 
             if p >= 0.1 :
                 corr_spearman_ERA5[nj,ni] = np.nan
             else:
                 corr_spearman_ERA5[nj,ni] = r
                 
    data_set = xr.Dataset( coords={'lon': ([ 'lon'], era5_all.longitude),
                                             'lat': (['lat',], era5_all.latitude)})
    
    data_set["spearmanr"] = (['lat', 'lon'],  corr_spearman_ERA5)
        
    data_set.to_netcdf(out + 'Daymet_v3_spearmann_Correlation_ERA5grid' + variable + '_'+str(yi)+'_'+str(yf)+'_'+month+'_OUTAOUAIS_python.nc')             
             