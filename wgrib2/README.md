# pywgrib2 Docker container

This is a docker container setup to download and compile the latest pywgrib2 prgram. It's designed with a "from scratch" approach, compiling the raw source on an ubuntu 20:04 base image. 
The image contains the wgrib2 libraries, python 3.8, as well as numpy. Additional Python modules will be added later.  

# Usage

This is a work in progress image, and significant changes should be expected. The plan is to use it via a volume mounted that contains the Python script to run.  