function [varid, add_offset, scale_factor, latid, lonid] ...
    = get_varattributs(ncid)
% Returns information about variable and attributes in a NetCDF file

% Version 2.0 of April 2012
% Created by Milka Radojevic, August 2011
% Data Access Integration & Climate Analysis Group, Montreal, Canada

% Returns information about netCDF file ncid
[~,nvars,~,~] = netcdf.inq(ncid);
    varid = max(nvars)-1; %here, varid attributes are before general attrib
    
% Returns informations about attributes associated with the variable varid
[~,~,~,natts] = netcdf.inqVar(ncid,varid);

    for iat = 1:natts
        % get the name of the attribute associated with the variable
        attname = netcdf.inqAttName(ncid,varid,iat-1);

            % get value of add_offcale & scale_factor
            if strcmpi(attname,'add_offset'),
                add_offset = netcdf.getAtt(ncid,varid,attname,'double');
            elseif strcmpi(attname,'scale_factor'),
                scale_factor = netcdf.getAtt(ncid,varid,attname,'double');
            end
     end
    
 % if there is no desired attributes, their value is set to zero
 if exist('add_offset','var') == 0, 
     add_offset = 0; 
 end
 %
 if exist('scale_factor','var') == 0, 
     scale_factor = 1; 
 end
 
 
 % Added on April 19th, 2012 by Milka Radojevic, UQAM, Montreal
 % Find all attributes in the header 
  for attid = 1:max(nvars) % No of the attributs (start with zero)
 
      % No of characteristics in each attribute
      [~,~,~,NoAttChar] = netcdf.inqVar(ncid,attid-1);
 
      % Find name of each characteristics
      for iachar = 1:NoAttChar
         AttName = netcdf.inqAttName(ncid,attid-1,iachar-1);
         AttNameVal = netcdf.getAtt(ncid,attid-1,AttName);
         if strcmpi(AttNameVal,'longitude'),
            lonid = attid-1;
         elseif strcmpi(AttNameVal,'latitude'),
            latid = attid-1;
         end
        
         clear AttName AttNameVal;
      end
      clear NoAttChar;
  
end
