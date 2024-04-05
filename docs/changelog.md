# Changelog

For a RSS feed of these changes, subscribe using this link: <https://github.com/alexander0042/pirateweather/commits/main.atom>.

???+ note "Version 1.5"
	
    * December 11, 2023: API Version 1.5.6
	    * Added error handling for times in the future per issue [#122](https://github.com/Pirate-Weather/pirateweather/issues/122).
     	* Improved how short term historic forecasts (<3 days) and processed.
      	* Not live yet, but significant progress on V2.0 has occurred, and ingest scripts for NBM + HRRR Smoke are complete, as well as updates to allow for previous observations to be used in processing.
    * August 29, 2023: API Version 1.5.5
    	* Dull back-end update: added response compression to reduce a terrifyingly large AWS data transfer bill, and removed old logging statements.
    * July 13, 2023: API Version 1.5.4
    	* Fixed a series of rounding issues: [#4](https://github.com/alexander0042/pirateweather/issues/4), [#36](https://github.com/alexander0042/pirateweather/issues/36), and [#77](https://github.com/alexander0042/pirateweather/issues/77).
    * July 6, 2023: API Version 1.5.3
	    * Fixed a glitch producing a "snow" precipitation type when very small amounts of precipitation were forecasted per issue [#78](https://github.com/alexander0042/pirateweather/issues/78).
    	* Fixed an issue with the icon field returning the night icons in areas with 24 hours of sun per [issue #79](https://github.com/alexander0042/pirateweather/issues/78).
    	* Fixed an parsing problem with small negative latitudes per [issue #67](https://github.com/alexander0042/pirateweather/issues/78).
    * May 26, 2023: API Version 1.5
	    * Least interesting point update ever, but important nevertheless! Migrated existing keys from using AWS API Gateway to Kong as the back-end layer. This will allow the service to grow past the 10,000 user limit imposed by the AWS Gateway, allows me to add a caching layer to improve performance, provides more AWS availability zone redundancy, and provides some more flexible routing options in the future. As a bonus, Kong returns the number of API requests remaining as a header, addressing [issue #54](https://github.com/alexander0042/pirateweather/issues/54).
   
??? note "Version 1.4"

	* March 13, 2023: API Version 1.4.1
		* Fixed a rounding bug introduced in 1.4 which sometimes created issues with the currently block precipitation intensity parameter over the HRRR grid per [issue #29](https://github.com/alexander0042/pirateweather/issues/29).
	* February 28, 2023: API Version 1.4
		* Fixed a long standing bug in the GEFS precipitation intensity for the currently and minutely blocks per [issue #24](https://github.com/alexander0042/pirateweather/issues/24). Outside of the HRRR area, precipitation intensities are now calculated using GEFS, instead of just returning zero!
		* Corrected how midnight is calculated in the Eastern Hemisphere.
   
??? note "Version 1.3"

	* January 27, 2023: API Version 1.3.2
		* Fixed an issue created when fixing the HRRR grid point issue that resulted in the HRRR model not being used per [this issue](https://github.com/alexander0042/pirateweather/issues/22).
	* January 26, 2023: API Version 1.3.1
		* Fixed an issue with the time parameter not showing up as an integer per [this issue](https://github.com/alexander0042/pirateweather/issues/4).
		* Fixed an issue where the HRRR model would grab results for the incorrect grid cell when a point very near the edge was requested.
	* January 24, 2023: API Version 1.3
		* Rapid update here- implemented the `temperatureHigh` and `TemperatureLow` parameters to match Dark Sky, by using the daily high and nighttime low data. 
		* Added the missing `windGuestTime`.
		* Corrected a bug on all the max/min times for days 2-7.
		* Changed all daily parameters except icon/ summary to be calculated over a 24 hour period from 12:00 am to 12:00 am, instead of 4:00 to 4:00.
		* Fixed a bug with sunrise and sunset times in UTC+x time zones.
   
??? note "Version 1.2"

	* January 23, 2023: API Version 1.2
		* Alerts! Finally wrote a processing script to save weather alerts as a NetCDF file, which provides much more detail as well as much faster response times.
   
??? note "Version 1.1"

	* December 1, 2022: API Version 1.1.10
    	* Quick fix to address a server error when requesting a point on the edge of the HRRR grid.
	* November 25, 2022: API Version 1.1.9
    	* Add in a daily average precipitation intensity for compatibility with Dark Sky. Note that this value will always be in either mm or inches, so may not align with accumulation during days with mixed rain and snow.
	* October 28, 2022: API Version 1.1.8
    	* Change the interpolation weighting function for GFS/ GEFS model data from inverse distance (1/distance) to inverse distance squared (1/distance^2). This increases the weight of the nearest grid cell, particularly when a forecast point is near the centre of a cell. The goal for this change is to make results more accurate in coastal areas where there can be large differences between land and water cells while keeping the smooth transition from one grid point to the next.
	* September 7, 2022: API Version 1.1.7
    	* Update the logic when model data is missing per [this issue](https://github.com/alexander0042/pirate-weather-ha/issues/30#issuecomment-1227640161).
	* March 30, 2022: API version 1.1.6
    	* Updated the fog icon to allow it to display at night.
		* Aligned the cloud cover icon with [NOAA definitions](https://weather.com/science/weather-explainers/news/common-weather-terms-used-incorrectly).
		* Capped the visibility at 10 miles to avoid HRRR/ GFS inconsistency.
		* Corrected a bug causing "-0" to be returned when very small accumulations were forecasted.
		* Corrected the wind icon threshold.
		* Resolves [Issue #3](https://github.com/alexander0042/pirateweather/issues/3).
	* March 25, 2022: API version 1.1.5
    	* Changed the visibility threshold for the fog icon to 1 km per [OFCM](https://web.archive.org/web/20110521015053/http://www.ofcm.gov/fmh-1/pdf/H-CH8.pdf).
		* Part of [issue #30](https://github.com/alexander0042/pirate-weather-ha/issues/30).
	* March 22, 2022: API version 1.1.4
		* Fix a bug when requesting data at the edges of the domain [per issue #41](https://github.com/alexander0042/pirate-weather-ha/issues/41).
	* March 16, 2022: API version 1.1.3
		* Small performance increase (~0.3 s) by changing the way time zones are calculated to use [TimeZoneFinderL](https://timezonefinder.readthedocs.io/en/latest/). This could result in incorrect time zones sometimes, but since this isn't used as part of the weather details, shouldn't pose a major issue. If highly accurate time zones are required, a new `tz=precise` url parameter is available.
		* Return elevation data from [ETPOP1](https://www.ngdc.noaa.gov/mgg/global/).
	* February 18, 2022: API version 1.1.2	
		* Fix for missing alerts that were missing an issued time.
		* Corrected the accumulation when sleet was forecasted (part of [issue #30](https://github.com/alexander0042/pirate-weather-ha/issues/30)).  
	* February 4, 2022: API version 1.1.1	
		* Fix for missing alert description.
	* February 1, 2022: API version 1.1
    	* Bugfix and performance release to clean up some things that didn't make it into V1.0.
    	* Much (30%) faster API response times by changing how the nearest grid cell lookup is performed. The grid cell is now calculated directly using the HRRR/ GFS grid math, as opposed to reading from an index file. The time zone lookup has also been optimized to only call the lookup function once. 
    	* Fixed the implementation of the "exclude" option.
    	* Fixed the US NWS alerts parser.
    	* Per [this issue](https://github.com/alexander0042/pirate-weather-ha/issues/30#issuecomment-1014959232), precipitation intensity is now always returned in mm of water equivalent per hour. 
    	* Per [this issue](https://github.com/alexander0042/pirate-weather-ha/issues/30#issuecomment-1009379064), the precipitation icon is now trigged by 0.25 mm/h of precipitation, instead of 1 mm/h.
    	* Corrected a small bug where a negative precipitation rate could be returned.
      
??? note "Winter 2022"

 	* Winter 2022
    	* Official V1.0 release! These docs have been updated to reflect the current version, but I'll leave the previous version up for reference under the [v0.1 header](https://pirateweather.readthedocs.io/en/latest/indexv01/).
    	* Changed the data ingest pipeline to use AWS Fargate (thanks sponsors!) improving the resolution by 4x!
    	* Added short term historic data via the `time` parameter.
    	* Fixed a long standing issue with wind speeds.
    	* Added support for the `exclude` flag.
    	* Moved the documentation over to ReadTheDocs.
    	* Published the [processing scripts](https://github.com/alexander0042/pirateweather/tree/main/scripts) and [docker image](https://gallery.ecr.aws/j9v4j3c7/pirate-wgrib2).
    	* Added a version tag to the flags field
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

## Version 2.0 Pre-Release Changelog
Changelog for the upcoming version 2.0 of the API

* Version 2.0i
	* April 5, 2024:
 	* Fixed an issue where daylight savings time would offset the daily `time` parameter. This was reported in issue [#134](https://github.com/Pirate-Weather/pirateweather/issues/114)
  	* Fixed an issue where the hourly `time` parameter would be offet for fractional TimeZones as reported in issue [#32](https://github.com/Pirate-Weather/pirateweather/issues/32)
* Version 2.0h
	* April 5, 2024:
 	* Fixed the remaining bugs from issues [#155](https://github.com/Pirate-Weather/pirateweather/issues/155) and [#180](https://github.com/Pirate-Weather/pirateweather/issues/180)
* Version 2.0g
	* March 19, 2024:
 	* Fixed an issue where the currently cloud cover would interpolate from the next hour data to the current hour data.
* Version 2.0f
	* March 19, 2024:
 	* Fixed an issue where the currently cloud cover would interpolate from the next hour data to the current hour data.
* Version 2.0e
	* March 18, 2024:
 	* Fixed an issue where the currently icon and summary would return None instead of an icon
  	* Fixed an issue where the currently icon and summary would return clear instead of the correct icon 
  	* Changed the logic for the currently and minutely `preciptiationIntensity` to return data even if `precipitationProbaility` is zero  
* Version 2.0d
	* March 15, 2024:
 	* Fixed the currently icon thresholds that occured after changing current cloud cover to a percentage 
* Version 2.0c
	* March 13, 2024:
 	* Fixed the daily min/max timing issues (turns out there were several different things that weren't working)
  	* Fixed most of the [#155](https://github.com/Pirate-Weather/pirateweather/issues/155) items
  	* HRRR subhourly and HRRR 0-18 will always be 1-2 hours off now. I'm trying to ingest the subhourly data as fast as possible, so it gets read as soon as four timesteps are published. The hourly data waits until the 18 hour timestep is out, and then has to process the previous 36 hours of data to create a cohesive timeseries. 
* Version 2.0b
	* March 11, 2024:

Excited to announce that the long awaited version 2.0 of the Pirate Weather API is ready for beta testing on the [dev.pirateweather.net](dev.pirateweather.net) endpoint! Ever since issue [#5](https://github.com/Pirate-Weather/pirateweather/issues/5) was opened two years ago, I realized that eventually my back-end would need a rewrite to handle a wider range of cases, and this is the culmination of that effort. I'll have a more detailed write-up eventually, but for now, I wanted to start this thread to consolidate issues with the new API in one place for me to change, as well as announce some of the new features. 

At a high level, there are four main improvements that will impact every request:

1. Includes a fancy new model from NOAA called the National Blend of Models
2. Does a way better job of calculating the daily high/ low/ accumulations for the current day
3. Returns somewhere between 10 and 50 times faster than v1 (this was my favourite to work out). I can't say for sure that it's the fastest weather API out there, but it's definitely in contention now.
4. Faster data ingest (~5 minutes).
5. Improved US alert processing.
6. Nearest storm distance and bearing!

As well as several new optional improvements behind a new `version=2` querystring parameter, to avoid breaking Dark Sky compatibility:

1. Short term (~36 hour) air quality forecasts (top requested feature!).
2. Liquid, snow, and ice precipitation types.
3. Model specific exclusions (`exclude=hrrr` or `exclude=nbm`), to facilitate performance comparisons between models.
7. Returned grid indexes of model results (this seemed small, but since HRRR is in Lambert, it was fairly complex).

* March 8, 2024
	* Currently block added which uses a mix of NBM/HRRR/GFS/GEFS data
	* Daily block added
 	* Alerts block added 
 	* Icon and summary data points added to all blocks
  	* Apparent Temperature now uses data from the GFS model instead of calculating it. This was reported in [issue #76](https://github.com/Pirate-Weather/pirateweather/issues/76) 
 	* Fix issues documented in [issue #155](https://github.com/Pirate-Weather/pirateweather/issues/155)  
* February 18, 2024
	* Hourly and minutely blocks have been added 
* February 6, 2024
	* [National Blend of Models](https://blend.mdl.nws.noaa.gov/) data is now being shown in the API.
 	* Querying by lat/long is now working
  	* Nearest storm data and bearings now return data instead of always returning zero. This was reported in issues [#6](https://github.com/Pirate-Weather/pirateweather/issues/6), [#91](https://github.com/Pirate-Weather/pirateweather/issues/91) and [#121](https://github.com/Pirate-Weather/pirateweather/issues/121)
  	* Development URL is now located at ` http://piratev2lb-a90c79daaddc2625.elb.us-east-1.amazonaws.com:8000/forecastv2/<APIKEY>/<LAT>,<LON>`
* January 4, 2024 
	* Right now, there's not much to look at, since it's only a testing endpoint to make sure that things were flowing; however, it represents a ton of key improvements:
		1. ~100x faster responses
		2. NBM data (although it's not shown yet, it's in there!)
		3. Storm distances and directions
		4. Short term historic data, fixing the daily high/ low issues.
		5. Less interesting, but totally new ingest pipeline that's way more flexible/ maintainable.  
	* To access it, check out: `https://dev.pirateweather.net/forecastv2/<APIKEY>/<X>,<Y>`
	* X and Y are raw grid indexes (I warned it was rough), so keep them between 0-700, and the only data that's returned right now is the -36 hour UTC time for the HRRR model. In the next couple days, I'm going to fix lat/long and expose some of the raw model data (probably current values for everything), so they'll be something to look at! 
