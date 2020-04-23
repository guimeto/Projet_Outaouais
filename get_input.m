function InRealArr = get_input(targetDir, InFile)

%
% Author: Milka Radojevic, MSc in atmospheric sciences
% Institution: UQAM (Centre ESCER) & Environment Canada (CMC)
% Date: June 4th, 2012

% Description:
% Read input file if given in NetCDF data format

% Version 2.0

% Trick to copy long filename to working directory
% Note: in Matlab, filename longer than 68 chars is not allowed
if exist( InFile, 'file' ) == 0, 
 
curDir = pwd;  % save current directory location     

    if exist( char(targetDir), 'dir' ) == 7,    
        cd(char(targetDir)); % enter target directory
            % copy NetCDf file from targetDir
            copyfile(char(InFile),char(curDir),'f'); 
        cd(char(curDir));  % re-enter current working directory
    else
        'Attention: no such directory name or path incorect !';
    end

end
        
        
% open InFile & read
ncid = netcdf.open(InFile,'NC_NOWRITE');

    % Get varid and add_offset & scale_factor attributs from NetCDF
    [varid, add_offset, scale_factor] = get_varattributs(ncid);
    InArr = netcdf.getVar(ncid,varid,'double');
    
netcdf.close(ncid); % close InFile 


% Compute real values of InStrr
InRealArr = (InArr * scale_factor) + add_offset; 
clear InStrr;
    

end