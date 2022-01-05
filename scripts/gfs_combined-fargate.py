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
bucket         = os.environ['bucket']
download_path  = os.environ['download_path'] 
time_in        = os.environ['time']
temp_path      = os.environ['temp_path']

datetime_IN    = datetime.strptime(time_in,"%Y-%m-%dT%H:%M:%S%z")
datetime_RUN   = datetime_RUN = datetime_IN - timedelta(hours=5)

fDate          = datetime_RUN.strftime("%Y%m%d")
runTime        = "t" + datetime_RUN.strftime("%H") + "z"

print(time_in)
print(datetime_IN)
print(datetime_RUN)
print(fDate)
print(runTime)

# Setup paths
prod_A = 'gfs2'  #GFS

if not os.path.exists(download_path + '/' + prod_A):
    os.makedirs(download_path + '/' + prod_A)
if not os.path.exists(download_path + '/' + prod_A + '/' + fDate):
    os.makedirs(download_path + '/' + prod_A + '/' + fDate)
if not os.path.exists(download_path + '/' + prod_A + '/' + fDate + '/' + runTime):
    os.makedirs(download_path + '/' + prod_A + '/' + fDate + '/' + runTime)

# Merge paths
download_path_CK = download_path + '/' + prod_A + '/' + fDate + '/' + runTime + '/' + 'out_' + prod_A + '_chunked.nc'
download_path_NC = temp_path + '/' + prod_A + '_tmp.nc'


# Setup download file range
gfs_range1 = range(1,121)
gfs_range2 = range(123,241,3)
ncFileRange = [*gfs_range1, *gfs_range2]
#ncFileRange = range(3,241,3)
#ncFileRange = range(1,3,1)

ncTimeCount = 0

for ncFileName in ncFileRange:
  # Two loops for primary and b files
  grbTypes = ['pgrb2', 'pgrb2b']
  
  for grbType in  grbTypes:
    # Define download destination path
    #download_file_path = download_path + '/gfs2/' + fDate + '/' + runTime + '/download/' + 'gfs.f' + str(ncFileName).zfill(3) + '.' + grbType + '.grb'
    download_file_path = temp_path + '/gfs.f' + str(ncFileName).zfill(3) + '.' + grbType + '.grb'
    

    # Download from S3
    s3_filename = 'gfs.' + fDate + '/' + runTime[1:3] + '/atmos/gfs.' + runTime + '.' + grbType + '.0p25.f' + str(ncFileName).zfill(3)
    s3_client.download_file(bucket, s3_filename, download_file_path)
    
    
    if grbType == 'pgrb2':
      # Define temp path
      download_file_pathA = temp_path + '/gfs.f' + str(ncFileName).zfill(3) + '.' + grbType + '.grb'

      #download_path_GB_A = download_pathA + '/gfs2/' + fDate + '/' + runTime + '/gribs/' + 'gfs.f' + str(ncFileName).zfill(3) + '.' + grbType + '.earth.grb'
      download_path_GB_A = download_file_pathA + '.earth'

      matchString = (":(DPT:2 m above ground|TMP:2 m above ground|CRAIN:surface:.*hour fcst|"
                "CSNOW:surface:.*hour fcst|CFRZR:surface:.*hour fcst|"
                "PRATE:surface:.*hour fcst|PRES:surface|TOZNE|"
                "UGRD:10 m above ground:.*hour fcst|VGRD:10 m above ground:.*hour fcst|"
                "VIS:surface|GUST:surface:.*hour fcst|"
                "RH:2 m above ground:.*hour fcst|CICEP:surface:.*hour fcst|TOZNE):")

      pywgrib2_s.wgrib2([download_file_pathA, '-match', matchString, '-append', "-grib_out", download_path_GB_A])
      pywgrib2_s.wgrib2([download_file_pathA, '-rewind_init', download_file_pathA, '-match', 'APCP', '-append', '-grib', download_path_GB_A, '-quit'])
      pywgrib2_s.wgrib2([download_file_pathA, '-rewind_init', download_file_pathA, '-match', 'TCDC:entire atmosphere', '-append', '-grib', download_path_GB_A, '-quit'])
      pywgrib2_s.close(download_file_pathA)
        
    if grbType == 'pgrb2b':
      # Define temp path 
      download_file_pathB = temp_path + '/gfs.f' + str(ncFileName).zfill(3) + '.' + grbType + '.grb'

      #download_path_GB_B = download_path + '/gfs2/' + fDate + '/' + runTime + '/gribs/' + 'gfs.f' + str(ncFileName).zfill(3) + '.' + grbType + '.earth.grb'
      download_path_GB_B = download_file_pathB + '.earth'

      pywgrib2_s.wgrib2([download_file_pathB, '-match', '(:DUVB:surface:)', '-append', '-grib_out', download_path_GB_B])
      pywgrib2_s.close(download_file_pathB)
  
  
  ### Merge ###
  #print('##File 1##')
  pywgrib2_s.wgrib2([download_path_GB_A, '-append', '-netcdf', download_path_NC])

  #print('##File 2##')
  pywgrib2_s.wgrib2([download_path_GB_B, '-append', '-netcdf', download_path_NC])
  
  pywgrib2_s.close(download_path_GB_A)
  os.remove(download_path_GB_A)
  pywgrib2_s.close(download_path_GB_B)
  os.remove(download_path_GB_B)
  os.remove(download_file_pathA)
  os.remove(download_file_pathB)
  
 
# Remove Chunk file if exists
if os.path.isfile(download_path_CK):
  os.remove(download_path_CK)

if os.path.isfile(download_path  + '/' + prod_A + '/' + fDate + '/' + runTime + '/' + prod_A + '.done'):
  os.remove(download_path  + '/' + prod_A + '/' + fDate + '/' + runTime + '/' +  prod_A + '.done')


print('###Chunk')
chk = Dataset(download_path_CK, "w")
src = Dataset(download_path_NC, 'r', format="NETCDF3_CLASSIC")  

# Save Lat Lon
lats = src.variables['latitude'][:]
lons = src.variables['longitude'][:]

np.save(download_path  + '/' + prod_A + '/' + prod_A + '-lats.npy', lats.data)
np.save(download_path  + '/' + prod_A + '/' + prod_A + '-lons.npy', lons.data)


# copy global attributes all at once via dictionary
chk.setncatts(src.__dict__)

# copy dimensions
for name, dimension in src.dimensions.items():
  chk.createDimension(name, (len(dimension) if not dimension.isunlimited() else None))
# copy all file data except for the excluded
for name, variable in src.variables.items():
  print('##DIM##')
  print(len(variable.dimensions))
  print(variable.shape)
  if len(variable.dimensions)==3:
      if 'PRATE_surface' in name:
          x = chk.createVariable(name, variable.datatype, variable.dimensions, chunksizes=[160,2,4], zlib=True, least_significant_digit=4, complevel=1)
      elif 'APCP_surface' in name:
          x = chk.createVariable(name, variable.datatype, variable.dimensions, chunksizes=[160,2,4], zlib=True, least_significant_digit=4, complevel=1)
      else:
          x = chk.createVariable(name, variable.datatype, variable.dimensions, chunksizes=[160,2,4], zlib=True, least_significant_digit=1, complevel=1)
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
f = open(download_path  + '/' + prod_A + '/' + fDate + '/' + runTime + '/' + prod_A + '.done', "w")
f.write(download_path_CK)
f.close()





















