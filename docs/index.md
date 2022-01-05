# Pirate Weather V1.0
Weather forecasts are primarily found using models run by government agencies, but the [outputs](https://weather.gc.ca/grib/what_is_GRIB_e.html) aren't easy to use or in formats built for the web.
To try to address this, I've put together a service that reads weather forecasts and serves it following the [Dark Sky API](https://web.archive.org/web/20200723173936/https://darksky.net/dev/docs) style. Key details about setup/ usage of the API are on the main website <https://pirateweather.net/>, but I also wanted to give an overview of how I assembled all the pieces. I used many online guides during this process, so wanted to try to help someone else here! 

Before going any farther, I wanted to add a link to support this project. Running this on AWS means that it scales beautifully and is incredibly reliable, but also costs real money. I'd love to keep this project going long-term, but I'm still paying back my student loans and my AWS credits won't last forever, which limits how much I can spend on this! Anything helps, and a $2 monthly donation lets me raise your API limit from 20,000 calls/ month to 50,000 calls per month.

<a href="https://www.buymeacoffee.com/pirateweather" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>

Alternatively, I also have a GitHub Sponsorship page setup on my [profile](https://github.com/sponsors/alexander0042/)!

This project (especially the free tier) wouldn't be possibile without the ongoing support from the project sponsors, so they're the [heros here](https://github.com/sponsors/alexander0042/)! 


## Recent Updates- Spring 2021
1. Implemented historic data retrieval (Dark Sky's Time Machine function).
2. Added a front-end viewer <https://weather.pirateweather.net/>.
3. Improved the precipitation probabilities (ensemble members with accumulations greater than 1 mm, instead of 0 mm).
4. Fixed things that broke due to the new version of the GFS/ GEFS models.
5. Several other small bug fixes, including improving the icon selection logic and UV index. 

## Background
This project started from two points: as part of my [PhD](https://coastlines.engineering.queensu.ca/dunexrt), I had to become very familiar with working with NOAA forecast results (<https://orcid.org/0000-0003-4725-3251>). Separately, an old tablet set up as a "Magic Mirror,” and was using a [weather module](https://github.com/jclarke0000/MMM-DarkSkyForecast) that relied on the Dark Sky API, as well as my [Home Assistant](https://www.home-assistant.io/) setup. So when I heard that it was [shutting down](https://blog.darksky.net/dark-sky-has-a-new-home/), I thought, "I wonder if I could do this.” Plus, I love learning new things (<http://alexanderrey.ca/>), and I had been looking for a project to learn Python on, so this seemed like the perfect opportunity!

Spoiler alert, but it was much, much more difficult than I thought, but learned a lot throughout the process, and I think the end result turned out really well! 

### First Attempt- Microsoft Azure
My first attempt at setting this up was on [Microsoft Azure](https://azure.microsoft.com/en-ca/). They had a great [student credit offer](https://azure.microsoft.com/en-ca/free/students/), and running docker containers worked really well. 

However, I ran into issues with data ingest, and couldn't figure out a good way to store the files in a way that I could easily read them later. There is probably a solution to this, but I got distracted with other work and my student credit ran out. Of the three clouds that I tried, I loved the interface, and it had the least complex networking and permission setup! 

### Second Attempt- Google Cloud
My next attempt was to try [Google's Cloud](https://cloud.google.com/). Their BigQuery GIS product looked really interesting, since it handled large georeferenced datasets naturally. Google also stored the weather model data in their cloud already, simplifying data transfer.

What I found was that BigQuery works with point or feature data, and not particularly well with raster (gridded) data. However, it [can be done](https://medium.com/google-cloud/how-to-query-geographic-raster-data-in-bigquery-efficiently-b178b1a5e723) by treating each grid node as a separate point! Then, by running the [st_distance](https://cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions#st_distance) function against each point, it's very easy to find the nearest one. I also optimized this method by [partitioning](https://cloud.google.com/bigquery/docs/partitioned-tables) the globe into sections based on latitude and longitude, which made searches very fast. 

This was all working well, but where this approach broke down was on data ingest. The best way I could find to load data into BigQuery was by saving each grid node as a line on a csv file and importing that. The easiest way was to do this for each forecast time step and then import each step separately and merging them in BigQuery. However, this didn't work, since the [order of the points](https://cloud.google.com/bigquery/docs/loading-data-cloud-storage-csv) does not stay the same. I also tried this with spatial joins, but the costs quickly get prohibitive.

What ended up "working" was merging the csv files, and then uploading that file. This required an incredibly messy bash script, and meant spinning up a VM with a ton of memory and processing in order to make it reasonably fast. So despite this approach almost working, and being very cool (weather maps would have been very easy), I ended up abandoning it. 

## Current Process- AWS 
What ended up working here was discovering the AWS Elastic File System [(EFS)](https://aws.amazon.com/efs/). I wanted to avoid "reinventing the wheel" as much as possible, and there is already a great tool for extracting data from forecast files- [WGRIB2](https://www.cpc.ncep.noaa.gov/products/wesley/wgrib2/)! Moreover, NOAA data was [already being stored](https://registry.opendata.aws/collab/noaa/) on AWS. This meant that, from the 10,000 ft perspective, data could be downloaded and stored on a filesystem that could then be easily accessed by a serverless function, instead of trying to move it to a database.

That is the "one-sentence" explanation of how this is set up, but for more details, read on!

<iframe src="https://app.cloudcraft.co/view/a7efdf8d-2e5d-42aa-a4af-f2580ed530a0?key=reaYW5VNqfox1POlY7AwQw&interactive=true&embed=true" width="375" height="500">
</iframe>

### Data Sources
Starting from the beginning, two NOAA models are used for the raw forecast data: HRRR and GFS.

#### HRRR
The High Resolution Rapid Refresh [(HRRR)](https://rapidrefresh.noaa.gov/hrrr/) provides forecasts over all of the continental US, as well as most of the Canadian population. 15-minute forecasts every 3 km are provided every hour for 18 hours, and every 6 hours a 48-hour forecast is run, all at a 3 km resolution. This was perfect for this project, since Dark Sky provided a minute-by-minute forecast for 1 hour, which can be loosely approximated using the 15-minute HRRR forecasts. HRRR has almost all of the variables required for the API, with the exception of UV radiation and ozone. Personally, this is my favourite weather model, and the one that produced the best results during my thesis research on Hurricane Dorian <https://doi.org/10.1029/2020JC016489>. 

#### GFS
The Global Forecast System [(GFS)](https://www.ncdc.noaa.gov/data-access/model-data/model-datasets/global-forcast-system-gfs) is NOAA's global weather model. Running with a resolution of about 30 km (0.25 degrees), the GFS model provides hourly forecasts out of 120 hours, and 3-hour forecasts out to 240 hours. Here, GFS data is used for anywhere in the world not covered by the HRRR model, and for all results past 48 hours. 

The GFS model also underpins the Global Ensemble Forecast System [(GEFS)](https://www.ncdc.noaa.gov/data-access/model-data/model-datasets/global-ensemble-forecast-system-gefs), which is the 30-member ensemble (the website says 21, but there are 30 data files) version of the GFS. This means that 30 different "versions" of the model are run, each with slightly different starting assumptions. The API uses the GEFS to get precipitation type, quantity, and probability, since it seemed like the most accurate way of determining this. I have no idea how Dark Sky did it, and I am very open to feedback about other ways it could be assigned, since getting the precipitation probability number turned out to be one of the most complex parts of the entire setup! 

### ERA5
To provide historic weather data, the [European Reanalysis 5 Dataset](https://registry.opendata.aws/ecmwf-era5/) is used. This source is particularly interesting, since unlike the real-time NOAA models that I need to convert, it's provided in the "cloud native" [Zarr](https://zarr.readthedocs.io/en/stable/) file format. This lets the data be accessed directly and quickly in S3 from Lambda. There aren't nearly as many, many parameters available as with the GFS or HRRR models, but there are enough to cover the most important variables. 

#### Others
There are a number of other models that I could have used as part of this API. The Canadian model [(HRDPS)](https://weather.gc.ca/grib/grib2_HRDPS_HR_e.html) is even higher resolution (2.5 km), and seems to do particularly well with precipitation. Also, the [European models](https://www.ecmwf.int/en/forecasts) are sometimes considered better global models than the GFS model is, which would make it a great addition. However, HRRR and GFS were enough to get things working, and since they are stored on AWS already, there were no data transfer costs! 

As the rest of this document explains, the data pipeline here is fairly flexible, and given enough interest, it would be relatively straightforward to add additional model sources/ historic forecasts.  

Forecast data is provided by NOAA in [GRIB2 format](https://en.wikipedia.org/wiki/GRIB). This file type has a steep learning curve, but is brilliant once I realized how it worked. In short, it saves all the forecast parameters, and includes metadata on their names and units. GRIB files are compressed to save space, but are referenced in a way that lets individual parameters be quickly extracted. In order to see what is going on in a GRIB file, the NASA [Panoply](https://www.giss.nasa.gov/tools/panoply/) reader works incredibly well.

### Lambda and WGRIB2 Setup
AWS [Lambda](https://aws.amazon.com/lambda/) allows code to run without requiring any underlying server infrastructure (*serverless*). In my case, I used Python as the target language, since I was interested in learning it! Once triggered, a Lambda function will run with the configured memory. It can pull data from S3 or the Elastic File System [(EFS)](https://aws.amazon.com/efs/), and can use information passed as part of the trigger. Lambda functions can depend on layers or support code packages. In Python, almost anything that comes via an `import` line needs to be added as a layer. However, the total size of these layers can't exceed [250 MB](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html), which seems like a lot of space until it isn't. 

For this application, I wanted to use the [WGRIB2](https://www.cpc.ncep.noaa.gov/products/wesley/wgrib2/) application as much as I could, since it has been extensively optimized for this sort of work. [Pywgrib2](https://www.cpc.ncep.noaa.gov/products/wesley/wgrib2/pywgrib2.html) was recently released, which is the Python interface for working with WGRIB2 files. I used the [pywgrib2_s](https://www.cpc.ncep.noaa.gov/products/wesley/wgrib2/pywgrib2_s.html) flavour, and then always called it using the `.wgrib2` [method](https://www.cpc.ncep.noaa.gov/products/wesley/wgrib2/pywgrib2_s_wgrib2.html). The package has some interesting tools for reading gribs without having to call the C routines directly (and an xarray version), which would be faster; however, I couldn't get them to work. There are several great [guides](https://wahlnetwork.com/2020/07/28/how-to-create-aws-lambda-layers-for-python/) on how to do this, but in short:
* Create a Python virtual environment in an Amazon Linux EC2 instance
* `pip install` the package that's needed
* Zip the `site-packages` folder
* Import to AWS

There were two major issues I ran into. One was that running out of space for the layer, which I solved by going through the `site-packages` and removing anything that seemed unnecessary, the testing the function and hoping that everything worked. Particularly with pywgrib2, there were several large test/ documentation/ resources that are not required for every case, so I could get the layer to fit within the limit. The second problem was fixed by adding environmental variables for `PATH` and `LD_LIBRARY_PATH` pointing to subfolders with important libraries. I also found [this GitHub repo](https://github.com/mthenw/awesome-layers) of helpful Lambda layers and the [GeoLambda](https://github.com/developmentseed/geolambda) project. GeoLambda *almost* worked for everything, and would have been much easier, but didn't leave enough space to install WGRIB2. 

Beyond WGRIB2, I also created layers for [NetCDF4](https://unidata.github.io/netcdf4-python/), [Astral](https://pypi.org/project/astral/), [pytz](https://pypi.org/project/pytz/), and [timezonefinder](https://pypi.org/project/timezonefinder/). To get historic data, I added a [Zarr](https://zarr.readthedocs.io/en/stable/) layer; however, it is too large to be combined with the NetCDF4 layer in Lambda, which is why it's a separate API call compared to the forecast API.  
 
## Data Pipeline

### Ingest
Forecasts are saved from NOAA onto the [AWS Public Cloud](https://registry.opendata.aws/collab/noaa/) into two buckets for the [HRRR](https://registry.opendata.aws/noaa-hrrr-pds/) and [GFS](https://registry.opendata.aws/noaa-gfs-bdp-pds/) models. Each time a new file is added to these buckets, S3 sends a notification using AWS' [SNS](https://aws.amazon.com/sns/?whats-new-cards.sort-by=item.additionalFields.postDateTime&whats-new-cards.sort-order=desc), which triggers a Lambda function. 

This function first checks if the file added to NOAA's bucket (that triggered the function) meets a list of requirements- there are a lot more files added to the buckets than are needed for weather forecasting, so a regex is used to filter out unnecessary ones. If the grib file is needed, then the function extracts the forecast time and run time (ex. a file for forecast hour 6 from a model run a 18:00 UTC would be T18Z, F006). The grib file is downloaded to the Lambda `/tmp/` directory, then the `-match` [command](https://www.cpc.ncep.noaa.gov/products/wesley/wgrib2/match.html) runs to extract the required parameters (2 m temperature, wind, precipitation type, pressure, visibility, dew point, cloud cover, relative humidity, etc.). 

For the HRRR model, the wind directions need to be converted from [grid relative to earth relative](https://github.com/blaylockbk/pyBKB_v2/blob/master/demos/HRRR_earthRelative_vs_gridRelative_winds.ipynb), using the wgrib2 `-new_grid_winds` [command](https://www.cpc.ncep.noaa.gov/products/wesley/wgrib2/new_grid_winds.html). For the GFS model, there are two accumulated precipitation fields (`APCP`), one representing 3 hours of accumulation, and one representing 0 to the forecast hour. wgrib2 has a `-ncep_norm` [command](https://www.cpc.ncep.noaa.gov/products/wesley/wgrib2/ncep_norm.html); however, it requires that all the time steps are in the same grib file, which isn't how they're saved to the buckets. Instead, I used tip #66 from the (ever handy) [wgrib2 tricks](https://www.ftp.cpc.ncep.noaa.gov/wd51we/wgrib2/tricks.wgrib2) site, and added the `-quit` command to stop wgrib2 from processing the second `APCP` record. 

My complete pywgrib2_s command ended up looking like this:
1. `pywgrib2_s.wgrib2([download_path, '-new_grid_winds', 'earth', '-new_grid_interpolation', 'neighbor', '-match', matchString, '-new_grid', HRRR_grid1, HRRR_grid2, HRRR_grid3, download_path_GB])`
2. `pywgrib2_s.wgrib2([download_path, '-rewind_init', download_path, '-new_grid_winds', 'earth', '-new_grid_interpolation', 'neighbor', '-match', 'APCP', '-append','-new_grid', HRRR_grid1, HRRR_grid2, HRRR_grid3, download_path_GB, '-quit'])`

Where `matchString` was the list of parameters, `HRRR_grid1, HRRR_grid2, HRRR_grid3` are the HRRR grid parameters, and `download_path_GB` was the output file location.

Once wgrib2 has run, the function then uploads the processed grib file to my own s3 bucket. Since only the key parameters are included, the bucket size is fairly small (<15 GB), but it does generate a **lot** of `PUT` requests, particularly for the ensemble forecast (240 hours/ 3 hours per forecast step is 80 files, multiplied by 4 model runs per day, multiplied by 30 ensemble members gives 9,600 actions a day, or about 300,000 per month). 

### Merge and Process
Every time a new grib file is added to my S3 bucket, it generates a SNS event for the second set of functions, which perform additional processing, merge the time steps, and save the result as a NetCDF file. 
Because the forecasts do not necessarily arrive in chronological order, it's not possible to wait for a specific string to know that all the data has arrived. Instead, the function checks how many files have been saved, and starts running when all files are there. 

My initial plan was to simply save the grib files to EFS and access them via py_wgrib2; however, despite EFS being very quick and wgrib2's optimizations, this was never fast enough to be realistic (~20 seconds). Eventually, I was pointed in the direction of a more structured file type, and since there was already a great NetCDF Python package, it seemed perfect! 

The overall processing flow is fairly straightward:
1. Download one forecast time step to `\tmp\`
2. Run the wgrib2 `-netcdf` [command](https://www.cpc.ncep.noaa.gov/products/wesley/wgrib2/netcdf.html) to save as a NetCDF3 file
3. Create a new [in-memory](https://unidata.github.io/netcdf4-python/#in-memory-diskless-datasets) NetCDF4 file 
4. Copy variables over from NetCDF3 to NetCDF4, enabling compression and significant digit limit for each one 
5. Download subsequent forecast time steps, convert to NetCDF3 and append the data to the end of the NetCDF4 file
6. [Chunk](https://www.unidata.ucar.edu/software/netcdf/workshops/2011/nc4chunking/) the NetCDF4 file by time to dramatically speed up access times and save to EFS
7. A separate pickle file is saved with the latitudes and longitudes of each grid node

While the process is simple, the details here are tricky. This function had to run quickly because it required significant amounts of memory, which drives up the Lambda bill, and also had to avoid writing to EFS as much as possible, since that burned through my [burst credits ](https://aws.amazon.com/premiumsupport/knowledge-center/efs-burst-credits/). Hence the in-memory dataset and compression, which was crucial, since there are a lot of zeros in the grib files. This process would be much simpler if wgrib2 could export directly to NetCDF4 (since NetCDF3 doesn't have compression), but this is currently at the bleeding edge of [support](https://www.cpc.ncep.noaa.gov/products/wesley/wgrib2/).

#### Model Specific Notes
1. Since the HRRR sub-hourly model saves four time steps to each grib file, each iteration four steps get copied over instead of one. 
2. In order to get UV data, a separate grib file is needed for the GFS model, as it is classified as a "Least commonly used parameters.” The data ingest steps are the same, but there is an extra step where the wgrib2 `-append` [command ](https://www.cpc.ncep.noaa.gov/products/wesley/wgrib2/append.html) is used to merge the two NetCDF3 files together.
3. The ensemble data was by far the most difficult to deal with. There are several extra steps:
    * The 30-ensemble grib files for a given time step are merged and saved as a grib file in the `/tmp/`
 * The wgrib2 `-ens_processing` [command](https://www.cpc.ncep.noaa.gov/products/wesley/wgrib2/ens_processing.html) is then run on this merged grib file. This produces probability of precipitation, mean, and spread (which is used for precipitation intensity error) from the 30-member ensemble; however, it provides the probability of any (>0) precipitation. Since this is a little too sensitive, I used the excellent wgrib2 [trick #65](https://www.ftp.cpc.ncep.noaa.gov/wd51we/wgrib2/tricks.wgrib2), which combines `-rpn` and `-set_prob` to allow arbitrary values to be used.
 * These three values are then exported to NetCDF3 files with the `-set_ext_name` [command](https://www.cpc.ncep.noaa.gov/products/wesley/wgrib2/var.html) set to 1
 * The files are then converted to NetCDF 4 and chucked in the same way
4. For most variables, the `least significant digit` [parameter](https://unidata.github.io/netcdf4-python/#efficient-compression-of-netcdf-variables) is set to 1, and the compression level is also set to 1. There is probably some room for further optimization here. 

### Retrieval
When a request comes in, a Lambda function is triggered and is passed the URL parameters (latitude/ longitude/ extended forecast/ units) as a JSON payload. These are extracted, and then the [nearest grid cell ](https://kbkb-wx-python.blogspot.com/2016/08/find-nearest-latitude-and-longitude.html)to the lat/long is found from the pickle files created from the model results. Weather variables are then iteratively extracted from the NetCDF4 files and saved to a 2-dimensional numpy arrays. This is then repeated for each model, skipping the HRRR results the requested location is outside of the HRRR domain. For the GFS model, precipitation accumulation is adjusted from the varying time step in the grib file to a standard 1-hour time step. 

Once the data has been read in, arrays area created for the minutely and hourly forecasts, and the data series from the model results is interpolated into these new output arrays. This process worked incredibly well, since NetCDF files natively save timestamps, so the same method could be followed for each data source. 

Some precipitation parameters are true/false (will it rain, snow, hail, etc.), and for these, the same interpolation is done using 0 and 1, and then the precipitation category with the highest value is selected and saved. Currently a 10:1 snow to rain ratio is used (1 mm of rain is 10 mm of snow), but this could be improved. Where available, HRRR sub-hourly results are used for minutely precipitation (and all currently results), and the GFS ensemble model is used for the hourly time series. Daily data is calculated by processing the hourly time series, calculating maximum, minimum, and mean values. 

For the GFS and GEFS models, the returned value is an weighted average (by 1 over the distance) of the closest 9 grid cells. For variables where taking an average isn't realistic (true/false variables), the most common (mode) result is used. While this approach isn't used for the HRRR model, since the cells are much closer together, I [got it working](https://gist.github.com/alexander0042/cf4103e3fbbd7d5a6bc949970dc61e09) using the numpy `np.argpartition` function to find the 9 closest points.

A few additional parameters are calculated without using the NOAA models. The incredibly handy [timezonefinder](https://pypi.org/project/timezonefinder/) python library is used to determine the local time zone for a request, which is required to determine when days start and end and which icon to use. [Astral](https://pypi.org/project/astral/) is used for sunrise, sunset, and moon phases. Apparent temperature is found by adjusting for either [wind chill](https://en.wikipedia.org/wiki/Wind_chill) or [humidex](https://en.wikipedia.org/wiki/Humidex), and the [UV Index](https://en.wikipedia.org/wiki/Ultraviolet_index) is calculated from the modelled solar radiation. This variable has some uncertainty, since the [official documentation](https://www.cpc.ncep.noaa.gov/products/stratosphere/uv_index/uv_global.shtml) suggests that these values should be multiplied by 40. I've found this produces values that are incorrect, and instead, the model results are multiplied by 0.4. Dark Sky provides both `temperatureHigh` and `temperatureMax` values, and since I am not sure what the difference between them is, the same value is currently used for both. 

Icons are based on the categorical precipitation if it is expected, and the total cloud cover percentage and visibility otherwise. For weather alerts, a GeoJSON is downloaded every 10 minutes from the [NWS](https://api.weather.gov/alerts), and the requested point is iteratively checked to see if it is inside one of the alert polygons. If a point is inside an alert, the details are extracted from the GeoJSON and returned. 
Finally, the forecast is converted into the requested units (defaulting to US customary units for compatibility), and then into the returned JSON payload. The lambda function takes between 1 and 3 seconds to run, depending on if the point is inside the HRRR model domain, and how many alerts are currently active in the US. 

#### Historic Data
Historic data is saved in the AWS ERA5 bucket in Zarr format, which makes it incredibly easy to work with here! I mostly followed the process outlined here: <https://github.com/zflamig/birthday-weather>, with some minor tweaks to read one location instead of the entire domain and to [process accumulation variables](https://nbviewer.jupyter.org/github/awslabs/amazon-asdi/blob/main/examples/dask/notebooks/era5_zarr.ipynb). This dataset didn't include cloud cover, which presented a significant issue, since that is what's used to determine the weather icons. To work around this, I used the provided shortwave radiation flux variable and compared it against the [theoretical clear sky radiation](https://www.mdpi.com/2072-4292/5/10/4735/htm). This isn't a perfect proxy, since it doesn't work at night, and there are other factors that can impact shortwave radiation other than cloud cover (notably elevation), but it provides a reasonable approximation.

## AWS API
The end of this service relies on two other AWS products, the [API Gateway](https://aws.amazon.com/api-gateway/) and [developer portal](https://aws.amazon.com/blogs/compute/generate-your-own-api-gateway-developer-portal/). I found the API Gateway (using the REST protocol) fairly straightforward- in this implantation there is one resource, a `GET` request to the custom domain name, which extracts the `{api-key}` and `{location}` from the URL as path parameters. It also checks for URL query parameters. This method then authenticates the request, passes it to the Lambda function, and returns the result. 

The trickiest part of this setup was, by far, getting the API Gateway to use an API key from the URL. This is not officially supported (as opposed to URL query parameters). This makes sense, since passing API keys in a URL isn't a [great idea](https://security.stackexchange.com/questions/118975/is-it-safe-to-include-an-api-key-in-a-requests-url, but for compatibility, I needed to find a way. 

After a few attempts, what ended up working was a custom Lambda Authorizer as described [here](https://stackoverflow.com/questions/39154723/api-gateway-possible-to-pass-api-key-in-url-instead-of-in-the-header). Essentially, what happens is that the API Gateway passes the request to this short Lambda function, which converts the URL path parameter into the API key. This is then passed back to the API Gateway for validation. For this to work, the `API Key Source` needs to be set to `AUTHORIZER` under the setting panel. 

The developer portal is as close to a one-click deployment as possible! All that was required to click "Deploy" from the [serverless repository page](https://serverlessrepo.aws.amazon.com/applications/arn:aws:serverlessrepo:us-east-1:563878140293:applications~api-gateway-dev-portal), and a series of resources are created to handle the webpage, sign in, usage, and monitoring! The only issues I ran into were making sure that my S3 bucket names were not too long and using the CloudFront [Invalidate](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Invalidation.html) tool to check how new content looks!

## Website Access
To provide an easy front end to this API, I set up a vue.js website <https://weather.pirateweather.net> based on [weather-vue](https://github.com/krestaino/weather-vue). This project was the ideal framework, since it already relied on the Dark Sky API for forecast data, and was well documented and easy to work with. I [modified the source](https://github.com/alexander0042/weather-vue) to use Pirate Weather, as well as adding minutely and hourly forecast data! 

The static webpage is built using vue and chart.js, integrated together following [this comment](https://stackoverflow.com/questions/55684836/how-to-update-a-chart-using-vuejs-and-chartjs) (check out the ForecastMinute.vue file in the repository for my implementation). The page relies on a [back-end server](https://github.com/alexander0042/weather-api), which didn't require any modifications beyond using a Dockerfile to run on Heroku. I added the line:`RUN sed -i 's/api.darksky.net/api.pirateweather.net/g' <file path>` to the Dockerfile, where `<file path>` is the path to the node.js Dark Sky module (ex. `/app/node_modules/dark-sky/dark-sky-api.js`. 

## Next Steps
While this service currently covers almost everything that the Dark Sky API does, I have a few ideas for future improvements to this service! 
1. Text Summaries. First and foremost, this is the largest missing piece. Dark Sky [open-sourced](https://github.com/darkskyapp/translations) their translation library, so my plan is to build off that to get this working. All the data is there, but it's a matter of writing the logics required to go from numerical forecasts to weather summaries. 
2. Documentation. While the archived Dark Sky API [documentation](https://web.archive.org/web/20200723173936/https://darksky.net/dev/docs) is great for now, the AWS API Gateway has a number of tools for adding my own documentation, which would make everything clearer and more accessible.
3. Additional sources. The method developed here is largely source agnostic. Any weather forecast service that delivers data using grib files that wgrib2 can understand (all the primary ones) is theoretically capable of being added in. The NOAA North American Mesoscale [NAM](https://www.ncdc.noaa.gov/data-access/model-data/model-datasets/north-american-mesoscale-forecast-system-nam) model would provide higher resolution forecasts out to 4 days (instead of the 2 days from HRRR). The [Canadian HRDPS Model](https://weather.gc.ca/grib/grib2_HRDPS_HR_e.html) is another tempting addition, since it provides data at a resolution even higher than HRRR (2.5 km vs. 3.5 km)! The [European model](https://www.ecmwf.int/en/forecasts/datasets/catalogue-ecmwf-real-time-products) would be fantastic to add in, since it often outperforms the GFS model; however, the data is not open, which would add a significant cost.

## Changelog
* October 4, 2021
  * Still working on bringing the NBM datasource online, but in the meantime I fixed a couple issues with [cloud cover](https://github.com/alexander0042/pirate-weather-ha/issues/18) and [pressure](https://github.com/alexander0042/pirate-weather-ha/issues/14) data responses.
  * The back end of this service is also getting more stable and predictable, so I've raised the free tier to 20,000 API calls/ month.
* August 17, 2021
  * Fixed how the API returns calls for locations at the edge of the grid, identified [here](https://github.com/alexander0042/pirate-weather-ha/issues/9)
* July 26, 2021:
  * Fixed an issue with the uk2 units. 
* June 22, 2021:
  * Major rework of the alerts setup. The old method had more detail about the alerts, but missed any that didn't include coordinate data (which was about half!). These missing alerts were just associated with a NWS region. Luckily, the amazing [Iowa State Mesonet](https://mesonet.agron.iastate.edu/request/gis/watchwarn.phtml) has a geojson source for current alerts, and every alert has a polygon attached! The alerts data (still US only) is now pulled from here.
* June 9, 2021:
  * Added several new variables to the front end website
  * Changed the UV processing factor from 0.25 to 0.4
  * Corrected a sunrise/ sunset timing issue
* May 25, 2021:
  * Corrected an icon issue, identified [here](https://github.com/alexander0042/pirate-weather-hacs/issues/2)
* May 20, 2021:
  * Changed the GFS retrieval to interpolate between a weighted average (by 1/distance) of the 9 closest grid cells, instead of just taking the nearest cell. This will help to smooth out some of the sudden jumps in the results. 
  
