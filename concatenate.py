# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 14:18:55 2020
Script to compute spearman correlation 
@author: guillaume
"""

import xarray as xr 
####https://uoftcoders.github.io/studyGroup/lessons/python/cartography/lesson/


variable = 'Tasmax'
yi = 1990
yf = 2019

for month in ['01','02','03','04','05','06','07','08','09','10','11','12']:    
        # lecture de la serie d ERA5
    path_era5 = 'J:/REANALYSES/ERA5/Tmax_daily_Outaouais/'
    file = path_era5 + 'ERA5_Outaouais_daily_tmax_'
    multi_file = [f'{file}{year}{month}.nc' for year in range(yi,yf,1)]
    era5_all = xr.concat([xr.open_dataset(f) for f in multi_file], 'time')
    
    # lecture de la serie daymet sur la grille era5
    path_daymet = 'K:/PROJETS/PROJET_OUTAOUAIS/Daily/tmax/'
    
    file = path_daymet + 'Daymet_v3_'+variable + '__'
    multi_file = [f'{file}{year}_{month}_OUTAOUAIS_ERA5grid_BV.nc' for year in range(yi,yf,1)]
    daymet_all = xr.concat([xr.open_dataset(f) for f in multi_file], 'time')
    
        
    daymet_all.to_netcdf(path_daymet + 'Daymet_v3_Daily_' + variable + '_'+str(yi)+'_'+str(yf)+'_'+month+'_OUTAOUAIS.nc')             
    era5_all.to_netcdf(path_era5 + 'ERA5grid_Daily_' + variable + '_'+str(yi)+'_'+str(yf)+'_'+month+'_OUTAOUAIS.nc')             