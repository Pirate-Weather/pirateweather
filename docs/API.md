# API Docs
This page serves as the documentation for the Pirate Weather API call and response format. Since this service is designed to be a drop in replacement for the [Dark Sky API](https://web.archive.org/web/20200723173936/https://darksky.net/dev/docs), the goal is to match that as closely as possible, and any disagreement between their service and Pirate Weather will be treated as a bug. However, as Pirate Weather continues to evolve, I plan on adding small, non-breaking additions where I can, and they will be documented here! Plus, always better to have my own (open source and editable) version of the docs!

## Request
The minimum structure for every request to this service is the same:
```
      https://api.pirateweather.net/forecast/[apikey]/[latitude],[longitude]
``` 
This specifies the service (either `api` or `timemachine`), root url (`pirateweather.net/forecast`), the api key used in the request (`[apikey]`), and the location (`[latitude],[longitude]`). There are many other ways to customize this request, but this is the minimum requirement! Calling the API with this request will return a JSON data structure (described below) with the requested weather information!
All request attributes are contained within the URL. Request headers are not parsed by the API, and returned headers only contain debugging information, with all the data contained in the JSON payload. 

### Request Parameters
The forecast request can be extended in several ways by adding parameters to the URL. The full set of URL options is:
```
      https://api.pirateweather.net/forecast/[apikey]/[latitude],[longitude],[time]?exclude=[excluded]&units=[unit]&extend=[hourly]&tz=[precise]
``` 

#### API Key
The API key needs to be requested from <https://pirateweather.net/>. After signing up for the service, the forecast API needs to be subscribed to, by logging in and clicking subscribe. Once subscribed to the API, it can take up to 20 minutes for the change to propagate to the gateway to allow requests, so go grab a coffee and it should be ready shortly after. 
As a reminder, this key is secret, and unique to each user. Keep it secret, and do not have it hard-coded into an application's source, and definitely don't commit it to a git repo!

#### Location
The location is specified by a latitude (1st) and longitude (2nd) in decimal degrees (ex. `45.42,-75.69`). An unlimited number of decimal places are allowed; however, the API only returns data to the closest 13 km model square, so there's no benefit after 3 digits. While the recommended way to format this field is with positive (North/ West) and negative (South/ East) degrees, results should be valid when submitting longitudes from 0 to 360, instead of -180 to 180. 

If you are looking for a place to figure out the latitude and longitude, [https://www.latlong.net/](https://www.latlong.net/) is a good starting point.

#### Time
The time field is optional for the forecast request, but mandatory for a historic request. If present, time can be specified in one of three different ways:

1. UNIX timestamp, or the number of seconds since midnight GMT on 1 Jan 1970 (this is the preferred way).
2. A datestring in the local time zone of the location being requested: `[YYYY]-[MM]-[DD]T[HH]:[MM]:[SS]`.
3. A datestring in UTC time: `[YYYY]-[MM]-[DD]T[HH]:[MM]:[SS]Z`
4. A time delta (in seconds) from the current time (ex. to get results for the previous day): `-86400`.

It's worth noting that Dark Sky also allows strings with a specified time zone (ex. `+[HH][MM]`). Right now this isn't supported, but if it's important for a workflow I can try to get it working.
If the time variable is not included, then the current time is used for the request. If a time variable is included, the request is treated as if it was requested at that time. This means that the API will return the forecast data that would have been returned then- so not quite observations, but the last forecast for that date. Results are always returned in UTC time using UNIX timestamps, and internally UNIX time is used for everything, with the exception of calculating where to begin and end the daily data. Also, for checking time format conversions, I found <https://www.silisoftware.com/tools/date.php> to be an invaluable resource.

#### Units
Specifies the requested unit for the weather conditions. Options are

* `ca`: SI, with Wind Speed and Wind Gust in kilometres per hour.
* `uk`: SI, with Wind Speed and Wind Gust in miles per hour and visibility are in miles.
* `us`: Imperial units
* `si`: SI units

For compatibility with Dark Sky, `us` (Imperial units) are the default if nothing is specified. For reference, the SI units are

* `summary`: Temperatures in degrees Celsius or accumulation in centimetres .
* `precipIntensity`: Millimetres per hour.
* `precipIntensityMax`: Millimetres per hour.
* `precipAccumulation`: Centimetres.
* `temperature`: Degrees Celsius.
* `temperatureMin`: Degrees Celsius.
* `temperatureMax`: Degrees Celsius.
* `apparentTemperature`: Degrees Celsius.
* `dewPoint`: Degrees Celsius.
* `windSpeed`: Meters per second.
* `windGust`: Meters per second.
* `pressure`: Hectopascals.
* `visibility`: Kilometres.

#### Exclude
Newly added as part of the V1.0 release, this parameter removes some of the data blocks from the reply. This can speed up the requests (especially if alerts are not needed!), and reduce the reply size. Exclude parameters can be added as a comma-separated list, with the options being:

* `currently`
* `minutely`
* `hourly`
* `daily`
* `alerts`

#### Extend
If `extend=hourly` is included, hourly data for the next 168 hours will be included, instead of the standard 48! This adds some time (~0.3s) to the response, since additional processing is required.

#### Time Zone
Finally, if `tz=precise` is included, the high precision algorithm of [TimeZoneFinder](https://timezonefinder.readthedocs.io/en/latest/) is used in place of the rapid one. This also adds some time (~0.3s), and in most cases doesn't impact the results (since everything is reported in UTC, the only thing the timezone is used for is to determine the start and end point of the day), but is added as an option if you need an accurate zone.   


### Example
```
	GET https://api.pirateweather.net/forecast/1234567890abcdefghijklmnopqrstuvwxyz/45.42,-74.30?&units=ca
	{
	  "latitude": 45.42,
	  "longitude": -75.69,
	  "timezone": "America/Toronto",
	  "offset": -5.0,
	  "elevation": 69,
	  "currently": {
		"time": 1674318840,
		"summary": "Clear",
		"icon": "clear-day",
		"nearestStormDistance": 0,
		"nearestStormBearing": 0,
		"precipIntensity": 0.0,
		"precipProbability": 0.0,
		"precipIntensityError": 0.0,
		"precipType": "none",
		"temperature": -4.59,
		"apparentTemperature": -7.82,
		"dewPoint": -6.21,
		"humidity": 0.88,
		"pressure": 1014.3,
		"windSpeed": 7.204,
		"windGust": 14.18,
		"windBearing": 255.53,
		"cloudCover": 0.14,
		"uvIndex": 2.38,
		"visibility": 14.7,
		"ozone": 402.2
	  },
	   "minutely":{
	      "summary":"Clear",
	      "icon":"clear",
	      "data":[
	         {
	            "time": 1674318840,
		    "precipIntensity": 0.0,
		    "precipProbability": 0.0,
		    "precipIntensityError": 0.0,
		    "precipType": "none"
	         },
	   ...
	      ]
	   },
	   "hourly":{
	      "summary": "Cloudy",
	      "icon": "cloudy",
	      "data": [
	         {
	            "time": 1674316800.0,
	            "icon": "partly-cloudy-day",
	            "summary": "Partly Cloudy",
	            "precipIntensity": 0.0033,
	            "precipProbability": 0.0,
	            "precipIntensityError": 0.0026,
	            "precipAccumulation": 0.0033,
	            "precipType": "snow",
	            "temperature": -5.4,
	            "apparentTemperature": -8.63,
	            "dewPoint": -7.02,
	            "humidity": 0.9,
	            "pressure": 1014.4,
	            "windSpeed": 6.88,
	            "windGust": 15.08,
	            "windBearing": 258.69,
	            "cloudCover": 0.49,
	            "uvIndex": 1.74,
	            "visibility": 14.8,
	            "ozone": 405.38
	         },
	   ...
	      ]
	   },
	   "daily": {
	      "summary": "Snow",
	      "icon": "cloudy",
	      "data": [
	         {
	            "time": 1674277200,
	            "icon": "cloudy",
	            "summary": "Cloudy",
	            "sunriseTime": 1674304502,
	            "sunsetTime": 1674338008,
	            "moonPhase": 0.9848795204636577,
	            "precipIntensity": 0.0179,
	            "precipIntensityMax": 0.0362,
	            "precipIntensityMaxTime": 1674356400,
	            "precipProbability": 0.0,
	            "precipAccumulation": 0.2861,
	            "precipType": "none",
	            "temperatureHigh": -2.59,
	            "temperatureHighTime": 1674331200,
	            "temperatureLow": -5.4,
	            "temperatureLowTime": 1674316800,
	            "apparentTemperatureHigh": -2.89,
	            "apparentTemperatureHighTime": 1674342000,
	            "apparentTemperatureLow": -8.63,
	            "apparentTemperatureLowTime": 1674316800,
	            "dewPoint": -5.6,
	            "humidity": 0.848,
	            "pressure": 1013.11,
	            "windSpeed": 5.92,
	            "windGust": 14.4,
	            "windBearing": 210.18,
	            "cloudCover": 0.768,
	            "uvIndex": 2.38,
	            "uvIndexTime": 1674320400,
	            "visibility": 15.1,
	            "temperatureMin": -5.4,
	            "temperatureMinTime": 1674316800,
	            "temperatureMax": -2.59,
	            "temperatureMaxTime": 1674331200,
	            "apparentTemperatureMin": -8.63,
	            "apparentTemperatureMinTime": 1674316800,
	            "apparentTemperatureMax": -2.89,
	            "apparentTemperatureMaxTime": 1674342000
	         },
	  ...
	   ]
	   "alerts": [
        
	   ],
	   "flags": {
	      "sources": [
	         "ETOPO1",
	         "gfs",
	         "gefs",
	         "hrrrsubh",
	         "hrrr"
	    ],
	   "sourceTimes": {
	         "hrrr_0-18": "2023-01-21 14:00:00",
	         "hrrr_subh": "2023-01-21 14:00:00",
	         "hrrr_18-48": "2023-01-21 12:00:00",
	         "gfs": "2023-01-21 06:00:00",
	         "gefs": "2023-01-21 06:00:00"
	    },
	   "nearest-station": 0,
	   "units": "ca",
	   "version": "V1.1.10"
	   }
	}
```

### Time Machine Request
In progress.
## Response
In progress.
### Data Block
In progress.

### Data Point

#### apparentTemperature
In progress.

#### apparentTemperatureMax, only on `daily`<br>
In progress.

#### apparentTemperatureMaxTime, only on `daily`<br>
In progress.

#### apparentTemperatureMin, only on `daily`<br>
In progress.

#### apparentTemperatureMinTime, only on `daily`<br>
In progress.

#### apparentTemperatureHigh, only on `daily`<br>
In progress.

#### apparentTemperatureHighTime, only on `daily`<br>
In progress.

#### apparentTemperatureLow, only on `daily`<br>
In progress.

#### apparentTemperatureLowTime, only on `daily`<br>
In progress.

#### cloudCover
Percentage of the sky that is covered in clouds. This value will be between 0 and 1 inclusive.

#### dewPoint
In progress.

#### humidity
Relative humidity expressed as a value between 0 and 1 inclusive.<br>

#### icon
One of a set of icons to provide a visual display of what's happening. This could be one of: 
`clear-day, clear-night, rain, snow, sleet, wind, fog, cloudy, partly-cloudy-day, partly-cloudy-night`.

The algorithm here is straightforward, coming from this [NOAA resource](https://weather.com/science/weather-explainers/news/common-weather-terms-used-incorrectly):

##### Hourly:

* If precipitation probability is greater than 30% and accumulation is greater than 0.25 mm, then the precipitation type.
* If visibility is less than 1 km, then `fog`.
* If winds are greater than 10 m/s, then `wind`.
* If cloud cover is greater than 75%, then `cloudy`.
* If cloud cover is greater than 37.5% and less than 75%, then `partly-cloudy-day` or `partly-cloudy-night`.
* If cloud cover is less than 37.5%, then `clear`.

##### Daily:
* If max probability is greater than 30% in any hour and total accumulation is greater than 1 mm, then precipitation type.
	* Type is based on the most common (modal) precipitation type.
* If average visibility is less than 1 km, then `fog`.
* If average wind speed is greater than 10 m/s, then `wind`.
* If average cloud cover is greater than 75%, then `cloudy`.
* If average cloud cover is greater than 37.5% and less than 75%, then `partly-cloudy-day`.
* If average cloud cover is less than 37.5%, then `clear`.

For additional details, see [issue #3](https://github.com/alexander0042/pirateweather/issues/3).

#### moonPhase, only on `daily`<br>
In progress.

#### nearestStormBearing, only on `currently`<br>
In progress.

#### nearestStormDistance, only on `currently`<br>
In progress.

#### ozone
In progress.

#### precipAccumulation, only on `hourly` and `daily`<br>
In progress.

#### precipIntensity
The rate in which liquid precipitation is falling. This value is expressed in millimeters per hour or inches per hour depending on the requested units.

#### precipIntensityMax, only on `daily`<br>
In progress.

#### precipIntensityMaxTime, only on `daily`<br>
In progress.

#### precipIntensityMin, only on `daily`<br>
In progress.

#### precipIntensityMinTime, only on `daily`<br>
In progress.

#### precipIntensityProbablity
The probablity of precipitation occuring expressed as a value between 0 and 1 inclusive.

#### precipType
The type of precipitation occuring. If `precipIntensity` is greater than zero this property will have one of the following values: `rain`, `snow` or `sleet` otherwise the value will be `none`.

#### pressure
In progress.

#### summary
In progress.

#### sunriseTime, only on `daily`<br>
In progress.

#### sunsetTime, only on `daily`<br>
In progress.

#### temperature
The air temperature in degrees celsius or degrees farenheit depending on the requested `units`

#### temperatureHigh, only on `daily`<br>
The daytime high temperature calculated between 6am and 6am local time.

#### temperatureHighTime, only on `daily`<br>
The time in which the high temperature occurs represented in UNIX time.

#### temperatureLow, only on `daily`<br>
The overnight low temperature calculated between 6am and 6am local time.

#### temperatureLowTime, only on `daily`<br>
The time in which the low temperature occurs represented in UNIX time.

#### temperatureMax, only on `daily`<br>
The maximum temperature calculated between 12am and 12am local time.

#### temperatureMaxTime, only on `daily`<br>
The time in which the maximum temperature occurs represented in UNIX time.

#### temperatureMin, only on `daily`<br>
The minimum temperature calculated between 12am and 12am local time.

#### temperatureMinTime, only on `daily`<br>
The time in which the minimum temperature occurs represented in UNIX time.

#### time
In progress.

#### unIndex
The UV index.

#### uvIndexTime, only on `daily`<br>
The time in which the maximum `uvIndex` occurs during the day.

#### visibility
The visibility in kilometres or miles depending on the requested units. In the `daily` block the visibility is the average visibility for the day. This value is capped at 16 kilometres or 10 miles depending on the requested units.

#### windBearing
In progress.

#### windGust
The wind gust in kilometres per hour or miles per hour depending on the requested units.

#### windGustTime, only on `daily`
The time in which the maximum wind gust occurs during the day represented in UNIX time.

#### windSpeed
The current wind speed in kilometres per hour or miles per hour depending on the requested units.

### Alerts
In progress.

### Flags
#### sources
The models used to generate the forecast.

#### sourceTimes
The time in UTC when the model was last updated.

#### nearest-station
The distance in miles or kilometres to the closest station used in the request.

#### units
Indicates which units were used in the forecasts.

#### version
The version of PirateWeather used to generate the forecast.
