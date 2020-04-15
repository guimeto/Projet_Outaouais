# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 13:06:25 2019

@author: guillaume
"""
import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import warnings; warnings.filterwarnings(action='once')
import seaborn as sns
from scipy import stats
import warnings; warnings.filterwarnings(action='ignore')

   
#Lecture des données quotidiennes de CORDEX 
rep1='K:/PROJETS/PROJET_CORDEX/CORDEX-NAM44/DONNEES/'
variable_in = 'tasmax'

path_rcp45 =  ['CANRCM4_CanESM2_rcp45',           
               'CRCM5-v1_CCCma-CanESM2_rcp45', 'CRCM5-v1_MPI-M-MPI-ESM-LR_rcp45' ,  
               'HIRHAM5_ICHEC-EC-EARTH_rcp45',  
               'RCA4.v1_CCCma-CanESM2_rcp45','RCA4.v1_ICHEC-EC-EARTH_rcp45']

path_rcp85 = ['CANRCM4_CanESM2_rcp85',            
              'CRCM5-v1_CCCma-CanESM2_rcp85','CRCM5-v1_MPI-M-MPI-ESM-MR_rcp85',    
              'HIRHAM5_ICHEC-EC-EARTH_rcp85',  
              'RCA4.v1_CCCma-CanESM2_rcp85','RCA4.v1_ICHEC-EC-EARTH_rcp85']

path_histo = ['CANRCM4_CanESM2_historical',           
              'CRCM5-v1_CCCma-CanESM2_historical', 'CRCM5-v1_MPI-M-MPI-ESM-LR_historical',   
              'HIRHAM5_ICHEC-EC-EARTH_histo',  
              'RCA4.v1_CCCma-CanESM2_histo','RCA4.v1_ICHEC-EC-EARTH_histo']

list_rcp45 = ['CANRCM4_NAM-44_ll_CanESM2_rcp45',             
              'CRCM5-v1_NAM-44_ll_CCCma-CanESM2_rcp45', 'CRCM5-v1_NAM-44_ll_MPI-M-MPI-ESM-LR_rcp45' ,
              'HIRHAM5_NAM-44_ll_ICHEC-EC-EARTH_rcp45', 
              'RCA4.v1_NAM-44_ll_CCCma-CanESM2_rcp45','RCA4.v1_NAM-44_ll_ICHEC-EC-EARTH_rcp45']

list_rcp85 = ['CANRCM4_NAM-44_ll_CanESM2_rcp85',            
              'CRCM5-v1_NAM-44_ll_CCCma-CanESM2_rcp85','CRCM5-v1_NAM-44_ll_MPI-M-MPI-ESM-MR_rcp85', 
              'HIRHAM5_NAM-44_ll_ICHEC-EC-EARTH_rcp85',  
              'RCA4.v1_NAM-44_ll_CCCma-CanESM2_rcp85','RCA4.v1_NAM-44_ll_ICHEC-EC-EARTH_rcp85']

list_histo = ['CANRCM4_NAM-44_ll_CanESM2_historical',           
              'CRCM5-v1_NAM-44_ll_CCCma-CanESM2_historical', 'CRCM5-v1_NAM-44_ll_MPI-M-MPI-ESM-LR_historical',   
              'HIRHAM5_NAM-44_ll_ICHEC-EC-EARTH_histo',  
              'RCA4.v1_NAM-44_ll_CCCma-CanESM2_histo','RCA4.v1_NAM-44_ll_ICHEC-EC-EARTH_histo']

titre='Outaouais Bassin Versant: 1971-2000 et 2071-2100'

#Mois = ['novembre','decembre','janvier','fevrier','mars','avril']
Mois = ['avril']
#list_month = ["11","12","01","02","03","04",]
list_month = ["04"]

yi = 1971
yf = 2000
# Lecture du bassin versant de la rivière des Outaouais interpolé sur le doaime CORDEX-NAM44 
MASK = xr.open_dataset('Outaouais_NAM44.nc')
lat2d=MASK.variables['lat'][:]
lon2d=MASK.variables['lon'][:]
mask = MASK['sftlf'][ :, :].values
lonM = lon2d.where(mask==100)
latM = lat2d.where(mask==100)
    
result_histo = []
tt_histo = []
pr_histo = [] 
s2=[]
for i in range(0,len(list_histo)):  
    for year in range(yi,yf+1):
        print("Lecture de l'annee {} pour le modele {}".format(year, list_histo[i]))
        for m in list_month: 
            tt=0                        
            #globals()['flattened_list_'+str(year)] = []         
            # lecture de la température
            filename= rep1 + path_histo[i] + '/MONTH/' + variable_in + '/' +  list_histo[i] +  '_' + variable_in + '_' + str(year) + m + '.nc' 
            TAS = xr.open_dataset(filename)
            # lecture de la précipitation
            filename= rep1 + path_histo[i] + '/MONTH/preacc/' +  list_histo[i] +  '_preacc_' + str(year) + m + '.nc'    
            PR = xr.open_dataset(filename)
            # Les chams de temperature et de précipitation peuvent ne pas avoir la même dimension temporelle
            # Pour contourner ce pbm, on va créer un xarray.dataset avec ls deux variables mais uniquement 
            # avec la dimension temporelle de la précipitation 
           
            ds = xr.Dataset({'temperature': (['time', 'y', 'x'],  TAS.tasmax.values),
                               'precipitation': (['time', 'y', 'x'], PR.preacc.values)},
                                             coords={'lon': (['y', 'x'], PR.lon),
                                                     'lat': (['y', 'x'], PR.lat),
                                                      'time': PR.time})
                
            # On va détecter les journées avec précipitation et relever la température associée
            PR_w_precip = ds.precipitation.where( (ds.precipitation >= 1) )
            # On va détecter les journées avec précipitation et relever la température associée           
            TT_w_precip = ds.temperature.where( (ds.precipitation >= 1) )
            
           # Etape ou on peut sauver un champs netcdf intermédiaire  
           # PR_w_precip.to_netcdf('method1.nc'   
            
            # On filtre les points de grille au-dessus du bassin versant          
            PR_w_precip_BV = PR_w_precip.where(MASK.sftlf == 100 )
            TT_w_precip_BV = TT_w_precip.where(MASK.sftlf == 100 )
            
            # On effectue une moyenne spatiale par jour       
            PR_masked =  PR_w_precip_BV.mean(dim=('y', 'x'))
            TT_masked =  TT_w_precip_BV.mean(dim=('y', 'x'))
            
            # On crée un masque 1D des points de grille sans nan
            #PR_masked = PR_w_precip_BV.stack(dim=['time','y','x']).notnull()
            #TT_masked = TT_w_precip_BV.stack(dim=['time','y','x']).notnull()
            
            #PR_stacked = PR_w_precip_BV.stack(dim=['time','y','x'])[PR_masked].values
            #TT_stacked = TT_w_precip_BV.stack(dim=['time','y','x'])[TT_masked].values
            
            # On applique ce asque sur les données 1D  
            #PR_stacked = PR_w_precip_BV.stack(dim=['time','y','x'])[PR_masked].values
            #TT_stacked = TT_w_precip_BV.stack(dim=['time','y','x'])[TT_masked].values
            
            tt_histo.append(pd.DataFrame(TT_masked))          
            pr_histo.append(pd.DataFrame(PR_masked)) 
            dy = len(PR_masked.time)
            s = pd.Series( ['RCMS_Histo'] * dy)
            s = s.astype('category')
            s2.append(s)
            tt+=1
                        
data_pr_histo = pd.concat(pr_histo) 
data_tt_histo = pd.concat(tt_histo) 
category =  pd.concat(s2)      
result_histo = pd.concat([category, data_pr_histo,data_tt_histo],axis=1)
result_histo.columns = ['Scenario','Precipitation', 'Temperature']



  
yi = 2071
yf = 2100
result_rcp45 = []
tt_rcp45 = []
pr_rcp45 = [] 
s2=[]
for i in range(0,len(list_rcp45)): 
    for year in range(yi,yf+1):
        print("Lecture de l'annee {} pour le modele {}".format(year, list_rcp45[i]))
        for m in list_month: 
            tt=0         
            #globals()['flattened_list_'+str(year)] = []         
            # lecture de la température
            filename= rep1 + path_rcp45[i] + '/MONTH/' + variable_in + '/' +  list_rcp45[i] +  '_' + variable_in + '_' + str(year) + m + '.nc' 
            TAS = xr.open_dataset(filename)
            # lecture de la précipitation
            filename= rep1 + path_rcp45[i] + '/MONTH/preacc/' +  list_rcp45[i] +  '_preacc_' + str(year) + m + '.nc'    
            PR = xr.open_dataset(filename)
            
            # Les chams de temperature et de précipitation peuvent ne pas avoir la même dimension temporelle
            # Pour contourner ce pbm, on va créer un xarray.dataset avec ls deux variables mais uniquement 
            # avec la dimension temporelle de la précipitation 
            
            ds = xr.Dataset({'temperature': (['time', 'y', 'x'],  TAS.tasmax.values),
                           'precipitation': (['time', 'y', 'x'], PR.preacc.values)},
                                         coords={'lon': (['y', 'x'], PR.lon),
                                                 'lat': (['y', 'x'], PR.lat),
                                                  'time': PR.time})
     
            # On va détecter les journées avec précipitation et relever la température associée
            PR_w_precip = ds.precipitation.where( (ds.precipitation >= 1) )
            # On va détecter les journées avec précipitation et relever la température associée           
            TT_w_precip = ds.temperature.where( (ds.precipitation >= 1) )
            
           # Etape ou on peut sauver un champs netcdf intermédiaire  
           # PR_w_precip.to_netcdf('method1.nc'   
            
            # On filtre les points de grille au-dessus du bassin versant          
            PR_w_precip_BV = PR_w_precip.where(MASK.sftlf == 100 )
            TT_w_precip_BV = TT_w_precip.where(MASK.sftlf == 100 )
            
             # On effectue une moyenne spatiale par jour       
            PR_masked =  PR_w_precip_BV.mean(dim=('y', 'x'))
            TT_masked =  TT_w_precip_BV.mean(dim=('y', 'x'))
            
            tt_rcp45.append(pd.DataFrame(TT_masked))
            pr_rcp45.append(pd.DataFrame(PR_masked)) 
            dy = len(PR_masked.time)
            s = pd.Series( ['RCMS_rcp45'] * dy)
            s = s.astype('category')
            s2.append(s)
            tt+=1
            
data_pr_rcp45 = pd.concat(pr_rcp45) 
data_tt_rcp45 = pd.concat(tt_rcp45) 
category =  pd.concat(s2)    
result_rcp45 = pd.concat([category,data_pr_rcp45, data_tt_rcp45],axis=1)
result_rcp45.columns = ['Scenario','Precipitation', 'Temperature']


tt_rcp85 = []
pr_rcp85 = []
s2=[]
    
for i in range(0,len(list_rcp85)):    
    for year in range(yi,yf+1):
        print("Lecture de l'annee {} pour le modele {}".format(year, list_rcp85[i]))
        for m in list_month:  
            tt=0                        
            #globals()['flattened_list_'+str(year)] = []         
            # lecture de la température
            filename= rep1 + path_rcp85[i] + '/MONTH/' + variable_in + '/' +  list_rcp85[i] +  '_' + variable_in + '_' + str(year) + m + '.nc' 
            TAS = xr.open_dataset(filename)
            # lecture de la précipitation
            filename= rep1 + path_rcp85[i] + '/MONTH/preacc/' +  list_rcp85[i] +  '_preacc_' + str(year) + m + '.nc'    
            PR = xr.open_dataset(filename)
            # Les chams de temperature et de précipitation peuvent ne pas avoir la même dimension temporelle
            # Pour contourner ce pbm, on va créer un xarray.dataset avec ls deux variables mais uniquement 
            # avec la dimension temporelle de la précipitation 
            try:
                ds = xr.Dataset({'temperature': (['time', 'y', 'x'],  TAS.tasmax.values),
                           'precipitation': (['time', 'y', 'x'], PR.preacc.values)},
                                         coords={'lon': (['y', 'x'], PR.lon),
                                                 'lat': (['y', 'x'], PR.lat),
                                                  'time': PR.time})
            except: pass

            try:               
                ds = xr.Dataset({'temperature': (['time', 'y', 'x'],  TAS.tasmax.values),
                           'precipitation': (['time', 'y', 'x'], PR.get("Daily precipitation accumulation").values)},
                                         coords={'lon': (['y', 'x'], PR.lon),
                                                 'lat': (['y', 'x'], PR.lat),
                                                  'time': PR.time})
            except: pass
        
            try:
                ds = xr.Dataset({'temperature': (['time', 'y', 'x'],  TAS.tasmax.values),
                           'precipitation': (['time', 'y', 'x'], PR.pr.values)},
                                         coords={'lon': (['y', 'x'], PR.lon),
                                                 'lat': (['y', 'x'], PR.lat),
                                                  'time': PR.time})
            except: pass
            
            
     
            # On va détecter les journées avec précipitation et relever la température associée
            PR_w_precip = ds.precipitation.where( (ds.precipitation >= 1))
            # On va détecter les journées avec précipitation et relever la température associée           
            TT_w_precip = ds.temperature.where( (ds.precipitation >= 1) )
            
           # Etape ou on peut sauver un champs netcdf intermédiaire  
           # PR_w_precip.to_netcdf('method1.nc'   
            
            # On filtre les points de grille au-dessus du bassin versant          
            PR_w_precip_BV = PR_w_precip.where(MASK.sftlf == 100 )
            TT_w_precip_BV = TT_w_precip.where(MASK.sftlf == 100 )
                   
            # On effectue une moyenne spatiale par jour       
            PR_masked =  PR_w_precip_BV.mean(dim=('y', 'x'))
            TT_masked =  TT_w_precip_BV.mean(dim=('y', 'x'))
          
           
            tt_rcp85.append(pd.DataFrame(TT_masked))
            pr_rcp85.append(pd.DataFrame(PR_masked)) 
            
            dy = len(PR_masked.time)
            s = pd.Series( ['RCMS_rcp85'] * dy)
            s = s.astype('category')
            s2.append(s)
            tt+=1
          
data_pr_rcp85 = pd.concat(pr_rcp85) 
data_tt_rcp85 = pd.concat(tt_rcp85)   
category =  pd.concat(s2)      
result_rcp85  = pd.concat([category, data_pr_rcp85, data_tt_rcp85],axis=1)  
result_rcp85.columns = ['Scenario','Precipitation', 'Temperature']


result_histo=result_histo.dropna()
result_rcp45=result_rcp45.dropna()
result_rcp85=result_rcp85.dropna()

final = pd.concat([result_histo, result_rcp45, result_rcp85], axis=0)

import corr_indice
g = sns.PairGrid(final[["Scenario", "Temperature", "Precipitation"]], 
                 hue="Scenario", palette=dict(RCMS_Histo = 'green', RCMS_rcp45 = 'blue', RCMS_rcp85 = 'red')) 
g.map_upper(corr_indice.corr_pearson) 
g.map_upper(corr_indice.corr_spearman) 
g.map_upper(corr_indice.corr_kendall) 
g.map_lower(sns.regplot, marker="o", scatter_kws={'s':2}) 
g.map_diag(sns.kdeplot) 
g.set(alpha=0.5)

g.add_legend(fontsize=15) 
g.set(alpha=0.1)

fig1 = plt.gcf()
fig1.suptitle(titre, size=15)
fig1.subplots_adjust(top=0.9)     
g.savefig(('deltaPR_vs_deltaT_2071-2100.png'), dpi=300, bbox_inches='tight')



