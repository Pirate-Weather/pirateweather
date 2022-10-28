# Changelog

For a RSS feed of these changes, subscribe using this link: <https://github.com/alexander0042/pirateweather/commits/main.atom>.

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
* Febuary 1, 2022: API version 1.1
    * Bugfix and performance release to clean up some things that didn't make it into V1.0.
    * Much (30%) faster API response times by changing how the nearest grid cell lookup is performed. The grid cell is now calculated directly using the HRRR/ GFS grid math, as opposed to reading from an index file. The time zone lookup has also been optimized to only call the lookup function once. 
    * Fixed the implementation of the "exclude" option.
    * Fixed the US NWS alerts parser.
    * Per [this issue](https://github.com/alexander0042/pirate-weather-ha/issues/30#issuecomment-1014959232), precipitation intensity is now always returned in mm of water equivalent per hour. 
    * Per [this issue](https://github.com/alexander0042/pirate-weather-ha/issues/30#issuecomment-1009379064), the precipitation icon is now trigged by 0.25 mm/h of precipitation, instead of 1 mm/h.
    * Corrected a small bug where a negative precipitation rate could be returned.
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
  
