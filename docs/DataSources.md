# API Docs
This page serves as the documentation for the underlying data source algorithm for the Pirate Weather API- in sort, it explains which parameter comes from where. Since the goal of this API to to provide raw model data with as little processing as possible, results from the API should very closely match the model described in this document, with some minor differences due to interpolation. 

## Data sources
Several models are used to produce the forecast. They are all hosted on [AWS's Open Data Platform](https://registry.opendata.aws/collab/noaa/), and the fantastic [Herbie package](https://github.com/blaylockbk/Herbie) is used to download and perform initial processing for all of them.    

#### NBM
The National Blend of Models [(NBM)](https://vlab.noaa.gov/web/mdl/nbm) is a calibrated blend of both NOAA and non-NOAA weather models from around the world. Running every hour for about days, the NBM produces a forecast that aims to leverage strengths from each of the source models, as well as providing some probabilistic forecasts. For most weather elements in the US and Canada, this is the primary source. 

#### HRRR
The High Resolution Rapid Refresh [(HRRR)](https://rapidrefresh.noaa.gov/hrrr/) provides forecasts over all of the continental US, as well as most of the Canadian population. 15-minute forecasts every 3 km are provided every hour for 18 hours, and every 6 hours a 48-hour forecast is run, all at a 3 km resolution. This was perfect for this project, since Dark Sky provided a minute-by-minute forecast for 1 hour, which can be loosely approximated using the 15-minute HRRR forecasts.

#### GFS
The Global Forecast System [(GFS)](https://www.ncdc.noaa.gov/data-access/model-data/model-datasets/global-forcast-system-gfs) is NOAA's global weather model. Running with a resolution of about 30 km (0.25 degrees), the GFS model provides hourly forecasts out of 120 hours, and 3-hour forecasts out to 240 hours. Here, GFS data is used for anywhere in the world not covered by the HRRR model, and for all results past 48 hours. 

The GFS model also underpins the Global Ensemble Forecast System [(GEFS)](https://www.ncdc.noaa.gov/data-access/model-data/model-datasets/global-ensemble-forecast-system-gefs), which is the 30-member ensemble (the website says 21, but there are 30 data files) version of the GFS. This means that 30 different "versions" of the model are run, each with slightly different starting assumptions. The API uses the GEFS to get precipitation type, quantity, and probability, since it seemed like the most accurate way of determining this. I have no idea how Dark Sky did it, and I am very open to feedback about other ways it could be assigned, since getting the precipitation probability number turned out to be one of the most complex parts of the entire setup! 

#### GEFS
The Global Ensemble Forecast System [(GEFS)](https://www.ncei.noaa.gov/products/weather-climate-models/global-ensemble-forecast) is the ensemble version of NOAA's GFS model. By running different variations parameters and inputs, 30 different versions of this model are run at the same time, providing 3-hour forecasts out to 240 hours. The API uses the GEFS to get precipitation type, quantity, and probability, since it seemed like the most accurate way of determining this. I have no idea how Dark Sky did it, and I am very open to feedback about other ways it could be assigned, since getting the precipitation probability number turned out to be one of the most complex parts of the entire setup! 

### ERA5
To provide historic weather data, the [European Reanalysis 5 Dataset](https://registry.opendata.aws/ecmwf-era5/) is used. This source is particularly interesting, since unlike the real-time NOAA models that I need to convert, it's provided in the "cloud native" [Zarr](https://zarr.readthedocs.io/en/stable/) file format. This lets the data be accessed directly and quickly in S3 from Lambda. There aren't nearly as many, many parameters available as with the GFS or HRRR models, but there are enough to cover the most important variables. 


## Forecast element sources
Every Pirate Weather forecast element for each time block (`currently`, `minutely`, `hourly`, or `daily`) is included in the table below, along with the primary, secondary, and tertiary data sources. Fallback sources are used if model data is intentionally excluded, the request point is outside of the primary model coverage area, or if there's some sort of data interruption. 


|Parameter 	|Currently   |Minutely   |Hourly/ Daily   |
|---|---|---|---|---|
|apparentTemperature	|NBM > GFS				|N/A   	|NBM > GFS   			 	|
|cloudCover   			|NBM > HRRR > GFS   	|N/A   	|NBM > HRRR > GFS   		|		
|dewPoint     			|NBM > HRRR > GFS   	|N/A   	|NBM > HRRR > GFS   		|
|fireIndex    			|NBM   			  		|N/A   	|NBM   			 			|
|humidity     			|NBM > HRRR > GFS   	|N/A   	|NBM > HRRR > GFS   		|
|iceAccumulation   		|NBM > HRRR > GEFS > GFS|N/A   	|NBM > HRRR > GEFS > GFS	|
|liquidAccumulation 	|NBM > HRRR > GEFS > GFS|N/A   	|NBM > HRRR > GEFS > GFS	|
|nearestStormBearing	|GFS   					|N/A   	|GFS   						|
|nearestStormDistance   |GFS   					|N/A   	|GFS   						|
|ozone   				|GFS   					|N/A   	|GFS   						|
|precipAccumulation 	|NBM > HRRR > GEFS > GFS|N/A   	|NBM > HRRR > GEFS > GFS	|
|precipIntensity   		|NBM > HRRR > GEFS 		|HRRR	|NBM > HRRR > GEFS			|
|precipIntensityError	|GEFS					|GEFS	|GEFS						|	
|precipProbability  	|NBM > GEFS 			|NBM 	|NBM > GEFS					|
|precipType   			|NBM > HRRR > GEFS 		|HRRR  	|NBM > HRRR > GEFS			|
|pressure   			|HRRR > GFS   			|N/A	|HRRR > GFS 				|
|snowAccumulation   	|NBM > HRRR > GEFS > GFS|N/A   	|NBM > HRRR > GEFS > GFS 	|
|smoke   				|NBM   					|N/A   	|NBM   						|
|temperature   			|NBM > HRRR > GFS   	|N/A   	|NBM > HRRR > GFS   		|
|uvIndex   				|GFS   					|N/A   	|GFS   						|
|visibility   			|NBM > HRRR > GFS   	|N/A   	|NBM > HRRR > GFS   		|
|windBearing  			|NBM > HRRR > GFS   	|N/A   	|NBM > HRRR > GFS   		|
|windGust   			|NBM > HRRR > GFS   	|N/A   	|NBM > HRRR > GFS   		|
|windSpeed   			|NBM > HRRR > GFS   	|N/A	|NBM > HRRR > GFS   		|
