# Ingest script for docker image for hourly HRRR products

import json
import os
import shutil
import sys
import uuid
from datetime import datetime, timedelta
from urllib.parse import unquote_plus

import boto3
import numpy as np
import pywgrib2_s
from botocore import UNSIGNED
from botocore.client import Config
from netCDF4 import Dataset, MFDataset

s3_client = boto3.client('s3', config=Config(signature_version=UNSIGNED))
s3 = boto3.resource('s3')


# Set variables from ENV
bucket = os.environ['bucket']
download_path = os.environ['download_path']
time_in = os.environ['time']
temp_path = os.environ['temp_path']

# 1 hour 45 minute delay
datetime_IN = datetime.strptime(time_in, "%Y-%m-%dT%H:%M:%S%z")
datetime_RUN = datetime_RUN = datetime_IN - timedelta(hours=1, minutes=45)

fDate = datetime_RUN.strftime("%Y%m%d")
runTime = "t" + datetime_RUN.strftime("%H") + "z"

print(time_in)
print(datetime_IN)
print(datetime_RUN)
print(fDate)
print(runTime)

# Setup paths

prod_A = 'subh2'  # SubHourly HRRR
prod_B = 'hrrrh2'  # Hourly HRRR
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
download_path_CK = download_path + '/' + prod_A + '/' + \
    fDate + '/' + runTime + '/' + 'out_' + prod_A + '_chunked.nc'
download_path_CK_B = download_path + '/' + prod_B + '/' + \
    fDate + '/' + runTime + '/' + 'out_' + prod_B + '_chunked.nc'

download_path_NC_A = temp_path + '/' + prod_A + '_tmp.nc'
download_path_NC_B = temp_path + '/' + prod_B + '_tmp.nc'

# Setup download file range
ncFileRange_A = range(1, 5)
ncFileRange_B = range(1, 19)

# Setup grid transformation
HRRR_grid1 = 'lambert:262.500000:38.500000:38.500000:38.500000'
HRRR_grid2 = '237.280472:1799:3000.000000'
HRRR_grid3 = '21.138123:1059:3000.000000'


# SUBH
grbType = 'wrfsubhf'
for ncFileName in ncFileRange_A:
    download_file_pathA = temp_path + '/subh.f' + \
        str(ncFileName).zfill(3) + '.' + grbType + '.grb'
    download_path_GB_A = temp_path + '/subh.f' + \
        str(ncFileName).zfill(3) + '.' + grbType + '.grb.earth'
    # Download from S3
    s3_filename = 'hrrr.' + fDate + '/conus/hrrr.' + runTime + \
        '.wrfsubhf' + str(ncFileName).zfill(2) + '.grib2'
    print(s3_filename)

    s3_client.download_file(bucket, s3_filename, download_file_pathA)

    matchString = (":(TMP:2 m above ground|CRAIN:surface|CSNOW:surface|"
                   "CFRZR:surface|PRATE:surface|PRES:surface|CICEP:surface|"
                   "UGRD:10 m above ground:.*min fcst|"
                   "VGRD:10 m above ground:.*min fcst|"
                   "VIS:surface|DPT:2 m above ground|APCP:surface|"
                   "TCDC:entire atmosphere|GUST:surface):")

    # ((15|30|45|60|75|90|105|120|135|150|165|180|"
    # "195|210|225|240|300|360|420|480|540|600|660|720|780|840|900|960|1020|1080) min fcst|.*acc fcst):")

    # Convert to earth oriented winds and select variables
    pywgrib2_s.wgrib2([download_file_pathA, '-new_grid_winds', 'earth', '-new_grid_interpolation', 'neighbor', '-match', matchString,
                       '-new_grid', HRRR_grid1, HRRR_grid2, HRRR_grid3, download_path_GB_A])
    pywgrib2_s.close(download_path_GB_A)

    # Add to NetCDF
    pywgrib2_s.wgrib2([download_path_GB_A, '-append',
                      '-netcdf', download_path_NC_A])

    pywgrib2_s.close(download_file_pathA)
    pywgrib2_s.close(download_path_GB_A)

    os.remove(download_file_pathA)
    os.remove(download_path_GB_A)

# HRRRH
grbType = 'wrfsfc'
for ncFileName in ncFileRange_B:
    download_file_pathB = temp_path + '/hrrrh.f' + \
        str(ncFileName).zfill(3) + '.' + grbType + '.grb'
    download_path_GB_B = temp_path + '/hrrrh.f' + \
        str(ncFileName).zfill(3) + '.' + grbType + '.grb.earth'

    # Download from S3
    s3_filename = 'hrrr.' + fDate + '/conus/hrrr.' + runTime + \
        '.wrfsfcf' + str(ncFileName).zfill(2) + '.grib2'
    print(s3_filename)

    s3_client.download_file(bucket, s3_filename, download_file_pathB)

    matchString = (":(TMP:2 m above ground|CRAIN:surface|CSNOW:surface|"
                   "CFRZR:surface|PRATE:surface|PRES:surface|CICEP:surface|"
                   "UGRD:10 m above ground:.*hour fcst|"
                   "VGRD:10 m above ground:.*hour fcst|"
                   "VIS:surface|DPT:2 m above ground|TCDC:entire atmosphere|GUST:surface|RH:2 m above ground):")

    pywgrib2_s.wgrib2([download_file_pathB, '-new_grid_winds', 'earth', '-new_grid_interpolation', 'neighbor',
                      '-match', matchString, '-new_grid', HRRR_grid1, HRRR_grid2, HRRR_grid3, download_path_GB_B])
    pywgrib2_s.wgrib2([download_file_pathB, '-rewind_init', download_file_pathB, '-new_grid_winds', 'earth', '-new_grid_interpolation',
                      'neighbor', '-match', 'APCP', '-append', '-new_grid', HRRR_grid1, HRRR_grid2, HRRR_grid3, download_path_GB_B, '-quit'])
    pywgrib2_s.close(download_path_GB_B)
    # Add to NetCDF
    pywgrib2_s.wgrib2([download_path_GB_B, '-append',
                      '-netcdf', download_path_NC_B])

    pywgrib2_s.close(download_file_pathB)
    pywgrib2_s.close(download_path_GB_B)

    os.remove(download_file_pathB)
    os.remove(download_path_GB_B)


# Remove Chunk file if exists
if os.path.isfile(download_path_CK):
    os.remove(download_path_CK)
if os.path.isfile(download_path + '/' + prod_A + '/' + fDate + '/' + runTime + '/' + prod_A + '.done'):
    os.remove(download_path + '/' + prod_A + '/' + fDate +
              '/' + runTime + '/' + prod_A + '.done')

if os.path.isfile(download_path_CK_B):
    os.remove(download_path_CK_B)
if os.path.isfile(download_path + '/' + prod_B + '/' + fDate + '/' + runTime + '/' + prod_B + '.done'):
    os.remove(download_path + '/' + prod_B + '/' + fDate +
              '/' + runTime + '/' + prod_B + '.done')

print('###Chunk')
chkA = Dataset(download_path_CK, "w")
chkB = Dataset(download_path_CK_B, "w")

srcA = Dataset(download_path_NC_A, 'r', format="NETCDF3_CLASSIC")
srcB = Dataset(download_path_NC_B, 'r', format="NETCDF3_CLASSIC")

# copy global attributes all at once via dictionary
grbTypes = ['wrfsubhf', 'wrfsfc']
for grbType in grbTypes:
    if grbType == 'wrfsubhf':
        src = srcA
        chk = chkA
        chk.setncatts(srcA.__dict__)
        prod = prod_A
    elif grbType == 'wrfsfc':
        src = srcB
        chk = chkB
        chk.setncatts(srcB.__dict__)
        prod = prod_B

    # Save Lat Lon
    lats = src.variables['latitude'][:]
    lons = src.variables['longitude'][:]

    np.save(download_path + '/' + prod + '/' + prod + '-lats.npy', lats.data)
    np.save(download_path + '/' + prod + '/' + prod + '-lons.npy', lons.data)

    # copy dimensions for srcA and srcB
    for name, dimension in src.dimensions.items():
        chk.createDimension(
            name, (len(dimension) if not dimension.isunlimited() else None))
    # copy all file data except for the excluded
    for name, variable in src.variables.items():
        print('##DIM##')
        print(len(variable.dimensions))
        print(variable.shape)
        if len(variable.dimensions) == 3:
            if 'PRATE_surface' in name:
                x = chk.createVariable(name, variable.datatype, variable.dimensions, chunksizes=[
                                       18, 10, 10], zlib=True, least_significant_digit=4, complevel=1)
            else:
                x = chk.createVariable(name, variable.datatype, variable.dimensions, chunksizes=[
                                       18, 10, 10], zlib=True, least_significant_digit=1, complevel=1)
        else:
            x = chk.createVariable(
                name, variable.datatype, variable.dimensions)

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
        runDatesPath = download_path + '/' + prod_A
    elif runPath == 1:
        runDatesPath = download_path + '/' + prod_B

    runDates = [f for f in os.listdir(runDatesPath) if not os.path.isfile(
        os.path.join(runDatesPath, f))]
    runDatesInt = [int(i) for i in runDates]

    for g in runDatesInt:
        # Cycle through dates
        dataRuns_g = [f for f in os.listdir(runDatesPath + '/' + str(
            g)) if not os.path.isfile(os.path.join(runDatesPath + '/' + str(g), f))]
        dataRunsInt_g = [int(z[1:3]) for z in dataRuns_g]

        gfsRunDate = datetime(int(str(g)[0:4]),
                              int(str(g)[4:6]),
                              int(str(g)[6:8]), 00, 00, 00)

        if gfsRunDate < (datetime.now() - timedelta(days=7)):
            shutil.rmtree(runDatesPath + '/' + str(g))
            print(runDatesPath + '/' + str(g))


# Save completion files
f = open(download_path + '/' + prod_A + '/' + fDate +
         '/' + runTime + '/' + prod_A + '.done', "w")
f.write(download_path_CK)
f.close()
f = open(download_path + '/' + prod_B + '/' + fDate +
         '/' + runTime + '/' + prod_B + '.done', "w")
f.write(download_path_CK_B)
f.close()
