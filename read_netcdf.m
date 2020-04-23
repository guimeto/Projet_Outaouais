function [InArrReal, LatArr, LonArr] = read_netcdf(InFile)
 
  % open InFile & read
    ncid = netcdf.open(InFile,'NC_NOWRITE');
    
    % get varid and add_offset & scale_factor attributs from NetCDF
      [varid, latid, lonid] = get_varattributs(ncid);
        
        InArr = netcdf.getVar(ncid,varid,'double');
        LatArr = netcdf.getVar(ncid,latid,'double');
        LonArr = netcdf.getVar(ncid,lonid,'double');
        
    netcdf.close(ncid); %close InFile 
  
    % get real values for InStrr
      InArrReal = (InArr * scale_factor) + add_offset; 
      clear InStrr;
    
end
       

    