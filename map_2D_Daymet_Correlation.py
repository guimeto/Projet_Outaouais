from netCDF4 import Dataset
import matplotlib.pylab as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
import matplotlib as mpl
import pandas as pd
import datetime
####https://uoftcoders.github.io/studyGroup/lessons/python/cartography/lesson/

## Date à utiliser 

path_in='K:/PROJETS/PROJET_OUTAOUAIS/Daily/Correlations/'
file = 'Daymet_v3_spearmann_Correlation_ERA5grid_Daily_Tasmin'
yi = 1990
yf = 2019
# lecture du contour du bassin versant 
BV_border = pd.read_csv('./points_contour_BV.csv', sep=',')
def plot_background(ax):
    ax.set_extent([-84,-70,45,48])
    ax.coastlines(resolution='110m');
    ax.add_feature(cfeature.OCEAN.with_scale('50m'))      
    ax.add_feature(cfeature.LAND.with_scale('50m'))       
    ax.add_feature(cfeature.LAKES.with_scale('50m'))     
    ax.add_feature(cfeature.BORDERS.with_scale('50m'))    
    ax.add_feature(cfeature.RIVERS.with_scale('50m'))    
    coast = cfeature.NaturalEarthFeature(category='physical', scale='10m',    
                        facecolor='none', name='coastline')
    ax.add_feature(coast, edgecolor='black')
    
    states_provinces = cfeature.NaturalEarthFeature(
        category='cultural',
        name='admin_1_states_provinces_lines',
        scale='10m',
        facecolor='none')

    ax.add_feature(states_provinces, edgecolor='gray')

   
    return ax

for month in ['01','02','03','04','05','06','07','08','09','10','11']:
    monthstr = datetime.date(1900, int(month), 1).strftime('%B')   
    filename = path_in + file
    
    dset=Dataset(filename + '_' + str(yi) + '_' + str(yf) + '_' + month +'_OUTAOUAIS_matlab.nc')
    ## Lecture du fichier 
    var=dset.variables['Spearmanr'][:].squeeze()
    lon=dset.variables['lon'][:]
    lat=dset.variables['lat'][:]

    
    fig = plt.figure(figsize=(28,16))
    crs=ccrs.LambertConformal()
    ax = plt.axes(projection=crs)
    plot_background(ax)
    
    ## Choisissons une colormap
    cmap0 = mpl.cm.get_cmap('jet', 16)
    #cmap0.set_under('w') ## on met en blanc les valeurs inferieures au min de clev
    #cmap0.set_over('black')
    
    mm = ax.contourf(lon,\
                           lat,\
                           var,\
                           vmin=0.8,\
                           vmax=1., \
                           transform=ccrs.PlateCarree(),\
                           cmap=cmap0)
    mtl_lon, mtl_lat = -73.5, 45.5
    
    levels = np.arange(0,1.6,0.1) 
    #var_contour = ax.contour(lon, lat, var, levels=levels, linewidths=1, colors='k',transform = ccrs.PlateCarree())
    #plt.clabel(var_contour,  levels, inline=True, fmt='%1i', fontsize=10)
        
    # ajout du contour du basson versant 
    colors = ['red']
    maskBV = ['Bassin versant des Outaouais']                      
    ax.plot(BV_border.X,BV_border.Y, transform=ccrs.PlateCarree(), color=colors[0], linewidth=2, label=maskBV[0])
    plt.legend(loc="best", markerscale=2., fontsize=20)
    # Define gridline locations and draw the lines using cartopy's built-in gridliner:
    xticks = np.arange(-150.0,-40.0,20)
    yticks =np.arange(10,80,10)    
    fig.canvas.draw()    

    cbar = plt.colorbar(mm, orientation='horizontal', shrink=0.75, drawedges='True', ticks=np.arange(0.8, 1., .02),extend='both')
    cbar.set_label(u'\n DAYMET - Lambert Conformal Conic - Résolution: 1km \nDonnées archivées et distribuées par ORNL DAAC', size='medium') # Affichage de la légende de la barre de couleur
    cbar.ax.tick_params(labelsize=17)  
    
    plt.xlabel(u'\Daily minimum temperature (Celcius)',size='x-large')
    string_title=u'Spearman Correlation daily minimum temperature Daymet/ERA5 \n ' + monthstr + ' reference period 1990-2019\n'
    plt.title(string_title, size='xx-large')
    plt.savefig('./figures/Spearman_DAYMET_ERA5_Tmin_1990-2019_'+str(month)+'_matlab.png', bbox_inches='tight', pad_inches=0.1)
    plt.show()  
    plt.close()
    
    
    
    
    
    
