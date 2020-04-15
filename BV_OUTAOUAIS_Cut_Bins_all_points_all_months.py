# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 13:06:25 2019

@author: guillaume
"""
import xarray as xr
import pandas as pd
import matplotlib.pylab as plt
import warnings; warnings.filterwarnings(action='once')
import seaborn as sns
import warnings; warnings.filterwarnings(action='ignore')
import datetime
   
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

titre='Outaouais Bassin Versant: Daily mean precipitation'

list_month = ['11','12','01','02','03','04','05']


yi = 1971
yf = 2000

futi = 2071
futf = 2100

legends = ['RCMs historical: 1971-2000', 'RCMs rcp45 scenario: 2071-2100', 'RCMs rcp85 scenario: 2071-2100']

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
for m in list_month: 
    month = datetime.date(1900, int(m), 1).strftime('%B')        
    yi = 1971
    yf = 2000
    for i in range(0,len(list_histo)):  
        for year in range(yi,yf+1):
            print("Lecture de l'annee {} pour le modele {}".format(year, list_histo[i]))                  
                  
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
                    
            # On va détecter les centiles des P>1mm et relever la température associée
            PR_w_precip = ds.precipitation.where( (ds.precipitation >= 1) )
            # On va détecter les journées avec précipitation et relever la température associée           
            TT_w_precip = ds.temperature.where( (ds.precipitation >= 1) )
                
            # Etape ou on peut sauver un champs netcdf intermédiaire  
            # PR_w_precip.to_netcdf('method1.nc'   
                
            # On filtre les points de grille au-dessus du bassin versant          
            PR_w_precip_BV = PR_w_precip.where(MASK.sftlf == 100 )
            TT_w_precip_BV = TT_w_precip.where(MASK.sftlf == 100 )
                
            # On effectue une moyenne spatiale par jour       
            PR_masked =  PR_w_precip_BV
            TT_masked =  TT_w_precip_BV
                
            # On crée un masque 1D des points de grille sans nan
            PR_masked = PR_w_precip_BV.stack(dim=['time','y','x']).notnull()
            TT_masked = TT_w_precip_BV.stack(dim=['time','y','x']).notnull()
    
            # On applique ce asque sur les données 1D  
            PR_stacked = PR_w_precip_BV.stack(dim=['time','y','x'])[PR_masked].values
            TT_stacked = TT_w_precip_BV.stack(dim=['time','y','x'])[TT_masked].values
                
            tt_histo.append(pd.DataFrame(TT_stacked))          
            pr_histo.append(pd.DataFrame(PR_stacked)) 
      
                            
data_pr_histo = pd.concat(pr_histo) 
data_tt_histo = pd.concat(tt_histo) 
         
result_histo = pd.concat([ data_pr_histo,data_tt_histo],axis=1)
result_histo.columns = ['Precipitation', 'Temperature']

result_rcp45 = []
tt_rcp45 = []
pr_rcp45 = [] 
for m in list_month: 
    month = datetime.date(1900, int(m), 1).strftime('%B')      
    yi = futi
    yf = futf   
    for i in range(0,len(list_rcp45)): 
        for year in range(yi,yf+1):
            print("Lecture de l'annee {} pour le modele {}".format(year, list_rcp45[i]))            
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
            
             # On crée un masque 1D des points de grille sans nan
            PR_masked = PR_w_precip_BV.stack(dim=['time','y','x']).notnull()
            TT_masked = TT_w_precip_BV.stack(dim=['time','y','x']).notnull()

            # On applique ce asque sur les données 1D  
            PR_stacked = PR_w_precip_BV.stack(dim=['time','y','x'])[PR_masked].values
            TT_stacked = TT_w_precip_BV.stack(dim=['time','y','x'])[TT_masked].values
            
            tt_rcp45.append(pd.DataFrame(TT_stacked))          
            pr_rcp45.append(pd.DataFrame(PR_stacked)) 
          
data_pr_rcp45 = pd.concat(pr_rcp45) 
data_tt_rcp45 = pd.concat(tt_rcp45) 
  
result_rcp45 = pd.concat([data_pr_rcp45, data_tt_rcp45],axis=1)
result_rcp45.columns = ['Precipitation', 'Temperature']

result_rcp85 = []
tt_rcp85 = []
pr_rcp85 = []
for m in list_month: 
    month = datetime.date(1900, int(m), 1).strftime('%B')  
    yi = futi
    yf = futf    
    for i in range(0,len(list_rcp85)):    
        for year in range(yi,yf+1):
            print("Lecture de l'annee {} pour le modele {}".format(year, list_rcp85[i]))              
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
                   
            
             # On crée un masque 1D des points de grille sans nan
            PR_masked = PR_w_precip_BV.stack(dim=['time','y','x']).notnull()
            TT_masked = TT_w_precip_BV.stack(dim=['time','y','x']).notnull()

            # On applique ce asque sur les données 1D  
            PR_stacked = PR_w_precip_BV.stack(dim=['time','y','x'])[PR_masked].values
            TT_stacked = TT_w_precip_BV.stack(dim=['time','y','x'])[TT_masked].values
            
            tt_rcp85.append(pd.DataFrame(TT_stacked))          
            pr_rcp85.append(pd.DataFrame(PR_stacked)) 

              
data_pr_rcp85 = pd.concat(pr_rcp85) 
data_tt_rcp85 = pd.concat(tt_rcp85) 
      
result_rcp85  = pd.concat([data_pr_rcp85, data_tt_rcp85],axis=1)  
result_rcp85.columns = ['Precipitation', 'Temperature']


bins_T = list(range(-20,40,2))
lst = list(range(-20,42,2))
lst2 = list(range(-18,42,2))
labels = [format(x, '02d') for x in lst]
labels2 = [format(x, '02d') for x in lst2]
label_bins = [x+':'+y for x,y in zip(labels,labels2)] 
 
result_histo['temp_bins'] = pd.cut(x=result_histo['Temperature'], bins=lst, labels=label_bins)
result_rcp45['temp_bins'] = pd.cut(x=result_rcp45['Temperature'], bins=lst, labels=label_bins)
result_rcp85['temp_bins'] = pd.cut(x=result_rcp85['Temperature'], bins=lst, labels=label_bins)
#result_histo = result_histo[result_histo.temp_bins != '20:22']

list_tmp=[]
for label in label_bins:
    tmp = pd.DataFrame(result_histo['Precipitation'].loc[result_histo['temp_bins'] == label].values)
    tmp.columns = [label]
    list_tmp.append(tmp)
final_histo = pd.concat(list_tmp)

list_tmp=[]
for label in label_bins:
    tmp = pd.DataFrame(result_rcp45['Precipitation'].loc[result_rcp45['temp_bins'] == label].values)
    tmp.columns = [label]
    list_tmp.append(tmp)
final_rcp45 = pd.concat(list_tmp)

list_tmp=[]
for label in label_bins:
    tmp = pd.DataFrame(result_rcp85['Precipitation'].loc[result_rcp85['temp_bins'] == label].values)
    tmp.columns = [label]
    list_tmp.append(tmp)
final_rcp85 = pd.concat(list_tmp)


final_histo = final_histo.assign(Location=1)
final_rcp45 = final_rcp45.assign(Location=2)
final_rcp85 = final_rcp85.assign(Location=3)

cdf = pd.concat([final_histo, final_rcp45, final_rcp85])

mdf = pd.melt(cdf, id_vars=['Location'], var_name=['temp_bins'])

ax = sns.boxplot(x="temp_bins", 
                 y="value",
                 hue="Location", 
                 data=mdf, 
                 showfliers=False,
                 palette=[sns.xkcd_rgb["medium green"], 
                          sns.xkcd_rgb["medium blue"],
                          sns.xkcd_rgb["pale red"]],
                 )    # https://xkcd.com/color/rgb/


   


#ax.set(ylim=(0, 50))
#plt.legend(title='Smoker', loc='upper left', labels=['RCMs historical', 'RCMs rcp45 scenario', 'RCMs rcp85 scenario'])
handles, _ = ax.get_legend_handles_labels()
ax.legend(handles, legends ,prop={'size':15})
ax.set_title('Outaouais Watershed: November to May' , fontdict={'fontsize': 20, 'fontweight': 'bold'})
ax.set_ylabel('Daily precipitation [mm]', fontdict={'fontsize': 15, 'fontweight': 'bold'})
ax.set_xlabel('Daily maximum temperature range [Celcius]', fontdict={'fontsize': 15, 'fontweight': 'bold'})
for item in ax.get_xticklabels():
    item.set_rotation(45)  
fig1 = plt.gcf()
fig1.subplots_adjust(top=0.9)     
plt.savefig(('Precipitation_Daily_by_TMAXBins_All_points_November_to_May_'+str(futi)+'-'+str(futf)+'.png'), dpi=300, bbox_inches='tight')



