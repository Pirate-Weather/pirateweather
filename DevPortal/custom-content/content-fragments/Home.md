---
title: Pirate Weather
header: A Free, Open, and Documented Forecast API 
tagline: An unprocessed weather forecast API, built to be fully Dark Sky compatible.
gettingStartedButton: Get Started
apiListButton: Our APIs
---
# Quick Links
* [Get a weather forecast in the Dark Sky style](https://merrysky.net/)
* [Technical blog](https://docs.pirateweather.net)
* [Home Assistant Integration](https://github.com/alexander0042/pirate-weather-hacs)
* [Processing code repo](https://github.com/alexander0042/pirateweather)
* [Change log](https://docs.pirateweather.net/en/latest/changelog/)

#### Publications and Press
* [AWS blog post](https://aws.amazon.com/blogs/publicsector/making-weather-forecasts-accessible-serverless-infrastructure-open-data-aws/)
* [TLDR Newsletter](https://tldr.tech/tech/2023-01-11)
* [BoingBoing](https://boingboing.net/2023/01/10/pirate-weather-api-has-more-features.html)
* [Hacker News Front Page](https://news.ycombinator.com/item?id=34329988)

# Pirate Weather API
        
Weather forecasts are primarily determined using models run by government agencies, but the outputs aren't easy to use or in [formats](https://weather.gc.ca/grib/what_is_GRIB_e.html) built for applications.
To try to address this, I've put together a service (built on AWS Lambda) that reads public weather forecasts and serves it following the Dark Sky API style. It is **not** a reverse engineering of the API, since their implementation relies on radar forecasts for minutely results, as well as a few additional features. The API aims to return data using the same json structure as what Dark Sky uses, available here: [https://web.archive.org/web/20200723173936/https://darksky.net/dev/docs](https://web.archive.org/web/20200723173936/https://darksky.net/dev/docs). Feel free to register, subscribe to this API (navigate to [APIs](/apis) and **click subscribe**!), and let me know how it works at <api@alexanderrey.ca>.
To help support this project (my student AWS credits run out in June!), I've set up a [donation link](https://www.buymeacoffee.com/pirateweather). There's also an option for a monthly donations, which both supports this project and raises monthly API limit!  
 
<a href="https://www.buymeacoffee.com/pirateweather" target="_blank"><img src="https://pirateweather.net/custom-content/default-yellow.webp" width="200" height="59.533" alt="Buy Me A Coffee" ></a>

Alternatively, I also have a GitHub Sponsorship page setup on my [profile](https://github.com/sponsors/alexander0042/)!

## Why?
This API is designed to be a drop in replacement/ alternative to the Dark Sky API, and as a tool for assessing GFS and HRRR forecasts via a JSON API. This solves two goals:

1. It will also allow **legacy** applications to continue running after the Dark Sky shutdown, since as Home Assistant Integrations, Magic Mirror cards, and a whole host of other applications that have been developed over the years.
2. For anyone that is interested in knowing **exactly** how your weather forecasts are generated, this is the "show me the numbers" approach, since the data returned is directly from NOAA models, and every processing step I do is [documented](https://blog.pirateweather.net/). There are [lots](https://openweathermap.org/) [of](https://www.theweathernetwork.com) [existing](https://weather.com) [services](https://www.accuweather.com/) that provide custom forecasts using their own unique technologies, which can definitely improve accuracy, but I'm an engineer, so I wanted to be able to know what's going into the forecasts I'm using. If you're the sort of person who wants a [dense 34-page PowerPoint](http://rapidrefresh.noaa.gov/pdf/Alexander_AMS_NWP_2020.pdf) about why it rained when the forecast said it wouldn't, then this might be for you.
3. I wanted to provide a more **community focused** source of weather data. Weather is local, but I'm only in one spot, so I rely on people filing [issues](https://github.com/alexander0042/pirateweather/issues) to help improve the forecast!

Moreover, as part of my PhD program in Coastal Engineering, I spent a lot of time working with these types of files to build a real-time forecast model <https://coastlines.engineering.queensu.ca/dunexrt/>. When Dark Sky announced they were shutting down their API, I thought this would be a great opportunity to learn Python and cloud infrastructure. While Python was easier than anticipated, the cloud portion was not. After trying Azure, Google Cloud (which almost worked with BigQuery, and would have been very fast), I realized that I could mount files to functions using Amazon's Elastic File System. This solved a ton of problems, so everything is hosted in AWS, and is mostly within the free tier!

## Current Status
This API in currently in its version 1.0 release. Forecast data, including current conditions, minutely data for one hour, hourly data for up to 168 hours, and daily data for 7 days should be accurate for anywhere in the world. Weather alerts are working in the US. The service is stable and reliable, tolerating things like missing data or incorrectly formatted inputs. I'm hoping to get some feedback about how this API is performing in different locations, as well as compatibility concerns.  Feel free to sign up for the API, give it a try, and let me know how it goes!

I would love to get some comments on this service- if it's useful, how it's working, how it's not, and any other ideas, bugs, feedback! Please pass them along to <api@alexanderrey.ca>. 

### Implemented
1. API Key signups and monitoring
    * Key usage is capped at 20,000 calls a month (every 15 minutes)
    * This is subject to change depending on what my AWS bill looks like.
2. Weather forecast ingest and processing
3. Current, minutely, hourly, and daily forecasts
    * All the Dark Sky fields, including UV radiation, cloud cover, sunrise/sunset, moon phase, and temperature
    * Precipitation types and probabilities
    * Icons (`clear-day`, `clear-night`, `rain`, `snow`, `sleet`, `wind`, `fog`, `cloudy`, `partly-cloudy-day`, or `partly-cloudy-night`).
4. Drop-in compatibility with the Dark Sky API structure 
    * Uses the same `https://api.pirateweather.net/forecast/<API-Key>/<latitude>,<longitude>` setup.
    * Longitude's west (greater than 180 degrees) should be given in negative degrees.
    * Forty-eight hour default forecast, up to 168 hours using the `?extend=hourly` URL parameter.
    * Returns data using the same field names.
5. Time zones 
6. Weather Alerts in the US
7. Time Machine
 
### In Progress
1. Text summaries 
    * I would like to the official (and open-source) [Dark Sky package](https://github.com/darkskyapp/translations), but it's written in Node.js, not Python.
    * For now, the text summary just returns the icon text.
2. More detailed weather alerts and global coverage.
3. Nearest storm data. I would love to add this, but have no idea how to calculate what a storm.
4. Maps!

## Technical details
I've made a more comprehensive document with implementation details at <https://blog.pirateweather.net>. The big picture outline of this project is relatively straightforward. As new forecasts are posted to S3 buckets, an AWS Lambda function (in Python) downloads the grib files and extracts the relevant fields using [pywgrib2](https://www.cpc.ncep.noaa.gov/products/wesley/wgrib2/pywgrib2.html). The crucial step to this project is that this NetCDF file is then "chunked" to allow for quick access to one point via the [NetCDF4-Python library](https://unidata.github.io/netcdf4-python/). This dramatically speeds up the access times, making quick retrieval of data when the API is called possible. The AWS API gateway handles the front of the API calls, and the [AWS API Developer Portal](https://github.com/awslabs/aws-api-gateway-developer-portal) covers API signups. 

For ensemble data, there is an extra step of running the wgrib2 [ens_processing](https://www.cpc.ncep.noaa.gov/products/wesley/wgrib2/ens_processing.html) function. This feature calculated the probability of precipitation, as well as model spreads. The features and optimizations of wgrib2 underpin a lot of this project, and although it's not the easiest tool to learn, it is incredibly powerful. 

Historic requests (aka Time Machine) are provided using the [AWS ERA5 Dataset](https://registry.opendata.aws/ecmwf-era5/). This dataset is stored in the [Zarr](https://zarr.readthedocs.io/en/stable/), which makes it possible for me to grab a specific time step without having to store the entire dataset myself. 

### Architecture overview
<img src="https://github.com/alexander0042/pirateweather/Arch_Diagram_2023.png" width="325">

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


## Weather Data Sources
All weather data comes from the AWS open data program <https://registry.opendata.aws/collab/noaa/>. This is a fantastic program, since it is more reliable than the NOAA distribution, and means there are no data transfer changes!

High Resolution Rapid Refresh [(HRRR)](https://rapidrefresh.noaa.gov/hrrr/): 15-minute forecasts out to 48 hours for the continental US, southern Canada, and northern Mexico. This is an amazing model- it gives results in 3 km increments, and I've found it to be very accurate in a wide range of situations. 

Global Forecast System[(GFS)](https://www.ncdc.noaa.gov/data-access/model-data/model-datasets/global-forcast-system-gfs): forecasts beyond 48 hours, and for the rest of the world. GFS is lower resolution (~18 km), but provides a wide range of variables (including UV), as well as global coverage. The ensemble version [GEFS](https://www.ncdc.noaa.gov/data-access/model-data/model-datasets/global-ensemble-forecast-system-gefs) provides precipitation probabilities. 

The [ERA5 Dataset](https://registry.opendata.aws/ecmwf-era5/) is used for historic requests. It doesn't have the same range of fields that forecasts do, which limits the accuracy somewhat, but it an amazing resource. 
I would love to add more data sources some day, and while it would not be too technically complex, it would add to the processing costs. If there's another model out there that publishes in the grib format, let me know (<api@alexanderrey.ca>), especially if it has sub-hourly outputs. 

## Other Notes and Assumptions
1. While this API will give minutely forecasts for anywhere in the world, they are calculated using the HRRR-subhourly forecasts, so only accurate to 15-minute periods. Outside of the HRRR domain, they are calculated using the GFS hourly forecasts, so really not adding much value! 
2. Precipitation probabilities are a tricky problem to solve- weather models don't give a range of outcomes, just one answer. To get probabilities, this implementation relies on the Global Ensemble Forecast System [(GEFS)](https://www.ncdc.noaa.gov/data-access/model-data/model-datasets/global-ensemble-forecast-system-gefs). This is a 30-member ensemble, so if 1 member predicts precipitation, the probability will be 1/30. GEFS data is also used to predict precipitation type and accumulation. A 1:10 snow-water ratio is assumed. 
3. Current conditions are based on model results (from HRRR-subhourly), which assimilates observations, but not direct observations. 
4. Why "Pirate Weather"? I've always thought that the HRRR model was pronounced the same way as the classic pirate "ARRR". Plus, compared to the range of commercial APIs with mystery processing steps, this service focuses on providing direct model data, which is just a little bit disruptive. I still think there's room for improvement with the name, so send suggestions my way!