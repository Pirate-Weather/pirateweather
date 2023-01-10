# Roadmap
1. Finish the API documentation.
2. Major change to weather alerts.
    * Using [WMO data](https://severeweather.wmo.int/v2/), I'm planning on returning alerts for all jurisdictions, not just the US! 
	* Alerts are also the slowest part of the API response now, since each polygon is checked. The plan is to interpolate alerts onto a grid as a processing step, letting the API function quickly check a NetCDF file instead.
3. Investigate using radar data.
    *  Investigate if it's feasible to use radar data for the currently conditions. This is a suggestion in [issue #10](https://github.com/alexander0042/pirateweather/issues/10).
4. Text summaries and translations.	
	* Based on the [existing repository](https://github.com/alexander0042/translations).
5. Improve source data.
	* Add in the [Real-Time Mesoscale Analysis model](https://www.nco.ncep.noaa.gov/pmb/products/rtma/) on a rapid (15 minute) update cycle for better current conditions. This is from the suggestion in [issue #30](https://github.com/alexander0042/pirate-weather-ha/issues/30).
	* Add in the [National Blend of Models](https://blend.mdl.nws.noaa.gov/) for better short term precipitation forecasting. 
