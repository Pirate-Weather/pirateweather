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
datetime_RUN   = datetime_RUN = datetime_IN - timedelta(hours=7)

fDate          = datetime_RUN.strftime("%Y%m%d")
runTime        = "t" + datetime_RUN.strftime("%H") + "z"

print(time_in)
print(datetime_IN)
print(datetime_RUN)
print(fDate)
print(runTime)

# Setup paths
prod_A = 'gefs2'  #GEFS
prod_B = 'gefsa2' #GFS Averaged

if not os.path.exists(download_path + '/' + prod_A):
    os.makedirs(download_path + '/' + prod_A)
if not os.path.exists(download_path + '/' + prod_A + '/' + fDate):
    os.makedirs(download_path + '/' + prod_A + '/' + fDate)
if not os.path.exists(download_path + '/' + prod_A + '/' + fDate + '/' + runTime):
    os.makedirs(download_path + '/' + prod_A + '/' + fDate + '/' + runTime)

if not os.path.exists(download_path + '/' + prod_B):
    os.makedirs(download_path + '/' + prod_B)
if not os.path.exists(download_path + '/' + prod_B + '/' + fDate):
    os.makedirs(download_path + '/' + prod_B + '/' + fDate)
if not os.path.exists(download_path + '/' + prod_B + '/' + fDate + '/' + runTime):
    os.makedirs(download_path + '/' + prod_B + '/' + fDate + '/' + runTime)


# Merge paths
download_path_CK     = download_path + '/' + prod_A + '/' + fDate + '/' + runTime + '/' + 'out_' + prod_A + '_chunked.nc'
download_path_CK_AVG = download_path + '/' + prod_B + '/' + fDate + '/' + runTime + '/' + 'out_' + prod_B + '_chunked.nc'

download_path_NC_A  = temp_path + '/' + prod_A + '_tmp.nc'
download_path_NC_B  = temp_path + '/' + prod_B + '_tmp.nc'

# Setup download file range
ncFileRange = range(3,241,3)
# ncFileRange = range(3,9,3)

ncTimeCount = 0

for ncFileName in ncFileRange:
  # Two loops for regular and averaged 
  grbTypes = ['gep', 'geavg']
  
  for grbType in grbTypes:
    if grbType == 'gep':

        # Loop through ensemble members
        ensFileRange = range(1, 31)
        download_path_GB_EN   =  temp_path + '/gep.f' + str(ncFileName).zfill(3) + '.' + grbType + '.grb' + '.ens'
        download_path_GB_ENP  =  temp_path + '/gep.f' + str(ncFileName).zfill(3) + '.' + grbType + '.grb' + '.enp'
        download_path_GB_ENP2 =  temp_path + '/gep.f' + str(ncFileName).zfill(3) + '.' + grbType + '.grb' + '.enp2'

        for ensFileName in ensFileRange:
            # Define temp path
            download_file_pathA  = temp_path + '/gep' + str(ensFileName).zfill(2) + '.f' + str(ncFileName).zfill(3) + '.' + grbType + '.grb'

            # Download from S3
            s3_filename = 'gefs.' + fDate + '/' + runTime[1:3] + '/atmos/pgrb2sp25/gep' + str(ensFileName).zfill(2) + '.' + runTime + '.pgrb2s.0p25.f' + str(ncFileName).zfill(3)
            s3_client.download_file(bucket, s3_filename, download_file_pathA)

            # Append precpn to ensemble file and remove member
            pywgrib2_s.wgrib2([download_file_pathA, '-match', 'APCP', '-append', "-grib_out", download_path_GB_EN])
            pywgrib2_s.close(download_file_pathA)
            os.remove(download_file_pathA)
    
        ### Ens processing at each time step
        # Ensemble processing and extract spread
        pywgrib2_s.wgrib2([download_path_GB_EN, '-ens_processing', download_path_GB_ENP, '0']) 
        pywgrib2_s.close(download_path_GB_ENP)
        matchString = (":(ens spread):")
        pywgrib2_s.wgrib2([download_path_GB_ENP, '-match', matchString, '-set_ext_name', '1', '-append', '-netcdf', download_path_NC_A])

        # Process ensemble using rpn and extract mean
        pywgrib2_s.wgrib2([download_path_GB_EN, '-rewind_init', download_path_GB_EN, '-rpn', '1:>=', '-ens_processing', download_path_GB_ENP2, '0']) 
        pywgrib2_s.close(download_path_GB_ENP2) 
        matchString = (":(ens mean):")
        pywgrib2_s.wgrib2([download_path_GB_ENP2, '-match', matchString, '-set_prob', '1', '1', '1', '1', '1', '-set_ext_name', '1', '-append', '-netcdf', download_path_NC_A])

        pywgrib2_s.close(download_path_GB_EN)
        pywgrib2_s.close(download_path_GB_ENP)
        pywgrib2_s.close(download_path_GB_ENP2)

        os.remove(download_path_GB_EN)
        os.remove(download_path_GB_ENP)
        os.remove(download_path_GB_ENP2)

    if grbType == 'geavg':
        # Averaged
        # Define temp paths
        download_file_pathB = temp_path + '/gefs.f' + str(ncFileName).zfill(3) + '.' + grbType + '.grb'
        download_path_GB_B = download_file_pathB + '.earth'
        # Download from S3
        s3_filename = 'gefs.' + fDate + '/' + runTime[1:3] + '/atmos/pgrb2sp25/geavg.' + runTime + '.pgrb2s.0p25.f' + str(ncFileName).zfill(3)
        # print(bucket)
        # print(s3_filename)
        s3_client.download_file(bucket, s3_filename, download_file_pathB)

        matchString = (":(CRAIN|"
                  "CSNOW|CFRZR|"
                  "PRATE|CICEP):")
    
        pywgrib2_s.wgrib2([download_file_pathB, '-match', matchString, '-append', "-grib_out", download_path_GB_B])
        a = pywgrib2_s.wgrib2([download_file_pathB, '-rewind_init', download_file_pathB, '-match', 'APCP', '-append', '-grib', download_path_GB_B, '-quit'])

        ### Merge and Remove ###
        pywgrib2_s.wgrib2([download_path_GB_B, '-append', '-netcdf', download_path_NC_B])

        pywgrib2_s.close(download_path_GB_B)
        os.remove(download_path_GB_B)
        os.remove(download_file_pathB)


# Remove Chunk file if exists
if os.path.isfile(download_path_CK):
  os.remove(download_path_CK)
if os.path.isfile(download_path  + '/' + prod_A + '/' + fDate + '/' + runTime + '/' + prod_A + '.done'):
  os.remove(download_path  + '/' + prod_A + '/' + fDate + '/' + runTime + '/' + prod_A + '.done')

if os.path.isfile(download_path_CK_AVG):
  os.remove(download_path_CK_AVG)
if os.path.isfile(download_path  + '/' + prod_B + '/' + fDate + '/' + runTime + '/' + prod_B + '.done'):
  os.remove(download_path  + '/' + prod_B + '/' + fDate + '/' + runTime + '/' + prod_B + '.done')

print('###Chunk')
chkA    = Dataset(download_path_CK, "w")
chkB    = Dataset(download_path_CK_AVG, "w")

srcA    = Dataset(download_path_NC_A, 'r', format="NETCDF3_CLASSIC")  
srcB    = Dataset(download_path_NC_B, 'r', format="NETCDF3_CLASSIC")  

# copy global attributes all at once via dictionary
for grbType in grbTypes:
    if grbType == 'gep':
        src = srcA
        chk = chkA
        chk.setncatts(srcA.__dict__)
        prod = prod_A
    elif grbType == 'geavg':
        src = srcB
        chk = chkB
        chk.setncatts(srcB.__dict__)
        prod = prod_B
        
    # Save Lat Lon
    lats = src.variables['latitude'][:]
    lons = src.variables['longitude'][:]

    np.save(download_path  +'/' + prod + '/' + prod + '-lats.npy', lats.data)
    np.save(download_path  + '/' + prod + '/' + prod + '-lons.npy', lons.data)


    # copy dimensions for srcA and srcB
    for name, dimension in src.dimensions.items():
        chk.createDimension(name, (len(dimension) if not dimension.isunlimited() else None))
    # copy all file data except for the excluded
    for name, variable in src.variables.items():
        print('##DIM##')
        print(len(variable.dimensions))
        print(variable.shape)
        if len(variable.dimensions)==3:
                if 'APCP_surface' in name:
                    x = chk.createVariable(name, variable.datatype, variable.dimensions, chunksizes=[80,7,7], zlib=True, least_significant_digit=4, complevel=1)
                elif len(variable.dimensions)==3:
                    x = chk.createVariable(name, variable.datatype, variable.dimensions, chunksizes=[80,7,7], zlib=True, least_significant_digit=2, complevel=1)
                else:
                    x = chk.createVariable(name, variable.datatype, variable.dimensions)
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
for runPath in range(0, 2):
    if runPath == 0:
        runDatesPath   = download_path + '/' + prod_A
    elif  runPath == 1:
        runDatesPath   = download_path + '/' + prod_B

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
f = open(download_path + '/' + prod_B + '/' + fDate + '/' + runTime + '/' + prod_B + '.done', "w")
f.write(download_path_CK_AVG)
f.close()



















