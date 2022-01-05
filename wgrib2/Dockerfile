# ======================================================================
# Dockerfile to compile wgrib2 based on Alpine linux
#
#           Homepage: http://www.cpc.ncep.noaa.gov/products/wesley/wgrib2/
# Available versions: ftp://ftp.cpc.ncep.noaa.gov/wd51we/wgrib2/
# ======================================================================

FROM ubuntu:20.04 AS base

ENV CC=gcc
ENV FC=gfortran

RUN apt-get update
RUN apt-get install -y build-essential gfortran wget file pip

RUN wget -q -O /tmp/wgrib2.tgz https://ftp.cpc.ncep.noaa.gov/wd51we/wgrib2/wgrib2.tgz

RUN tar -xf /tmp/wgrib2.tgz -C /tmp

WORKDIR /tmp/grib2
RUN ls -l

RUN sed -i "s|MAKE_SHARED_LIB=0|MAKE_SHARED_LIB=1|g" makefile

RUN make lib

#RUN mkdir -p .local/lib/python3.8/site-packages

RUN cp /tmp/grib2/lib/libwgrib2.so /usr/lib/python3.8/libwgrib2.so

RUN python3 -m pip install numpy boto3 netCDF4

RUN wget -q -O /usr/lib/python3.8/pywgrib2_s.py https://ftp.cpc.ncep.noaa.gov/wd51we/pywgrib2_s/pywgrib2_s/pywgrib2_s.py

ENTRYPOINT ["python3"]