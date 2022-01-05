### Ingest script for docker image for hourly HRRR products

import os
import json
import boto3
from botocore import UNSIGNED
from botocore.client import Config
import os
import shutil
import sys
import uuid
from urllib.parse import unquote_plus
import pywgrib2_s

from netCDF4 import Dataset
import numpy as np
from netCDF4 import MFDataset

from datetime import datetime, timedelta

s3_client = boto3.client('s3', config=Config(signature_version=UNSIGNED))
s3 = boto3.resource('s3')


# Set variables from ENV
bucket              = os.environ['bucket']
download_path       = os.environ['download_path'] 
time_in             = os.environ['time']
temp_path           = os.environ['temp_path']

# 2 hour 30 minute delay
datetime_IN    = datetime.strptime(time_in,"%Y-%m-%dT%H:%M:%S%z")
datetime_RUN   = datetime_RUN = datetime_IN - timedelta(hours=2, minutes=30)

fDate          = datetime_RUN.strftime("%Y%m%d")
runTime        = "t" + datetime_RUN.strftime("%H") + "z"

print(time_in)
print(datetime_IN)
print(datetime_RUN)
print(fDate)
print(runTime)

# Setup paths
prod_A = 'hrrr6h2'  #Hourly HRRR + 18
if not os.path.exists(download_path + '/' + prod_A):
    os.makedirs(download_path + '/' + prod_A)
if not os.path.exists(download_path + '/' + prod_A + '/' + fDate):
    os.makedirs(download_path + '/' + prod_A + '/' + fDate)
if not os.path.exists(download_path + '/' + prod_A + '/' + fDate + '/' + runTime):
    os.makedirs(download_path + '/' + prod_A + '/' + fDate + '/' + runTime)

# Merge paths
download_path_CK     = download_path + '/' + prod_A + '/' + fDate + '/' + runTime + '/' + 'out_' + prod_A + '_chunked.nc'

download_path_NC_A  = temp_path + '/' + prod_A + '_tmp.nc'

# Setup download file range
ncFileRange_A = rncFileRange = range(19, 49)

# Setup grid transformation
HRRR_grid1 = 'lambert:262.500000:38.500000:38.500000:38.500000'
HRRR_grid2 = '237.280472:1799:3000.000000'
HRRR_grid3 = '21.138123:1059:3000.000000'


# hrrr6h2
# HRRRH
grbType = 'wrfsfc'
for ncFileName in ncFileRange_A:
    download_file_pathA  = temp_path + '/hrrrh.f' + str(ncFileName).zfill(3) + '.' + grbType + '.grb'
    download_path_GB_A   = temp_path + '/hrrrh.f' + str(ncFileName).zfill(3) + '.' + grbType + '.grb.earth'

    # Download from S3
    s3_filename = 'hrrr.' + fDate + '/conus/hrrr.' + runTime + '.wrfsfcf' + str(ncFileName).zfill(2) + '.grib2'
    print(s3_filename)

    s3_client.download_file(bucket, s3_filename, download_file_pathA)

    matchString = (":(TMP:2 m above ground|CRAIN:surface|CSNOW:surface|"
                   "CFRZR:surface|PRATE:surface|PRES:surface|CICEP:surface|"
                   "UGRD:10 m above ground:.*hour fcst|"
                   "VGRD:10 m above ground:.*hour fcst|"
                   "VIS:surface|DPT:2 m above ground|TCDC:entire atmosphere|GUST:surface|RH:2 m above ground):")
    
    pywgrib2_s.wgrib2([download_file_pathA, '-new_grid_winds', 'earth', '-new_grid_interpolation', 'neighbor', '-match', matchString, '-new_grid', HRRR_grid1, HRRR_grid2, HRRR_grid3, download_path_GB_A])
    pywgrib2_s.wgrib2([download_file_pathA, '-rewind_init', download_file_pathA, '-new_grid_winds', 'earth', '-new_grid_interpolation', 'neighbor', '-match', 'APCP', '-append','-new_grid', HRRR_grid1, HRRR_grid2, HRRR_grid3, download_path_GB_A, '-quit'])
    pywgrib2_s.close(download_path_GB_A)

    # Add to NetCDF
    pywgrib2_s.wgrib2([download_path_GB_A, '-append', '-netcdf', download_path_NC_A])

    pywgrib2_s.close(download_file_pathA)
    pywgrib2_s.close(download_path_GB_A)

    os.remove(download_file_pathA)
    os.remove(download_path_GB_A)


# Remove Chunk file if exists
if os.path.isfile(download_path_CK):
  os.remove(download_path_CK)
if os.path.isfile(download_path  + '/' + prod_A + '/' + fDate + '/' + runTime + '/' + prod_A + '.done'):
        os.remove(download_path  + '/' + prod_A + '/' + fDate + '/' + runTime + '/' + prod_A + '.done')


print('###Chunk')
chkA    = Dataset(download_path_CK, "w")
srcA    = Dataset(download_path_NC_A, 'r', format="NETCDF3_CLASSIC")  

# Save Lat Lon
lats = srcA.variables['latitude'][:]
lons = srcA.variables['longitude'][:]

np.save(download_path  +'/' + prod_A + '/' + prod_A + '-lats.npy', lats.data)
np.save(download_path  + '/' + prod_A + '/' + prod_A + '-lons.npy', lons.data)

# copy global attributes all at once via dictionary
src = srcA
chk = chkA
chk.setncatts(srcA.__dict__)

# copy dimensions for srcA and srcB
for name, dimension in src.dimensions.items():
    chk.createDimension(name, (len(dimension) if not dimension.isunlimited() else None))
# copy all file data except for the excluded
for name, variable in src.variables.items():
    print('##DIM##')
    print(len(variable.dimensions))
    print(variable.shape)
    if len(variable.dimensions)==3:
        if 'PRATE_surface' in name:
            x = chk.createVariable(name, variable.datatype, variable.dimensions, chunksizes=[30, 10, 10], zlib=True, least_significant_digit=4, complevel=1)
        else:
            x = chk.createVariable(name, variable.datatype, variable.dimensions, chunksizes=[30, 10, 10], zlib=True, least_significant_digit=1, complevel=1)    
    else:
        x = chk.createVariable(name, variable.datatype, variable.dimensions)

    chk[name][:] = src[name][:]
    # copy variable attributes all at once via dictionary
    for ncattr in src[name].ncattrs():
        if ncattr != '_FillValue':
            chk[name].setncattr(ncattr, src[name].getncattr(ncattr))

src.close()
chk.close()

# Remove runs greater than a week old
for runPath in range(0, 1):
    if runPath == 0:
        runDatesPath   = download_path + '/' + prod_A

    runDates       = [f for f in os.listdir(runDatesPath) if not os.path.isfile(os.path.join(runDatesPath, f))]
    runDatesInt    = [int(i) for i in runDates]

    for g in runDatesInt:
        # Cycle through dates
        dataRuns_g      = [f for f in os.listdir(runDatesPath + '/' + str(g)) if not os.path.isfile(os.path.join(runDatesPath + '/' + str(g), f))]
        dataRunsInt_g   = [int(z[1:3]) for z in dataRuns_g]

        gfsRunDate  = datetime(int(str(g)[0:4]),
                int(str(g)[4:6]),
                int(str(g)[6:8]), 00, 00, 00)

        if gfsRunDate < (datetime.now() - timedelta(days=7)):
            shutil.rmtree(runDatesPath + '/' + str(g))
            print(runDatesPath + '/' + str(g))


# Save completion files
f = open(download_path + '/' + prod_A + '/' + fDate + '/' + runTime + '/' + prod_A + '.done', "w")
f.write(download_path_CK)
f.close()
















