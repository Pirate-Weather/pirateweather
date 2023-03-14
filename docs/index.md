<div class="imageContainer">
  <div class="text-block">
    <h1 style="color: white;">Pirate Weather</h1>
  </div>
</div>

[Get an API key](https://pirate-weather.apiable.io/){ .md-button .md-button--primary }

## Quick Links
* To [**register for the API**](https://pirate-weather.apiable.io/)
* [Access the old portal for sign-ups before March 2023](https://portal.pirateweather.net)
* [Get a weather forecast in the Dark Sky style](https://merrysky.net/)
* [Home Assistant Integration](https://github.com/alexander0042/pirate-weather-hacs)
* [Processing code repo](https://github.com/alexander0042/pirateweather)
* [Changelog](https://pirateweather.net/en/latest/changelog/)
* [Status page](https://stats.uptimerobot.com/DRKqBCok2N)

#### Publications and Press
* [AWS blog post](https://aws.amazon.com/blogs/publicsector/making-weather-forecasts-accessible-serverless-infrastructure-open-data-aws/)
* [TLDR Newsletter](https://tldr.tech/tech/2023-01-11)
* [BoingBoing](https://boingboing.net/2023/01/10/pirate-weather-api-has-more-features.html)
* [Hacker News Front Page](https://news.ycombinator.com/item?id=34329988)

# Introduction 
Weather forecasts are primarily found using models run by government agencies, but the [outputs](https://weather.gc.ca/grib/what_is_GRIB_e.html) aren't easy to use or in formats built for the web.
To try to address this, I've put together a service that reads weather forecasts and serves it following the [Dark Sky API](https://web.archive.org/web/20200723173936/https://darksky.net/dev/docs) style. 

Before going any farther, I wanted to add a [link to sign up and support this project](https://pirate-weather.apiable.io/products/weather-data)! Running this on AWS means that it scales beautifully and is much more reliable than if I was trying to host this, but also costs real money. I'd love to keep this project going long-term, but I'm still paying back my student loans, which limits how much I can spend on this! Anything helps, and a $2 monthly donation lets me raise your API limit from 10,000 calls/ month to 25,000 calls per month.

Alternatively, I also have a GitHub Sponsorship page set up on my [profile](https://github.com/sponsors/alexander0042/)! This gives the option to make a one-time donation to contribute this project. This project (especially the free tier) wouldn't be possible without the ongoing support from the project sponsors, so they're the [heros here](https://github.com/sponsors/alexander0042/)! 

<iframe src="https://github.com/sponsors/alexander0042/card" title="Sponsor alexander0042" height="225" width="600" style="border: 0;"></iframe>

## Recent Updates- Spring 2023
Up to version 1.4! As always, details are available in the [changelog](https://pirateweather.net/en/latest/changelog/).

1. New sign-up portal: <https://pirate-weather.apiable.io/>. This will let me spend way less time managing subscriptions, and more time data wrangling. Also addresses a ton of bugs related to the old developer portal. APIs requested via the old portal will continue to work though! 
2. Much better alert support.
3. A ton of assorted bug fixes.
4. Published official [API specifications](http://docs.pirateweather.net/en/latest/Specification/).
5. Major revamp of the Home Assistant Integration.

## Background
This project started from two points: as part of my [PhD](https://coastlines.engineering.queensu.ca/dunexrt), I had to become very familiar with working with NOAA forecast results (<https://orcid.org/0000-0003-4725-3251>). Separately, an old tablet set up as a "Magic Mirror,” and was using a [weather module](https://github.com/jclarke0000/MMM-DarkSkyForecast) that relied on the Dark Sky API, as well as my [Home Assistant](https://www.home-assistant.io/) setup. So when I heard that it was [shutting down](https://blog.darksky.net/dark-sky-has-a-new-home/), I thought, "I wonder if I could do this.” Plus, I love learning new things (<http://alexanderrey.ca/>), and I had been looking for a project to learn Python on, so this seemed like the perfect opportunity!
Spoiler alert, but it was way more difficult than I thought, but learned a lot throughout the process, and I think the end result turned out really well! 

## Why?
This API is designed to be a drop in replacement/ alternative to the Dark Sky API, and as a tool for assessing GFS and HRRR forecasts via a JSON API. This solves two goals:

1. It will also allow **legacy** applications to continue running after the Dark Sky shutdown, since as Home Assistant Integrations, Magic Mirror cards, and a whole host of other applications that have been developed over the years.
2. For anyone that is interested in knowing **exactly** how your weather forecasts are generated, this is the "show me the numbers" approach, since the data returned is directly from NOAA models, and every processing step I do is [documented](https://blog.pirateweather.net/). There are [lots](https://openweathermap.org/) [of](https://www.theweathernetwork.com) [existing](https://weather.com) [services](https://www.accuweather.com/) that provide custom forecasts using their own unique technologies, which can definitely improve accuracy, but I'm an engineer, so I wanted to be able to know what's going into the forecasts I'm using. If you're the sort of person who wants a [dense 34-page PowerPoint](http://rapidrefresh.noaa.gov/pdf/Alexander_AMS_NWP_2020.pdf) about why it rained when the forecast said it wouldn't, then this might be for you.
3. I wanted to provide a more **community focused** source of weather data. Weather is local, but I'm only in one spot, so I rely on people filing [issues](https://github.com/alexander0042/pirateweather/issues) to help improve the forecast!
## Current Process- AWS 
The key to everything here is AWS's Elastic File System [(EFS)](https://aws.amazon.com/efs/). I wanted to avoid "reinventing the wheel" as much as possible, and there is already a great tool for extracting data from forecast files- [WGRIB2](https://www.cpc.ncep.noaa.gov/products/wesley/wgrib2/)! Moreover, NOAA data was [already being stored](https://registry.opendata.aws/collab/noaa/) on AWS. This meant that, from the 10,000 ft perspective, data could be downloaded and stored on a file system that could then be easily accessed by a serverless function, instead of trying to move it to a database.
That is the "one-sentence" explanation of how this is set up, but for more details, read on!

### Architecture overview
<img src="https://github.com/alexander0042/pirateweather/raw/main/docs/images/Arch_Diagram_2023.png" width="325">

1. EventBridge timers launch Step Function to trigger Fargate
2. WGRIB2 Image pulled from repo
3. Fargate Cluster launched
4. Task to: Download, Merge, Chunk GRB files
5. Data saved to EFS
6. NWS alerts saved to EFS as GeoJSON
7. Lambda reads forecast data, processes and interpolates, returns JSON
8. Expose JSON forecast data via API Gateway
9. Distribute API endpoint via CloudFront
10. Monitor API key usage


### Data Sources
Starting from the beginning, three NOAA models are used for the raw forecast data: HRRR, GFS, and the GEFS.

#### HRRR
The High Resolution Rapid Refresh [(HRRR)](https://rapidrefresh.noaa.gov/hrrr/) provides forecasts over all of the continental US, as well as most of the Canadian population. 15-minute forecasts every 3 km are provided every hour for 18 hours, and every 6 hours a 48-hour forecast is run, all at a 3 km resolution. This was perfect for this project, since Dark Sky provided a minute-by-minute forecast for 1 hour, which can be loosely approximated using the 15-minute HRRR forecasts. HRRR has almost all of the variables required for the API, with the exception of UV radiation and ozone. Personally, this is my favourite weather model, and the one that produced the best results during my thesis research on Hurricane Dorian <https://doi.org/10.1029/2020JC016489>. 

#### GFS
The Global Forecast System [(GFS)](https://www.ncdc.noaa.gov/data-access/model-data/model-datasets/global-forcast-system-gfs) is NOAA's global weather model. Running with a resolution of about 30 km (0.25 degrees), the GFS model provides hourly forecasts out of 120 hours, and 3-hour forecasts out to 240 hours. Here, GFS data is used for anywhere in the world not covered by the HRRR model, and for all results past 48 hours. 

The GFS model also underpins the Global Ensemble Forecast System [(GEFS)](https://www.ncdc.noaa.gov/data-access/model-data/model-datasets/global-ensemble-forecast-system-gefs), which is the 30-member ensemble (the website says 21, but there are 30 data files) version of the GFS. This means that 30 different "versions" of the model are run, each with slightly different starting assumptions. The API uses the GEFS to get precipitation type, quantity, and probability, since it seemed like the most accurate way of determining this. I have no idea how Dark Sky did it, and I am very open to feedback about other ways it could be assigned, since getting the precipitation probability number turned out to be one of the most complex parts of the entire setup! 

#### GEFS
The Global Ensemble Forecast System [(GEFS)](https://www.ncei.noaa.gov/products/weather-climate-models/global-ensemble-forecast) is the ensemble version of NOAA's GFS model. By running different variations parameters and inputs, 30 different versions of this model are run at the same time, providing 3-hour forecasts out to 240 hours. The API uses the GEFS to get precipitation type, quantity, and probability, since it seemed like the most accurate way of determining this. I have no idea how Dark Sky did it, and I am very open to feedback about other ways it could be assigned, since getting the precipitation probability number turned out to be one of the most complex parts of the entire setup! 

### ERA5
To provide historic weather data, the [European Reanalysis 5 Dataset](https://registry.opendata.aws/ecmwf-era5/) is used. This source is particularly interesting, since unlike the real-time NOAA models that I need to convert, it's provided in the "cloud native" [Zarr](https://zarr.readthedocs.io/en/stable/) file format. This lets the data be accessed directly and quickly in S3 from Lambda. There aren't nearly as many, many parameters available as with the GFS or HRRR models, but there are enough to cover the most important variables. 

#### Others
There are a number of other models that I could have used as part of this API. The Canadian model [(HRDPS)](https://weather.gc.ca/grib/grib2_HRDPS_HR_e.html) is even higher resolution (2.5 km), and seems to do particularly well with precipitation. Also, the [European models](https://www.ecmwf.int/en/forecasts) are sometimes considered better global models than the GFS model is, which would make it a great addition. However, HRRR and GFS were enough to get things working, and since they are stored on AWS already, there were no data transfer costs! 

As the rest of this document explains, the data pipeline here is fairly flexible, and given enough interest, it would be relatively straightforward to add additional model sources/ historic forecasts.  

Forecast data is provided by NOAA in [GRIB2 format](https://en.wikipedia.org/wiki/GRIB). This file type has a steep learning curve, but is brilliant once I realized how it worked. In short, it saves all the forecast parameters, and includes metadata on their names and units. GRIB files are compressed to save space, but are referenced in a way that lets individual parameters be quickly extracted. In order to see what is going on in a GRIB file, the NASA [Panoply](https://www.giss.nasa.gov/tools/panoply/) reader works incredibly well.

### Lambda, Fargate, and WGRIB2 Setup
AWS [Lambda](https://aws.amazon.com/lambda/) allows code to run without requiring any underlying server infrastructure (*serverless*). In my case, I used Python as the target language, since I was interested in learning it! Once triggered, a Lambda function will run with the configured memory. It can pull data from S3 or the Elastic File System [(EFS)](https://aws.amazon.com/efs/), and can use information passed as part of the trigger. Lambda functions can depend on layers or support code packages. This API uses Lambda to retrieve and process the forecast data when a call is made. 
Lambda handles Python packages as layers, so I created layers for [NetCDF4](https://unidata.github.io/netcdf4-python/), [Astral](https://pypi.org/project/astral/), [pytz](https://pypi.org/project/pytz/), and [timezonefinder](https://pypi.org/project/timezonefinder/). To get historic data, I added a [Zarr](https://zarr.readthedocs.io/en/stable/) layer; however, it is too large to be combined with the NetCDF4 layer in Lambda, which is why it's a separate API call compared to the forecast API.  
For processing, I wanted to use the [WGRIB2](https://www.cpc.ncep.noaa.gov/products/wesley/wgrib2/) application as much as I could, since it has been extensively optimized for this sort of work. [Pywgrib2](https://www.cpc.ncep.noaa.gov/products/wesley/wgrib2/pywgrib2.html) was recently released, which is the Python interface for working with WGRIB2 files. I used the [pywgrib2_s](https://www.cpc.ncep.noaa.gov/products/wesley/wgrib2/pywgrib2_s.html) flavour, and then always called it using the `.wgrib2` [method](https://www.cpc.ncep.noaa.gov/products/wesley/wgrib2/pywgrib2_s_wgrib2.html).
I initially had this setup using Lambda, but ran into the 500 MB temporary storage limit that Lambda has. Instead, processing is now done using the Elastic Conatiner Service (ECS) and Fargate. This lets code run inside a Docker container, which I set up to compile the WGRIB2 code from source. This image is stored on [AWS](https://gallery.ecr.aws/j9v4j3c7/pirate-wgrib2), and gets retrieved each time a processing task is run! The [Dockerfile](https://github.com/alexander0042/pirateweather/tree/main/wgrib2) to generate this container is pretty simple, relying on Ubuntu as a base image and following the instructions from the [WGRIB2 README](https://www.ftp.cpc.ncep.noaa.gov/wd51we/wgrib2/_README). Only interesting part is a nifty "one-liner" to replace a specific line in the makefile: `RUN sed -i "s|MAKE_SHARED_LIB=0|MAKE_SHARED_LIB=1|g" makefile'.
 
## Data Pipeline

### Trigger
Forecasts are saved from NOAA onto the [AWS Public Cloud](https://registry.opendata.aws/collab/noaa/) into three buckets for the [HRRR](https://registry.opendata.aws/noaa-hrrr-pds/), [GFS](https://registry.opendata.aws/noaa-gfs-bdp-pds/), and [GEFS](https://registry.opendata.aws/noaa-gefs/ models. Since I couldn't find a good way to trigger processing tasks based on S3 events in a public buckled, the ingest system relies on timed events scheduled through [AWS EventBridge Rules](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-create-rule-schedule.html), with the timings shown in the table below:

|                    | GFS        | GEFS      | HRRR- 48h             | HRRR- 18h/ SubHourly |
|--------------------|------------|-----------|-----------------------|----------------------|
| Run Times (UTC)    | 0,6,12,18  | 0,6,12,18 | 0,6,12,18             | 0-24                 |
| Delay              | 5:00       | 7:00      | 2:30                  | 1:45                 |
| Ingest Times (UTC) | 5,11,17,23 | 7,13,19,1 | 2:30,8:30,14:30,20:30 | 1:45-00:45           |

Each rule calls a different [AWS Step Function](https://aws.amazon.com/step-functions/?step-functions.sort-by=item.additionalFields.postDateTime&step-functions.sort-order=desc), which is the tool that oversees the data pipeline. The step function takes the current time from the trigger, adds several other environmental parameters (like which bucket the data is saved in and which processing script to use), and then finally starts a Fargate Task using the WGRIB2/ Python Docker image! Step functions have the added perk that they can repeat the task if it fails for some reason. I spent some time optimizing the tasks to [maximize network speed](https://www.stormforge.io/blog/aws-fargate-network-performance/) and minimize the RAM requirements, settling on 1 CPU and 5 GB of RAM. The Fargate task is set up to have access to the NOAA S3 buckets, as well as an EFS file system to save the processed files. The python processing scripts are explained below, with the source code available on the [repository](https://github.com/alexander0042/pirateweather/tree/main/scripts).

### Download, Filter, and Merge
For all of the models, the download process works in a similar way:

1. Get the bucket, time, and download path from the environmental variables set by the step function.
2. Set up paths on the EFS filesystem.
3. Step through the required files and download using `boto3`.

For the HRRR model, the wind directions need to be converted from [grid relative to earth relative](https://github.com/blaylockbk/pyBKB_v2/blob/master/demos/HRRR_earthRelative_vs_gridRelative_winds.ipynb), using the wgrib2 `-new_grid_winds` [command](https://www.cpc.ncep.noaa.gov/products/wesley/wgrib2/new_grid_winds.html). Separately, for the GFS/ GEFS models, there are two accumulated precipitation fields (`APCP`), one representing 3 hours of accumulation, and one representing 0 to the forecast hour. wgrib2 has a `-ncep_norm` [command](https://www.cpc.ncep.noaa.gov/products/wesley/wgrib2/ncep_norm.html); however, it requires that all the time steps are in the same grib file, which isn't how they're saved to the buckets. Instead, I used tip #66 from the (ever handy) [wgrib2 tricks](https://www.ftp.cpc.ncep.noaa.gov/wd51we/wgrib2/tricks.wgrib2) site, and added the `-quit` command to stop wgrib2 from processing the second `APCP` record.

My complete pywgrib2_s command ended up looking like this:

1. `pywgrib2_s.wgrib2([download_path, '-new_grid_winds', 'earth', '-new_grid_interpolation', 'neighbor', '-match', matchString, '-new_grid', HRRR_grid1, HRRR_grid2, HRRR_grid3, download_path_GB])`
2. `pywgrib2_s.wgrib2([download_path, '-rewind_init', download_path, '-new_grid_winds', 'earth', '-new_grid_interpolation', 'neighbor', '-match', 'APCP', '-append','-new_grid', HRRR_grid1, HRRR_grid2, HRRR_grid3, download_path_GB, '-quit'])`

Where `matchString` was the list of parameters, `HRRR_grid1, HRRR_grid2, HRRR_grid3` are the HRRR grid parameters, and `download_path_GB` was the output file location.
Once wgrib2 has run, the processed grib files are appended to a NetCDF file (via `pywgrib2_s.wgrib2([download_path_GB, '-append', '-netcdf', download_path_NC])`). This is a NetCDF 3 file, so no compression, but is much easier to work with than GRIB files. After each step is added to the NetCDF, the original GRIBs are removed to save space. 
For most of the scripts, there are actually two different processes going on at the same time, downloading slightly different files. For the GFS model, this is the primary and secondary variable versions, for GEFS this is the complete ensemble as well as the mean, and for HRRR this is the hourly and subhourly forecasts. The process is the same as above, just replicated to reduce the number of scripts that need to be run. 

### Compress, Chunk, and Save
My initial plan was to simply save the grib files to EFS and access them via py_wgrib2; however, despite EFS being very quick and wgrib2's optimizations, this was never fast enough to be realistic (~20 seconds). Eventually, I was pointed in the direction of a more structured file type, and since there was already a great NetCDF Python package, it seemed perfect! 
From the merged NetCDF 3 files, the next steps are pretty straightforward:

1. Create a new [in-memory](https://unidata.github.io/netcdf4-python/#in-memory-diskless-datasets) NetCDF4 file .
2. Copy variables over from NetCDF3 to NetCDF4, enabling compression and significant digit limit for each one.
3. [Chunk](https://www.unidata.ucar.edu/software/netcdf/workshops/2011/nc4chunking/) the NetCDF4 file by time to dramatically speed up access times and save to EFS.
4. A separate pickle file is saved with the latitudes and longitudes of each grid node.
5. Old model results are removed from the EFS filesystem.

While the process is simple, the details here are tricky. The chunking and compression are the key elements here, since they allow for fast data retrieval, while using an in-memory dataset speeds things up a fair bit.

#### Model Specific Notes

1. In order to get UV data, a separate grib file is needed for the GFS model, as it is classified as a "Least commonly used parameters.” The data ingest steps are the same, but there is an extra step where the wgrib2 `-append` [command ](https://www.cpc.ncep.noaa.gov/products/wesley/wgrib2/append.html) is used to merge the two NetCDF3 files together.
2. The ensemble data was by far the most difficult to deal with. There are several extra steps:
    * The 30-ensemble grib files for a given time step are merged and saved as a grib file in the `/tmp/`
 * The wgrib2 `-ens_processing` [command](https://www.cpc.ncep.noaa.gov/products/wesley/wgrib2/ens_processing.html) is then run on this merged grib file. This produces probability of precipitation, mean, and spread (which is used for precipitation intensity error) from the 30-member ensemble; however, it provides the probability of any (>0) precipitation. Since this is a little too sensitive, I used the excellent wgrib2 [trick #65](https://www.ftp.cpc.ncep.noaa.gov/wd51we/wgrib2/tricks.wgrib2), which combines `-rpn` and `-set_prob` to allow arbitrary values to be used.
 * These three values are then exported to NetCDF3 files with the `-set_ext_name` [command](https://www.cpc.ncep.noaa.gov/products/wesley/wgrib2/var.html) set to 1
 * The files are then converted to NetCDF 4 and chucked in the same way
3. For most variables, the `least significant digit` [parameter](https://unidata.github.io/netcdf4-python/#efficient-compression-of-netcdf-variables) is set to 1, and the compression level is also set to 1. There is probably some room for further optimization here.
 
### Retrieval
When a request comes in, a Lambda function is triggered and is passed the URL parameters (latitude/ longitude/ time/ extended forecast/ units) as a JSON payload. These are extracted, and then the [nearest grid cell ](https://kbkb-wx-python.blogspot.com/2016/08/find-nearest-latitude-and-longitude.html)to the lat/long is found from the pickle files created from the model results. Using the time parameter (if available, otherwise the current time), the latest completed model runs are identified. Weather variables are then iteratively extracted from the NetCDF4 files and saved to a 2-dimensional numpy arrays. This is then repeated for each model, skipping the HRRR results the requested location is outside of the HRRR domain. For the GFS model, precipitation accumulation is adjusted from the varying time step in the grib file to a standard 1-hour time step. 

Once the data has been read in, arrays area created for the minutely and hourly forecasts, and the data series from the model results is interpolated into these new output arrays. This process worked incredibly well, since NetCDF files natively save timestamps, so the same method could be followed for each data source. 

Some precipitation parameters are true/false (will it rain, snow, hail, etc.), and for these, the same interpolation is done using 0 and 1, and then the precipitation category with the highest value is selected and saved. Currently a 10:1 snow to rain ratio is used (1 mm of rain is 10 mm of snow), but this could be improved. Where available, HRRR sub-hourly results are used for minutely precipitation (and all currently results), and the GFS ensemble model is used for the hourly time series. Daily data is calculated by processing the hourly time series, calculating maximum, minimum, and mean values. 

For the GFS and GEFS models, the returned value is a weighted average (by 1 over the distance) of the closest 9 grid cells. For variables were taking an average isn't realistic (true/false variables), the most common (mode) result is used. While this approach isn't used for the HRRR model, since the cells are much closer together, I [got it working](https://gist.github.com/alexander0042/cf4103e3fbbd7d5a6bc949970dc61e09) using the numpy `np.argpartition` function to find the 9 closest points.

A few additional parameters are calculated without using the NOAA models. The incredibly handy [timezonefinder](https://pypi.org/project/timezonefinder/) python library is used to determine the local time zone for a request, which is required to determine when days start and end and which icon to use. [Astral](https://pypi.org/project/astral/) is used for sunrise, sunset, and moon phases. Apparent temperature is found by adjusting for either [wind chill](https://en.wikipedia.org/wiki/Wind_chill) or [humidex](https://en.wikipedia.org/wiki/Humidex), and the [UV Index](https://en.wikipedia.org/wiki/Ultraviolet_index) is calculated from the modelled solar radiation. This variable has some uncertainty, since the [official documentation](https://www.cpc.ncep.noaa.gov/products/stratosphere/uv_index/uv_global.shtml) suggests that these values should be multiplied by 40. I've found this produces values that are incorrect, and instead, the model results are multiplied by 0.4. Dark Sky provides both `temperatureHigh` and `temperatureMax` values, and since I am not sure what the difference between them is, the same value is currently used for both. 

Icons are based on the categorical precipitation if it is expected, and the total cloud cover percentage and visibility otherwise. For weather alerts, a GeoJSON is downloaded every 10 minutes from the [NWS](https://api.weather.gov/alerts), and the requested point is iteratively checked to see if it is inside one of the alert polygons. If a point is inside an alert, the details are extracted from the GeoJSON and returned. 
Finally, the forecast is converted into the requested units (defaulting to US customary units for compatibility), and then into the returned JSON payload. The lambda function takes between 1 and 3 seconds to run, depending on if the point is inside the HRRR model domain, and how many alerts are currently active in the US. 

#### Historic Data
Historic data is saved in the AWS ERA5 bucket in Zarr format, which makes it incredibly easy to work with here! I mostly followed the process outlined here: <https://github.com/zflamig/birthday-weather>, with some minor tweaks to read one location instead of the entire domain and to [process accumulation variables](https://nbviewer.jupyter.org/github/awslabs/amazon-asdi/blob/main/examples/dask/notebooks/era5_zarr.ipynb). This dataset didn't include cloud cover, which presented a significant issue, since that is what's used to determine the weather icons. To work around this, I used the provided shortwave radiation flux variable and compared it against the [theoretical clear sky radiation](https://www.mdpi.com/2072-4292/5/10/4735/htm). This isn't a perfect proxy, since it doesn't work at night, and there are other factors that can impact shortwave radiation other than cloud cover (notably elevation), but it provides a reasonable approximation.

## AWS API
The end of this service relies on two other AWS products, the [API Gateway](https://aws.amazon.com/api-gateway/) and [developer portal](https://aws.amazon.com/blogs/compute/generate-your-own-api-gateway-developer-portal/). I found the API Gateway (using the REST protocol) fairly straightforward- in this implantation there is one resource, a `GET` request to the custom domain name, which extracts the `{api-key}` and `{location}` from the URL as path parameters. It also checks for URL query parameters. This method then authenticates the request, passes it to the Lambda function, and returns the result. 

The trickiest part of this setup was, by far, getting the API Gateway to use an API key from the URL. This is not officially supported (as opposed to URL query parameters). This makes sense, since passing API keys in a URL isn't a [great idea](https://security.stackexchange.com/questions/118975/is-it-safe-to-include-an-api-key-in-a-requests-url, but for compatibility, I needed to find a way. 

After a few attempts, what ended up working was a custom Lambda Authorizer as described [here](https://stackoverflow.com/questions/39154723/api-gateway-possible-to-pass-api-key-in-url-instead-of-in-the-header). Essentially, what happens is that the API Gateway passes the request to this short Lambda function, which converts the URL path parameter into the API key. This is then passed back to the API Gateway for validation. For this to work, the `API Key Source` needs to be set to `AUTHORIZER` under the setting panel. 

## Next Steps
While this service currently covers almost everything that the Dark Sky API does, I have a few ideas for future improvements to this service! 

1. Text Summaries. This is the largest missing piece. Dark Sky [open-sourced](https://github.com/darkskyapp/translations) their translation library, so my plan is to build off that to get this working. All the data is there, but it's a matter of writing the logics required to go from numerical forecasts to weather summaries. 
2. Additional sources. The method developed here is largely source agnostic. Any weather forecast service that delivers data using grib files that wgrib2 can understand (all the primary ones) is theoretically capable of being added in. The NOAA North American Mesoscale [NAM](https://www.ncdc.noaa.gov/data-access/model-data/model-datasets/north-american-mesoscale-forecast-system-nam) model would provide higher resolution forecasts out to 4 days (instead of the 2 days from HRRR). The [Canadian HRDPS Model](https://weather.gc.ca/grib/grib2_HRDPS_HR_e.html) is another tempting addition, since it provides data at a resolution even higher than HRRR (2.5 km vs. 3.5 km)! The [European model](https://www.ecmwf.int/en/forecasts/datasets/catalogue-ecmwf-real-time-products) would be fantastic to add in, since it often outperforms the GFS model; however, the data is not open, which would add a significant cost.

## Other Notes and Assumptions
1. While this API will give minutely forecasts for anywhere in the world, they are calculated using the HRRR-subhourly forecasts, so only accurate to 15-minute periods. Outside of the HRRR domain, they are calculated using the GFS hourly forecasts, so really not adding much value! 
2. Precipitation probabilities are a tricky problem to solve- weather models don't give a range of outcomes, just one answer. To get probabilities, this implementation relies on the Global Ensemble Forecast System [(GEFS)](https://www.ncdc.noaa.gov/data-access/model-data/model-datasets/global-ensemble-forecast-system-gefs). This is a 30-member ensemble, so if 1 member predicts precipitation, the probability will be 1/30. GEFS data is also used to predict precipitation type and accumulation. A 1:10 snow-water ratio is assumed. 
3. Current conditions are based on model results (from HRRR-subhourly), which assimilates observations, but not direct observations. 
4. Why "PirateWeather"? I've always thought that the HRRR model was pronounced the same way as the classic pirate "ARRR". Also, there is [one company](https://arstechnica.com/tech-policy/2020/10/google-asks-supreme-court-to-overrule-disastrous-ruling-on-api-copyrights/) out there that thinks APIs can be copyrighted, which might apply here. 

# Who is using PirateWeather?

- [MerrySky](https://merrysky.net) - Get a Forecast DarkSky Style
- [PW-forecast](https://github.com/ktrue/PW-forecast) and [https://saratoga-weather.org/scripts-PWforecast.php](https://saratoga-weather.org/scripts-PWforecast.php)

Do you use PirateWeather? Open a pull request to add it to the list.
