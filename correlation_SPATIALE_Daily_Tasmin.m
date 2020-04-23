%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%----------------Guillaume  Dueymes  22/04/2020---------------------------%
%                                                                         %
% Programme qui calcule la correlation spatiale                           %
% entre deux fichiers netcdf
% INPUT: serie temporelle au format Netcdf par mois
%% 
%% 
% OUTPUT:champ Netcdf                                                     %
% On appelle ici les 2 sous-routines: get_input.m et get_varattributs     %
%                                                                         %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clc; clear ; 

%% 
path_daymet='K:\PROJETS\PROJET_OUTAOUAIS\Daily\tmin\';
path_era5='J:\REANALYSES\ERA5\Tmin_daily_Outaouais\';
out='K:\PROJETS\PROJET_OUTAOUAIS\Daily\Correlations\';


precision='90p';
start_year=1990;
end_year=2019;
ny=end_year-start_year+1;
List_month = {'01','02','03','04','05','06','07','08','09','10','11','12'};
for t=1:12 
         mois=char(List_month(t));
 FichierIn = char ( strcat(path_daymet,'Daymet_v3_Daily_Tasmin_1990_2019_',char(mois),'_OUTAOUAIS.nc' ));
  ncid = netcdf.open(FichierIn,'NC_NOWRITE');
  LonArr = netcdf.getVar(ncid,0);
  LatArr = netcdf.getVar(ncid,1);
  VArr_Day = netcdf.getVar(ncid,3);
 clear FichierIn    
 [lat, lon] = meshgrid(LatArr, LonArr);              
 FichierIn = char ( strcat(path_era5,'ERA5grid_Daily_Tasmin_1990_2019_',char(mois),'_OUTAOUAIS.nc' ));
 ncid = netcdf.open(FichierIn,'NC_NOWRITE');
 VArr_ERA5 = netcdf.getVar(ncid,3);      
xc = size(VArr_Day,1);
yc = size(VArr_Day,2);

for l=1:xc 
     for m=1:yc          
            A= squeeze(VArr_Day(l,m,:));       
            B= squeeze(VArr_ERA5(l,m,:));

     [RHO(l,m),PVAL(l,m)] = corr(A,B,'Type','Spearman','rows','pairwise','tail','both');
     if PVAL(l,m) <= 0.1
        RHO1(l,m)=RHO(l,m) ;
     elseif (isnan(RHO(l,m)) == 1)
        RHO1(l,m)= NaN  ; 
     elseif PVAL(l,m) > 0.1
        RHO1(l,m)= NaN  ;
     end
     clear A B
     end
end



filenc= char ( strcat(out,'Daymet_v3_spearmann_Correlation_ERA5grid_Daily_Tasmin_1990_2019_',char(mois) ,'_OUTAOUAIS_matlab.nc' ));
ncid = netcdf.create(filenc,'NC_WRITE');
% Definition des dimensions
dimid_x = netcdf.defDim(ncid,'x',xc);
dimid_y = netcdf.defDim(ncid,'y',yc); 
dimid_time = netcdf.defDim(ncid,'time',1); 
% Definition des variables
%%Longitude
varid_lon = netcdf.defVar(ncid,'lon','float',[dimid_x,dimid_y]);
netcdf.putAtt(ncid,varid_lon,'units','degrees_east');
netcdf.putAtt(ncid,varid_lon,'long_name','Longitude');
netcdf.putAtt(ncid,varid_lon,'CoordinateAxisType','Lon');
%%Latitude
varid_lat = netcdf.defVar(ncid,'lat','float',[dimid_x,dimid_y]);
netcdf.putAtt(ncid,varid_lat,'units','degrees_north')
netcdf.putAtt(ncid,varid_lat,'long_name','Latitude');
netcdf.putAtt(ncid,varid_lat,'CoordinateAxisType','Lat');
%%Temps
varid_time = netcdf.defVar(ncid,'time','double',dimid_time);
netcdf.putAtt(ncid,varid_time,'long_name','Time');
netcdf.putAtt(ncid,varid_time,'delta_t','');
%%Indice de vague de chaleur
varid_hwdi = netcdf.defVar(ncid,'Spearmanr','float',[dimid_x,dimid_y,dimid_time]);
netcdf.putAtt(ncid,varid_hwdi,'long_name','');
netcdf.putAtt(ncid,varid_hwdi,'units','');
netcdf.putAtt(ncid,varid_hwdi,'missing_value',-999);
netcdf.putAtt(ncid,varid_hwdi,'coordinates','lon lat');

%%fermeture du fichier netcdf 
netcdf.endDef(ncid)

% % % Ecrire les variables
netcdf.putVar(ncid,varid_lon,lon);
netcdf.putVar(ncid,varid_lat,lat);
netcdf.putVar(ncid,varid_time,1);
netcdf.putVar(ncid,varid_hwdi,RHO1);
netcdf.close(ncid);   

clear IndArr RHO PVAL RHO1 TempArr
 
end  
  
