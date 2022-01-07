# Changelog
* Recent Updates- Winter 2022
  * Official V1.0 release! These docs have been updated to reflect the current version, but I'll leave the previous version up for reference under the [v0.1 header](https://pirateweather.readthedocs.io/en/latest/indexv01/). Some of the highlights of this release are:

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
  
