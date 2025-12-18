# Changelog

For a RSS feed of these changes, subscribe using this link: <https://github.com/Pirate-Weather/pirate-weather-code/commits/main.atom>.

???+ note "Version 2.9"

	* December 17, 2025, API Version 2.9.0g
		* Fix ERA5 Rounding for precipitation type as per [PR #477](https://github.com/Pirate-Weather/pirate-weather-code/pull/477).
		* Revert missing interp_time_take_blend to fix broken ingest as per [PR #476](https://github.com/Pirate-Weather/pirate-weather-code/pull/476).
	* December 15, 2025, API Version 2.9.0f
		* Fix DWD testing station and runtime as per [PR #475](https://github.com/Pirate-Weather/pirate-weather-code/pull/475).
		* Add ice/mixed precipitation types as per [PR #467](https://github.com/Pirate-Weather/pirate-weather-code/pull/467).
		* Fix DWD Historic data caching as per [PR #474](https://github.com/Pirate-Weather/pirate-weather-code/pull/474).
		* Validate DWD MOSMIX timestamps to prevent invalid sourceList entries as per [PR #473](https://github.com/Pirate-Weather/pirate-weather-code/pull/473).
		* Fix nearest station units as per [PR #472](https://github.com/Pirate-Weather/pirate-weather-code/pull/472).
	* December 8, 2025, API Version 2.9.0e
		* Update DWD ingest to use nearest interpoaltion for ptype as per [PR #463](https://github.com/Pirate-Weather/pirate-weather-code/pull/463).
		* Fix DWD MOSMIX precipitation intensity distribution and temperature validation as per [PR #462](https://github.com/Pirate-Weather/pirate-weather-code/pull/462).
		* Change DWD to nearest within radius interpolation as per [PR #460](https://github.com/Pirate-Weather/pirate-weather-code/pull/460).
		* Fix an issue where a cell with multiple MOSMIX stations displayed data randomly from either station as per [PR #457](https://github.com/Pirate-Weather/pirate-weather-code/pull/457).
	* December 7, 2025, API Version 2.9.0d
		* Fix an issue where DWD MOSMIX data was incorrectly offset as per [PR #456](https://github.com/Pirate-Weather/pirate-weather-code/pull/456).
	* December 7, 2025, API Version 2.9.0c
		* Fix an issue where DWD MOSMIX was showing in the sources for locations with no MOSMIX stations [PR #454](https://github.com/Pirate-Weather/pirate-weather-code/pull/454).
		* Fix an issue where the precipitation type and intensity arrays were not aligned as per [PR #452](https://github.com/Pirate-Weather/pirate-weather-code/pull/452).
		* Added falling back to another source if DWD MOSMIX has no data for that data point [PR #451](https://github.com/Pirate-Weather/pirate-weather-code/pull/451).
			* The available data varies per station so your station may not have the full suite of data. Solar radiation and wind gusts are primarily available for European stations.
	* December 4, 2025, API Version 2.9.0b
		* Fix an issue where some v2 fields were displaying in v1 requests as per [PR #450](https://github.com/Pirate-Weather/pirate-weather-code/pull/450).
		* Add support for DWD MOSMIX forecats where available as per [PR #449](https://github.com/Pirate-Weather/pirate-weather-code/pull/449).
	* December 4, 2025, API Version 2.9.0a
		* Refactor the codebase to break out the functions and simplify the code as [PR #438](https://github.com/Pirate-Weather/pirate-weather-code/pull/438).

??? note "Version 2.8"

	* December 4, 2025, API Version 2.8.5
		* Fix an issue that caused alerts to be duplicated as per [PR #439](https://github.com/Pirate-Weather/pirate-weather-code/pull/439).
	* December 1, 2025, API Version 2.8.4
		* Fix an issue with the minutely summary returning no type with precipitation intensity [PR #427](https://github.com/Pirate-Weather/pirate-weather-code/pull/427).
		* Fix alert ingest for Europe [PR #416](https://github.com/Pirate-Weather/pirate-weather-code/pull/416).
		* Fix an issue where ECMWF forecasted accumulation with no precipitation [PR #424](https://github.com/Pirate-Weather/pirate-weather-code/pull/424).
		* Fix an issue where the daily summary would fail to generate a proper summary when fog and high wind were forecasted as per [PR #422](https://github.com/Pirate-Weather/pirate-weather-code/pull/422).
		* Fix issues where certain data points were not properly rounded as per [PR #417](https://github.com/Pirate-Weather/pirate-weather-code/pull/417) and [PR #421](https://github.com/Pirate-Weather/pirate-weather-code/pull/421).
	* November 18, 2025, API Version 2.8.3
		* Optimized rounding to improve performance as per [PR #408](https://github.com/Pirate-Weather/pirate-weather-code/pull/408)
		* Fixed a broadcast ValueError with the GEFS model where the API assumed it always had the full length of data as per [PR #407](https://github.com/Pirate-Weather/pirate-weather-code/pull/407)
		* Fixed an issue where the API would include outdated alerts as per [PR #407](https://github.com/Pirate-Weather/pirate-weather-code/pull/407)
		* Fix the interpolation for minutely precipitation types per [PR #412](https://github.com/Pirate-Weather/pirate-weather-code/pull/412)
		* Lower the precipitation accumulation threshold for the daily summaries to 0.2 mm/day per [PR #412](https://github.com/Pirate-Weather/pirate-weather-code/pull/412)
		* Fix an issue with UK Alert parsing per [PR #412](https://github.com/Pirate-Weather/pirate-weather-code/pull/412)
	* November 17, 2025, API Version 2.8.2
		* Switched to using an external file sync container (rclone) to allow for multiple workers as per [PR #404](https://github.com/Pirate-Weather/pirate-weather-code/pull/404)
	* November 11, 2025, API Version 2.8.1
		* Changed the snow error calculations to use the density function as per [PR #380](https://github.com/Pirate-Weather/pirate-weather-code/pull/380)
		* Changed snow error calculations use hours where the type is snow and there is snow accumulation as per [PR #381](https://github.com/Pirate-Weather/pirate-weather-code/pull/381)
		* Fixed a KeyError in the minutely summary calculations as per [PR #376](https://github.com/Pirate-Weather/pirate-weather-code/pull/376)
		* Fixed a ValueError caused by alerts with no end time as per [PR #377](https://github.com/Pirate-Weather/pirate-weather-code/pull/376)
		* Alerts with no end date will return -999 as per [PR #378](https://github.com/Pirate-Weather/pirate-weather-code/pull/378)
		* Added padding to the ingest files to fix compatibility with Dask 2025.11.0 [PR #393](https://github.com/Pirate-Weather/pirate-weather-code/pull/393)
	* November 7, 2025, API Version 2.8
		* Added WMO alerts for global alert coverage as per [PR #320](https://github.com/Pirate-Weather/pirate-weather-code/pull/320)
		* Added the ECMWF model for better global forecasts as per [PR #317](https://github.com/Pirate-Weather/pirate-weather-code/pull/317)
		* Added the RTMA-RU model for the currently block for locations inside its domain as per [PR #311](https://github.com/Pirate-Weather/pirate-weather-code/pull/311)
		* Switched historic data source to ERA5 for all requests more than 10 days ago, GFS for requests between 10 days and 24 hours ago, and all models within 24 hours per [PR #330](https://github.com/Pirate-Weather/pirate-weather-code/pull/330)
			* This will improve response times and data consistently for historic requests, while allowing self hosting the Time Machine back end. 
		* Fixed an issue where the day icon, hourly block icon and day/night summary icon was hardcoded to use a day icon as per [PR #362](https://github.com/Pirate-Weather/pirate-weather-code/pull/362)
			* Locations experiencing polar night will no longer have the API return a day icon in these blocks
			* Locations experiencing polar day will see a day icon in the night summary block
		* Refactored the codebase to use SI units throughout as per [PR #348](https://github.com/Pirate-Weather/pirate-weather-code/pull/348)
		* Added a Day/Night Forecast as per [PR #349](https://github.com/Pirate-Weather/pirate-weather-code/pull/349)
			* The day portion of the forecast is calculated from 4am to 4pm and the night forecast is calculated from 5pm to 3am.
		* Added thunderstorm as a summary and icon per [PR #335](https://github.com/Pirate-Weather/pirate-weather-code/pull/335)
			* This means that the default icon set has been updated to include thunderstorm
		* Added solar and CAPE to API response when version>1 as per [PR #321](https://github.com/Pirate-Weather/pirate-weather-code/pull/321)
		* Updated `apparentTemperature` calculation to use solar radiation as per [PR #321](https://github.com/Pirate-Weather/pirate-weather-code/pull/321)
		* Fixed an crash when `nearestSubNational` is missing as per [PR #323](https://github.com/Pirate-Weather/pirate-weather-code/pull/323)

??? note "Version 2.7"

	* October 8, 2025, API Version 2.7.11
		* Add closest state/ province (`nearestSubNational`) and country.
		* Fixed a number of issues for the RTMA-RU/ECMWF/WMO Alerts ingest pipeline to allow for testing these sources in dev (planned for 2.8!)
	* October 8, 2025, API Version 2.7.10
		* Add the capacity to select a unit system automatically as per [PR #290](https://github.com/Pirate-Weather/pirate-weather-code/pull/290).
		* Fix an issue with `stationPressure` as per [PR #291](https://github.com/Pirate-Weather/pirate-weather-code/pull/291).
		* Added the ingest version to flags section behind the `version` query string as per [PR #290](https://github.com/Pirate-Weather/pirate-weather-code/pull/290).
		* Added closest city name to the flags section behind the `version` query string as per [PR #290](https://github.com/Pirate-Weather/pirate-weather-code/pull/290).
		* Added ingest for RTMA-RU as per [PR #263](https://github.com/Pirate-Weather/pirate-weather-code/pull/263).
		* Added ingest for WMO Alerts as per [PR #263](https://github.com/Pirate-Weather/pirate-weather-code/pull/263).
	* October 2, 2025, API Version 2.7.9
		* Fixed station pressure units in [PR #276](https://github.com/Pirate-Weather/pirate-weather-code/pull/276).
		* Updated timemachine data threshold and fixed file reading error [Issue #492](https://github.com/Pirate-Weather/pirateweather/issues/492).
	* September 23, 2025, API Version 2.7.8
		* Add station pressure in [PR #271](https://github.com/Pirate-Weather/pirate-weather-code/pull/271).
		* Added version tags to the release images [PR #267](https://github.com/Pirate-Weather/pirate-weather-code/pull/267).
		* Updated the build to use the most recent wgrib2 version.
	* September 23, 2025, API Version 2.7.7
		* Changed so that bad/ missing data is always returned as -999, instead of clipping to the extreme range in [PR #234](https://github.com/Pirate-Weather/pirate-weather-code/pull/234).
		* Changed the currently and minutely blocks to use reflectivity for precipitation where available as per [#390](https://github.com/Pirate-Weather/pirateweather/issues/390). The current models with reflectivity data are HRRR and GFS.
		* Added estimating the precipitation type when its none in the HRRR sub-hourly as per [PR #262](https://github.com/Pirate-Weather/pirate-weather-code/pull/262).
		* Fixed an issue where it was possible to have the daily `precipType` be snow without any significant accumulation as per [#413](https://github.com/Pirate-Weather/pirateweather/issues/413).
		* Changed snow accumulation to use a density formula instead of just multiplying by ten per [#89](https://github.com/Pirate-Weather/pirateweather/issues/89).
		* Fixed inconsistencies between metric and imperial units where the possible text was showing for imperial units but not on metric units as per [PR #255](https://github.com/Pirate-Weather/pirate-weather-code/pull/255).
		* Fixed an issue where the minutely text summaries were using the wrong accumulation unit as per [PR #261](https://github.com/Pirate-Weather/pirate-weather-code/pull/261).
	* August 11, 2025, API Version 2.7.6
		* Fixed a GFS ingest bug as per [#472](https://github.com/Pirate-Weather/pirateweather/issues/472) and [#429](https://github.com/Pirate-Weather/pirate-weather-ha/issues/429)
		* Fixed inconsistencies between `smoke`, `haze` and `mist`. These conditions now check if visibility is less than 10 km rather than less than or equal to in [PR #230](https://github.com/Pirate-Weather/pirate-weather-code/pull/230).
	* August 7, 2025, API Version 2.7.5
		* Fixed an issue where `nearestStormDistance` was -999 per [#480](https://github.com/Pirate-Weather/pirateweather/issues/480)
		* Fixed an issue where some data points would return -999 per [#486](https://github.com/Pirate-Weather/pirateweather/issues/486)
		* Added updated summaries for daily and translations on TimeMachine endpoint
		* Add smoke, haze and mist as conditions per [#460](https://github.com/Pirate-Weather/pirateweather/issues/460)
			* Smoke, haze and mist now have their own icons using the pirate icon set.
		* Fixed an issue where the `currently` summaries would return "Not Available" if one of `temperature`, `windSpeed`, `dewPoint`, `cloudCover`, `humidity` or `visibility` was -999.
			* Also corrected the icon to be `none` instead of `not-available`
	* July 17, 2025, API Version 2.7.4
	 	* Fixed an issue where `smoke` was always 0 per [#477](https://github.com/Pirate-Weather/pirateweather/issues/477)
	 	* Fixed 504 Gateway Timeouts on TimeMachine endpoint per [#478](https://github.com/Pirate-Weather/pirateweather/issues/478)
		* Added updated summaries for hourly and currently on TimeMachine endpoint
		* Added additional ingest checking to address rare high values per [#472](https://github.com/Pirate-Weather/pirateweather/issues/472)
	* July 10, 2025, API Version 2.7.3 - Bugfix release
	 	* Midnight currently values were sometimes incorrect per [#394](https://github.com/Pirate-Weather/pirateweather/issues/394)
	 	* Timemachine new file version fix per [#471](https://github.com/Pirate-Weather/pirateweather/issues/471)
	 	* Timemachine half hour timezone fix per [#459](https://github.com/Pirate-Weather/pirateweather/issues/459)
	 	* Change currently visibility to use HRRR SubHourly per [#437](https://github.com/Pirate-Weather/pirateweather/issues/437)
	 	* Add an additional check for array sizing (cause of June 26 downtime)
	 	* Add basic code testing [PR #167](https://github.com/Pirate-Weather/pirate-weather-code/pull/1670)
	 	* Assorted summary issues and improvements per [#137](https://github.com/Pirate-Weather/pirate-weather-code/issues/137)
	* June 11, 2025, API Version 2.7.2
	 	* Fixed a [build issue](https://github.com/Pirate-Weather/pirate-weather-code/pull/157)
	* June 9, 2025, API Version 2.7.1
	 	* Fixed an ingest interpolation issue causing inaccurate data per [issue #464](https://github.com/Pirate-Weather/pirateweather/issues/464)
	 	* Allow the  response container to query the raw Zarr files directly to simplify development
	* June 9, 2025, API Version 2.7
	 	* Moved the production API to Zarr v3
	 	* Updated the production API to run off the script in the Docker image
	 	* Added the 24 hour and day summaries as per [issue #48](https://github.com/Pirate-Weather/pirateweather/issues/48)
	 	* Fix `windBearing` and `nearestStormBearing` not being integers as per [#455](https://github.com/Pirate-Weather/pirateweather/issues/455)
	 	* Fix an issue with fractional TimeZones returning odd `currently` data as per [$458](https://github.com/Pirate-Weather/pirateweather/issues/458)
	 	* Fix an issue where the weekly summary could generate a null icon

??? note "Version 2.6"

	* April 16, 2025, API Version 2.6
	 	* Added the weekly and minutely summaries as per [issue #48](https://github.com/Pirate-Weather/pirateweather/issues/48)
		* Updated the daily summaries to show more precipitation information as per [issue #48](https://github.com/Pirate-Weather/pirateweather/issues/48)
			* Note: This is not the full daily summaries and merely enhances the current daily summaries with more precipitation information
		* Fixes an issue where GEFS error was always equal to precipitation accumulation as per [issue #434](https://github.com/Pirate-Weather/pirateweather/issues/434)
		* Add a Pirate Weather iconset as per [issue #402](https://github.com/Pirate-Weather/pirateweather/issues/402).
		* Significant self-hosting improvements per [PR #92](https://github.com/Pirate-Weather/pirate-weather-code/pull/92):
			* Update Zarr to V3.
			* x64 and ARM builds.
			* Optimize Dask code to reduce memory requirements to ~16 GB.
			* Add in ECMWF data (not yet in API).
			* Add in maps data output (not yet in API).
			

??? note "Version 2.5"

	* March 7, 2025, API Version 2.5.4
	 	* The API now returns a HTTP 400 Language Not Supported error for invalid translations instead of defaulting to English.
	* February 28, 2025, API Version 2.5.3
	 	* Fix an issue where the possible precipitation text was generating incorrectly on days with multiple precipitation types forecasted as per [pull request #80](https://github.com/Pirate-Weather/pirate-weather-code/pull/80)
	 	* Allow the GEFS model to be excluded [issue #412](https://github.com/Pirate-Weather/pirateweather/issues/412).
		* Zero intensity on currently and minutely when pop==0 as per [pull request #79](https://github.com/Pirate-Weather/pirate-weather-code/pull/79) and [pull request #81](https://github.com/Pirate-Weather/pirate-weather-code/pull/81).
		* Zero accumulation on hourly when pop==0 as per [pull request #79](https://github.com/Pirate-Weather/pirate-weather-code/pull/79)
	* February 26, 2025, API Version 2.5.2	
	 	* Fix a bug where the maximum intensity time was incorrect.
	 	* Allow the GEFS model to be excluded [issue #412](https://github.com/Pirate-Weather/pirateweather/issues/412).
	* February 26, 2025, API Version 2.5.1	
		* Updated containers to Python 3.13.
		* Improved Dev endpoint stability.
		* Improved monitoring stability
		* Fixed historic data python environment  
	* February 24, 2025, API Version 2.5
		* Added support for the Dark Sky translation module as per [issue #152](https://github.com/Pirate-Weather/pirateweather/issues/152)!
		* Document liquid water ratio in intensity to [align with Dark Sky](https://github.com/Pirate-Weather/pirate-weather-code/pull/53#issuecomment-2661603131). 
		* Zero intensity when pop==0 (https://github.com/Pirate-Weather/pirate-weather-code/issues/30).
		* Updated Docker containers to remove old pip requirements.
		* Move to Zarr V3 for the response script!
		* Corrected an issue where the fire index was capped at 15 instead of 100.

??? note "Version 2.4"

	* December 10, 2024, API Version 2.4.2
		* Quick bugfix to address an issue with alert ingest and ERA5 data retrieval for January dates.
	* November 26, 2024, API Version 2.4.1
		* Fixed unit issues that occured when fixing the data point value issue as per [issue #360](https://github.com/Pirate-Weather/pirateweather/issues/360).
	* November 25, 2024, API Version 2.4
		* First Official Open Source Release! Details in the new [Pirate Weather Code](https://github.com/Pirate-Weather/pirate-weather-code) repository, but starting today, you can see exactly how the data is processed, and even host your own instance of Pirate Weather! Contributions are welcome, so come check it out. Addresses the second oldest outstanding [issue #11](https://github.com/Pirate-Weather/pirateweather/issues/11).
		* Fixed a datetime bug per [issue #330](https://github.com/Pirate-Weather/pirate-weather-ha/issues/330). 
		* Corrects the Apparent Temperature calculation per [issue #363](https://github.com/Pirate-Weather/pirateweather/issues/363).
		* Changed the behaviour of new lines in NWS per [issue #367](https://github.com/Pirate-Weather/pirateweather/issues/367). 
		* Fixed issues where data points could return values outside of expected range as per [issue #360](https://github.com/Pirate-Weather/pirateweather/issues/360).

??? note "Version 2.3"

	* October 25, 2024, API Version 2.3.3
		* Updated cache parameters per [issue #350](https://github.com/Pirate-Weather/pirateweather/issues/350). 
		* Changed alert start time to use NWS effective time instead of onset time per [issue #353](https://github.com/Pirate-Weather/pirateweather/issues/353). 
		* Added line breaks in NWS alert descriptions [issue #353](https://github.com/Pirate-Weather/pirateweather/issues/353). 
		* Removed extra white space in NWS alert regions per [issue #353](https://github.com/Pirate-Weather/pirateweather/issues/353). 
		* Fixed a rounding issue in precipitation intensity per [issue #211](https://github.com/Pirate-Weather/pirateweather/issues/211). 
		* Added current day precipitation per [issue #211](https://github.com/Pirate-Weather/pirateweather/issues/211). 
		* Added a check to filter invalid data per [issue #354](https://github.com/Pirate-Weather/pirateweather/issues/354).  
	* October 7, 2024, API Version 2.3.2
		* Simplify US alert headline details per [issue #344](https://github.com/Pirate-Weather/pirateweather/issues/344).
		* Correct how Current Fire Index outside of NBM area is returned. -999 (for "No Data" is now displayed instead of 0.
	* September 23, 2024, API Version 2.3.1
		* Fixed some issues with Time Machine causing slow responses for the production API.
		* Added missing Dark Sky headers per [issue #334](https://github.com/Pirate-Weather/pirateweather/issues/334).
		* Fix for requested times on the hour returning incorrect data.
		* Updates to Apiable docs per [issue #324](https://github.com/Pirate-Weather/pirateweather/issues/324).
		* Assorted other time machine fixes per [issue #330](https://github.com/Pirate-Weather/pirateweather/issues/330).
		* Changed humidity priority to HRRR for consistency with dewpoint per [issue #282](https://github.com/Pirate-Weather/pirateweather/issues/282).
		* Started work on an interactive Swagger documentation at <https://api.pirateweather.net/docs>.   
	* September 13, 2024, API Version 2.3
		* Major Time Machine (historic data) update!
			* ERA-5 data now available from January 1940 to June 2024 via the excellent [NCAR archive](https://registry.opendata.aws/nsf-ncar-era5/)!
			* Performance for these requests has been considerably improved (~10 s), since it is no longer querying against the Google data.
			* Implemented using the excellent [Kerchunk library](https://fsspec.github.io/kerchunk)
			* The June 2024 end date will be moved up as the ERA-5 data is updated.
			* [Issue #130](https://github.com/Pirate-Weather/pirateweather/issues/130)
			* [Issue #316](https://github.com/Pirate-Weather/pirateweather/issues/316)
		* Historic model 1-hour forecast data is now available from June 2024 to present via the Pirate Weather Zarr archive.
			* While technically forecast data, these forecasts are as close to observations as possible.
			* Slower than ERA-5, since the full range of forecast models is used (~30 s).
		* Historic data is now accessible from both the timemachine.pirateweather.net endpoint and the api.pirateweather.net endpoint.
		* Documentation updates:
			* [Issue #315](https://github.com/Pirate-Weather/pirateweather/issues/315)
			* [Issue #320](https://github.com/Pirate-Weather/pirateweather/issues/320)
		* Added the ability to provide the API key as a query parameter or header (as `apikey`) per [issue #314](https://github.com/Pirate-Weather/pirateweather/issues/314).
		* Improved error handling for invalid locations per [issue #318](https://github.com/Pirate-Weather/pirateweather/issues/318)
		* Fixed an unreported bug for max/min Apparent Temperature Times

??? note "Version 2.2"

	* August 20, 2024, API Version 2.2
		* No endpoint facing changes, but a lot of backend reworking 
			* Switched back from the LMDB to a file based approach for ingesting new data, with a new timing function for updates. This approach is also faster, with most requests returning in <10 ms
			* Changed how Kong checks API keys to simplify the update roadmap for Kong
			* Added a container restart policy for the dev container to allow for faster updates  

??? note "Version 2.1"

	* August 16, 2024, API Version 2.1.2
		* Fixed the pressure variable showing surface level pressure instead of sea level pressure in the HRRR domain
	* August 16, 2024, API Version 2.1.1
		* Added a returned header for "X-Node-ID", allowing which of the two nodes a request is served by to be tracked for debugging
		* Fixed pressure variable to show Mean Sea Level Pressure
		* Updated how the .dev backend works, making it more unstable but also faster to get updates.  
			* A gentle reminder that this backend should not be used for production workloads and may serve incorrect/ outdated data, or no data at all.
	* August 15, 2024, API Version 2.1
		* Switched Apparent Temperature to use the Australian Bureau of Meteorology equation to improve accuracy and consistency.
		* Added a new "FeelsLike" parameter for raw model outputs
		* Moved things from disk based storage to a LMDB database called [Garnet](https://github.com/microsoft/garnet) which fixes the issue of the API returning weird results as reported in:
  			* [issue #229](https://github.com/Pirate-Weather/pirateweather/issues/229)
  			* [issue #255](https://github.com/Pirate-Weather/pirateweather/issues/255)
  			* [issue #249](https://github.com/Pirate-Weather/pirateweather/issues/249)
  			* [issue #266](https://github.com/Pirate-Weather/pirateweather/issues/266)
  			* [issue #283](https://github.com/Pirate-Weather/pirateweather/issues/283)
  			* [issue #284](https://github.com/Pirate-Weather/pirateweather/issues/284)
		* Fixed an issue where a `none` icon and summary would be returned due to an issue with the interpolation for the minutely data, essentially when the probability/ amount of precipitation increases significantly from one 3-hourly output timestep to the next as reported in issue [#281](https://github.com/Pirate-Weather/pirateweather/issues/281)
		* Improved the times for daily high/ low calculations in [issue #268](https://github.com/Pirate-Weather/pirateweather/issues/268)
     	* Prevented the API from returning incorrect data for requests more than 36 hours in the past
       	* Finally fixed the bug preventing results from being returned on the first day of the month

??? note "Version 2.0"

	* July 9, 2024, API Version 2.0.11
		* Added a check to the HRRR ingest script to check for misformed input files
		* The API now falls back to using NBM/GFS data instead of returning an Internal Server Error
		* These issues were reported in [#258](https://github.com/Pirate-Weather/pirateweather/issues/258)
	* June 18, 2024, API Version 2.0.10
		* Fixed a bug where `precipAccumulation` was being calculated from the GFS model instead of the GEFS model as per [#229](https://github.com/Pirate-Weather/pirateweather/issues/229)
	* May 30, 2024, API Version 2.0.9
		* Adjust the icon calculation approach to fix issues with a small number of very rainy hours per issue [#236](https://github.com/Pirate-Weather/pirateweather/issues/236).
  		* Changed the icon/ summary to use 4 am to 4 am for calculations to follow the Dark Sky approach per discussion [#239](https://github.com/Pirate-Weather/pirateweather/discussions/239).
	* May 21, 2024, API Version 2.0.8
		* Yet more error handling code to handle cases when model input files are misformed. 
	* May 15, 2024, API Version 2.0.7
		* New error handling code to handle cases when model input files are misformed. 
	* May 7, 2024, API Version 2.0.6
  		* Fixed a bug in the time specification processing [#211](https://github.com/Pirate-Weather/pirateweather/issues/221).
	* May 7, 2024, API Version 2.0.5
  		* Change near surface smoke units to be ug/m3.
	* May 6, 2024, API Version 2.0.4
  		* Fixed a bug in the grid index processing [#216](https://github.com/Pirate-Weather/pirateweather/issues/216)
  		* Enabled CORS support [#215](https://github.com/Pirate-Weather/pirateweather/issues/215)
	* April 30, 2024 and May 1, 2024, API Version 2.0.3
  		* Fixed a bug in the datetime rounding code failed because of the month rollover as reported in [#208](https://github.com/Pirate-Weather/pirateweather/issues/208)
  		* Fixed a bug where `precipType` would sometimes not adjust for the temperature
  		* Changed `precipProbability` to show the chance of precipitation for the rest of the day rather than the day as a whole.
  		* These issues were reported in [#205](https://github.com/Pirate-Weather/pirateweather/issues/205)
 	* April 30, 2024, API Version 2.0.2
  		* Fixed a bug where excluding data blocks broke as part of the 2.0 update as reported in [#108](https://github.com/Pirate-Weather/pirateweather/issues/108)
 	* April 24, 2024, API Version 2.0.1
  		* Fixed a bug where cloud cover could go below zero
  		* Fixed a bug in the sourceIDX section where negative longitude would display incorrectly.
  		* Fixed a bug where `precipAccumulation` would sometimes show more than four decimal points

??? note "Pre-Release Version 2.0"

	* Version 2.0l
		* April 18, 2024:
  		* Added fire index to currently 
		* Added fireIndexMaxTime to daily
		* Fixed a bug where the source time for the HRRR model 0-18 model was incorrect
		* Fixed a bug where the fire index wasn't ingesting
		* Added model lat lon values
 	* Version 2.0k
		* April 11, 2024:
	 	* Added `fireIndex`, `fireIndexMax` and `fireIndexMaxTime` which is behind the `version=2` parameter. Data is available in the US and parts of Canada. This was suggested in issue [#119](https://github.com/Pirate-Weather/pirateweather/issues/119)
   		* Fixed the precipitation probability rounding
   		* Added another icon check for no precipitation
   		* Fixed negative precipitation intensity
   		* Set the accumulation threshold to 0.02 mm for minutely/ hourly
	* Version 2.0j
		* April 9, 2024:
	 	* Changed the threshold to show the precipitaion icon in the currently block to 0.02 mm/h
	* Version 2.0i
		* April 5, 2024:
	 	* Fixed an issue where daylight savings time would offset the daily `time` parameter. This was reported in issue [#134](https://github.com/Pirate-Weather/pirateweather/issues/114)
	  	* Fixed an issue where the hourly `time` parameter would be offet for fractional TimeZones as reported in issue [#32](https://github.com/Pirate-Weather/pirateweather/issues/32)
	  	* Added dawnTime and duskTime which is behind the `version=2` parameter. This was suggested in discussion [#144](https://github.com/Pirate-Weather/pirateweather/discussions/144) and issue [#154](https://github.com/Pirate-Weather/pirateweather/issues/154) which was created from the discussion
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
		* Excited to announce that the long awaited version 2.0 of the Pirate Weather API is ready for beta testing on the [dev.pirateweather.net](dev.pirateweather.net) endpoint!
	 	* At a high level, there are four main improvements that will impact every request:
			1. Includes a fancy new model from NOAA called the National Blend of Models
			2. Does a way better job of calculating the daily high/ low/ accumulations for the current day
			3. Returns somewhere between 10 and 50 times faster than v1 (this was my favourite to work out). I can't say for sure that it's the fastest weather API out there, but it's definitely in contention now.
			4. Faster data ingest (~5 minutes).
			5. Improved US alert processing.
			6. Nearest storm distance and bearing!
	  	* As well as several new optional improvements behind a new `version=2` querystring parameter, to avoid breaking Dark Sky compatibility:
			1. Short term (~36 hour) smoke forecasts.
	  		2. Liquid, snow, and ice precipitation types.
	  	 	3. Model specific exclusions (`exclude=hrrr` or `exclude=nbm`), to facilitate performance comparisons between models.
	  	  	4. Returned grid indexes of model results (this seemed small, but since HRRR is in Lambert, it was fairly complex).
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

??? note "Version 1.5"
	
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

## Time Machine Changelog

* October 31, 2025
	* Changed TimeMachine to use the Google ERA5 dataset
		* Requests for the last 24 hours use all the sources and are unchanged;
		* Request for the last 10 days rely only on GFS data (although ECMWF would be easy to add) stored in the zip file on the server;
		* Requests >10 days rely on Google's ERA5 zarr dataset, which is a perfect source for this sort of application.
* December 9, 2024
	* Added a per API key rate limit of 1 to 4/ per second (depending on the plan) to prevent instabililty as per [https://github.com/Pirate-Weather/pirate-weather-code/issues/30#issuecomment-2528680513](https://github.com/Pirate-Weather/pirate-weather-code/issues/30#issuecomment-2528680513)
* September 13, 2024
	* Major time machine (historic data) update!
		* ERA-5 data now available from January 1940 to June 2024 via the excellent [NCAR archive](https://registry.opendata.aws/nsf-ncar-era5/)!
		* Performance for these requests has been considerably improved (~10 s), since it is no longer querying against the Google data.
		* Implemented using the excellent [Kerchunk library](https://fsspec.github.io/kerchunk)
		* The June 2024 end date will be moved up as the ERA-5 data is updated.
		* [Issue #130](https://github.com/Pirate-Weather/pirateweather/issues/130)
		* [Issue #316](https://github.com/Pirate-Weather/pirateweather/issues/316)
	* Historic model 1-hour forecast data is now available from June 2024 to present via the Pirate Weather Zarr archive.
		* While technically forecast data, these forecasts are as close to observations as possible.
		* Slower than ERA-5, since the full range of forecast models is used (~30 s).
	* Historic data is now accessible from both the timemachine.pirateweather.net endpoint and the api.pirateweather.net endpoint.
* April 18, 2024
	* Fixed an issue where locations in fractional timezones were not returning an error as reported in [#194](https://github.com/Pirate-Weather/pirateweather/issues/194)
* March 11, 2024
	* Fixed an issue where using local time format returned an Invalid Time Specification error as reported in issue [#162](https://github.com/Pirate-Weather/pirateweather/issues/162)
* January 16, 2024
	* Change the Time Machine to use ERA-5 model data from Google's dataset as AWS removed it. This was reported in [#130](https://github.com/Pirate-Weather/pirateweather/issues/130)
 		* As a result of the change the Time Machine endpoint only has historical data until May 2023
* August 29, 2023
	* Fixed an issue where some legacy keys could not consume the Time Machine endpoint reported in [#98](https://github.com/Pirate-Weather/pirateweather/issues/98)
* July 10, 2023
	* Fixed an issue with the timing of a day that rolls over into the next month as reported in issue [#86](https://github.com/Pirate-Weather/pirateweather/issues/86) 
* June 19, 2023
	* Fixed an issue where locations in fractional timezones were not returning an error as reported in [#74](https://github.com/Pirate-Weather/pirateweather/issues/74)
* May 27, 2023
	* Fixed an issue where negative longatide and latitude would be parsed as positive. This was reported in [#67](https://github.com/Pirate-Weather/pirateweather/issues/67)
* April 6, 2023
	* Fixed an issue where `apparentTemperatureMinTime` and `apparentTemperatureLowTime` were not returning UNIX timestamps. This was reported in issue [#46](https://github.com/Pirate-Weather/pirateweather/issues/46)
* March 20, 2023
	* Fixed an issue where Time Machine data was returning an error for dates after June 30, 2022
 	* Fixed the data in the currently block
  	* Integers are integered, floats are rounded to 2 decimal points
  	* Text descriptions are now much better
  	* These issues were reported in issue [#18](https://github.com/Pirate-Weather/pirateweather/issues/18)
* December 23, 2021
	* Fixed an issue where daylight savings time was being ignored as reported in [#4](https://github.com/alexander0042/alexander0042.github.io/issues/4)
* August 3, 2021
	* Fixed an issue where a combination of a time zone glitch and an issue with dates that were the last day of a month, since they required two separate calls to the archive.
 	* Fixed a couple other issues pertaining to rain/snow units
  	* These issues were reported in [#3](https://github.com/alexander0042/alexander0042.github.io/issues/3) 

