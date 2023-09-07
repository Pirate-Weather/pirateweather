# Roadmap
1. Improve the ingest scripts to keep the forecast initialization model results. This will allow for much better daily high and low data, as well as more accurate short term historical results.
	* Adding in the returned grid point.
	* More accurate snow height estimates for HRRR and liquid/solid breakout.
 	* Additional precipitation types.
  	* Open source!
   	* Nearest storm based on precipitation.
2. Weather maps from new Zarr datafiles.
3. Text summaries and translations.	
	* Based on the [existing repository](https://github.com/alexander0042/translations).
 	* Or possibly AI if it's fast enough! 
4. Finish the API documentation.
5. Add in alerts for Canada/ EU/ other.
6. Investigate using radar data/station data.
    *  Investigate if it's feasible to use radar data and/or station data for the currently conditions. This is a suggestion in [issue #10](https://github.com/alexander0042/pirateweather/issues/10).
7. Improve source data.
	* Add in the [Real-Time Mesoscale Analysis model](https://www.nco.ncep.noaa.gov/pmb/products/rtma/) on a rapid (15 minute) update cycle for better current conditions. This is from the suggestion in [issue #30](https://github.com/alexander0042/pirate-weather-ha/issues/30).
	* Add in the [National Blend of Models](https://blend.mdl.nws.noaa.gov/) for better short term precipitation forecasting. Specifically, I'm waiting for v4.1 of this to be released on AWS.
	* Add in HRRR Smoke for an Air Quality Index. 
