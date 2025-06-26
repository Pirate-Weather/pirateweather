# API Docs
This page serves as the documentation for the underlying data source algorithm for the Pirate Weather API- in sort, it explains which parameter comes from where. Since the goal of this API to to provide raw model data with as little processing as possible, results from the API should very closely match the model described in this document, with some minor differences due to interpolation. 

## Data sources
Several models are used to produce the forecast. They are all hosted on [AWS's Open Data Platform](https://registry.opendata.aws/collab/noaa/), and the fantastic [Herbie package](https://github.com/blaylockbk/Herbie) is used to download and perform initial processing for all of them.    

#### NBM
The National Blend of Models [(NBM)](https://vlab.noaa.gov/web/mdl/nbm) is a calibrated blend of both NOAA and non-NOAA weather models from around the world. Running every hour for about 7 days, the NBM produces a forecast that aims to leverage strengths from each of the source models, as well as providing some probabilistic forecasts. For most weather elements in the US and Canada, this is the primary source. 

#### HRRR
The High Resolution Rapid Refresh [(HRRR)](https://rapidrefresh.noaa.gov/hrrr/) provides forecasts over all of the continental US, as well as most of the Canadian population. 15-minute forecasts every 3 km are provided every hour for 18 hours, and every 6 hours a 48-hour forecast is run, all at a 3 km resolution. This was perfect for this project, since Dark Sky provided a minute-by-minute forecast for 1 hour, which can be loosely approximated using the 15-minute HRRR forecasts.

#### GFS
The Global Forecast System [(GFS)](https://www.ncdc.noaa.gov/data-access/model-data/model-datasets/global-forcast-system-gfs) is NOAA's global weather model. Running with a resolution of about 30 km (0.25 degrees), the GFS model provides hourly forecasts out of 120 hours, and 3-hour forecasts out to 240 hours. Here, GFS data is used for anywhere in the world not covered by the HRRR model, and for all results past 48 hours. 

The GFS model also underpins the Global Ensemble Forecast System [(GEFS)](https://www.ncdc.noaa.gov/data-access/model-data/model-datasets/global-ensemble-forecast-system-gefs), which is the 30-member ensemble (the website says 21, but there are 30 data files) version of the GFS. This means that 30 different "versions" of the model are run, each with slightly different starting assumptions. The API uses the GEFS to get precipitation type, quantity, and probability, since it seemed like the most accurate way of determining this. I have no idea how Dark Sky did it, and I am very open to feedback about other ways it could be assigned, since getting the precipitation probability number turned out to be one of the most complex parts of the entire setup! 

#### GEFS
The Global Ensemble Forecast System [(GEFS)](https://www.ncei.noaa.gov/products/weather-climate-models/global-ensemble-forecast) is the ensemble version of NOAA's GFS model. By running different variations parameters and inputs, 30 different versions of this model are run at the same time, providing 3-hour forecasts out to 240 hours. The API uses the GEFS to get precipitation type, quantity, and probability, since it seemed like the most accurate way of determining this. I have no idea how Dark Sky did it, and I am very open to feedback about other ways it could be assigned, since getting the precipitation probability number turned out to be one of the most complex parts of the entire setup! 

### ERA5
To provide historic weather data, the [NCAR European Reanalysis 5 Dataset](https://registry.opendata.aws/nsf-ncar-era5/) is used. This source uses NetCDF4 files saved on S3, which lets them be accessed directly from S3; however, it's not particularly fast, making it only suitable for historic requests. 


## Forecast element sources
Every Pirate Weather forecast element for each time block (`currently`, `minutely`, `hourly`, or `daily`) is included in the table below, along with the primary, secondary, and tertiary data sources. Fallback sources are used if model data is intentionally excluded, the request point is outside of the primary model coverage area, or if there's some sort of data interruption. 

At a high level, the general approach is to use NBM first, then HRRR, then GEFS, the GFS. However, for Currently and minutely results data from the sub-hourly (15 minute) HRRR model is preferred when it is available (not all variables are included in sub hourly, notably cloud cover, which would be great to have).  


|Parameter 	            |Currently                    |Minutely   			    |Hourly/ Daily          	|
|-----------------------|-----------------------------|-------------------------|---------------------------|
|apparentTemperature	|HRRR_SubH > NBM > GFS	      |N/A   				    |NBM > HRRR > GFS		 	|
|cloudCover   			|NBM > HRRR > GFS   	      |N/A   				    |NBM > HRRR > GFS   		|
|currentDayIce		    |NBM > HRRR > GEFS > GFS      |N/A					    |N/A						|
|currentDayLiquid       |NBM > HRRR > GEFS > GFS      |N/A					    |N/A						|
|currentDaySnow         |NBM > HRRR > GEFS > GFS      |N/A					    |N/A						|
|dewPoint     			|HRRR_SubH > NBM > GFS        |N/A   				    |NBM > HRRR > GFS   		|
|fireIndex    			|NBM   			  		      |N/A   				    |NBM   			 			|
|feelsLike    			|NBM > GFS  			      |N/A   				    |NBM > GFS		 			|
|humidity     			|HRRR > NBM > GFS   	      |N/A   				    |NBM > HRRR > GFS   		|
|iceAccumulation   		|N/A                          |N/A   				    |NBM > HRRR > GEFS > GFS	|
|liquidAccumulation 	|N/A                          |N/A   				    |NBM > HRRR > GEFS > GFS	|
|nearestStormBearing	|GFS   					      |N/A   				    |GFS   						|
|nearestStormDistance   |GFS   					      |N/A   				    |GFS   						|
|ozone   				|GFS   					      |N/A   				    |GFS   						|
|precipAccumulation 	|N/A                          |N/A   				    |NBM > HRRR > GEFS > GFS	|
|precipIntensity   		|HRRR_SubH > NBM > GEFS       |HRRR_SubH > NBM > GEFS	|NBM > HRRR > GEFS			|
|precipIntensityError	|GEFS					      |GEFS					    |GEFS						|	
|precipProbability  	|NBM > GEFS 			      |NBM > GEFS 			    |NBM > GEFS					|
|precipType   			|HRRR_SubH > NBM > GEFS       |HRRR_SubH > NBM > GEFS	|NBM > HRRR > GEFS			|
|pressure   			|HRRR > GFS   			      |N/A				        |HRRR > GFS 				|
|snowAccumulation   	|N/A					      |N/A   				    |NBM > HRRR > GEFS > GFS 	|
|smoke   				|HRRR   				      |N/A   				    |HRRR  						|
|temperature   			|HRRR_SubH > NBM > GFS        |N/A   				    |NBM > HRRR > GFS   		|
|uvIndex   				|GFS   					      |N/A   				    |GFS   						|
|visibility   			|HRRR_SubH > NBM > HRRR > GFS |N/A   				    |NBM > HRRR > GFS   		|
|windBearing  			|HRRR_SubH > NBM > GFS        |N/A   				    |NBM > HRRR > GFS   		|
|windGust   			|HRRR_SubH > NBM > GFS        |N/A   				    |NBM > HRRR > GFS   		|
|windSpeed   			|HRRR_SubH > NBM > GFS        |N/A				        |NBM > HRRR > GFS   		|

## Data Pipeline

### Trigger
Forecasts are saved from NOAA onto the [AWS Public Cloud](https://registry.opendata.aws/collab/noaa/) into three buckets for the [HRRR](https://registry.opendata.aws/noaa-hrrr-pds/), [GFS](https://registry.opendata.aws/noaa-gfs-bdp-pds/), and [GEFS](https://registry.opendata.aws/noaa-gefs/) models. Since I couldn't find a good way to trigger processing tasks based on S3 events in a public bucket, the ingest system relies on timed events scheduled through [AWS EventBridge Rules](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-create-rule-schedule.html), with the timings shown in the table below:

| Model                | Run Times (UTC) | Delay | Ingest Times (UTC)    |
|----------------------|-----------------|-------|-----------------------|
| GFS                  | 0,6,12,18       | 5:00  | 5,11,17,23            |
| GEFS                 | 0,6,12,18       | 7:00  | 7,13,19,1             |
| NBM                  | 0-24            | 1:45  | 1:45-00:45            |
| HRRR- 48h            | 0,6,12,18       | 2:30  | 2:30,8:30,14:30,20:30 |
| HRRR- 18h/ SubHourly | 0-24            | 1:45  | 1:45-00:45        	 |
