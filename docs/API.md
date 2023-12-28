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

Also worth noting that times far in the future are not supported and will return an error. Specifically, times within 1 hour of the present time will be rounded to present to account for small timing issues, with anything beyond that returning a 400 error.

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
Added as part of the V1.0 release, this parameter removes some of the data blocks from the reply. This can speed up the requests (especially if alerts are not needed!), and reduce the reply size. Exclude parameters can be added as a comma-separated list, with the options being:

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
		"windSpeed": 7.20,
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
	            "time": 1674316800,
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
	            "moonPhase": 0.99,
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
	            "windGustTime": 1674320400,
	            "windBearing": 210.18,
	            "cloudCover": 0.77,
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
			{
				"title": "Wind Advisory issued January 24 at 9:25AM CST until January 24 at 6:00PM CST by NWS Corpus Christi TX",
				"regions": ["Live Oak", " Bee", " Goliad", " Victoria", " Jim Wells", " Inland Kleberg", " Inland Nueces", " Inland San Patricio", " Coastal Aransas", " Inland Refugio", " Inland Calhoun", " Coastal Kleberg", " Coastal Nueces", " Coastal San Patricio", " Aransas Islands", " Coastal Refugio", " Coastal Calhoun", " Kleberg Islands", " Nueces Islands", " Calhoun Islands"],
				"severity": "Moderate",
				"time": 1674573900,
				"expires": 1674604800,
				"description": "* WHAT...Southwest winds 25 to 30 mph with gusts up to 40 mph.  * WHERE...Portions of South Texas.  * WHEN...Until 6 PM CST this evening.  * IMPACTS...Gusty winds could blow around unsecured objects. Tree limbs could be blown down and a few power outages may result.",
				"uri": "https://api.weather.gov/alerts/urn:oid:2.49.0.1.840.0.492c55233ef16d7a98a3337298c828b0f358ea34.001.1"
			},
		]
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
	   "version": "V1.5.5"
	   }
	}
```

### Time Machine Request
The forecast request can be extended in several ways by adding parameters to the URL. The full set of URL options is:

```
      https://timemachine.pirateweather.net/forecast/[apikey]/[latitude],[longitude],[time]?exclude=[excluded]&units=[unit]
```

The Time Machine uses ERA5 dataset which is updated monthly but the API stores the last three days of model data and to get access to that data you query the forecast API using the time parameter like in the following URL:

```
      https://api.pirateweather.net/forecast/[apikey]/[latitude],[longitude],[time]?exclude=[excluded]&units=[unit]
```

The response format is the same as the forecast except:

* The `currently` block will refer to the requested time and not the present time.
* The `minutely` block is not present except when querying data from the last five days.
* The `hourly` block will return data from midnight of the requested day to midnight the next day.
* The `daily` block will return the data for the current day except when querying data from the last five days.
* The `alerts` block is not included.
* The `flags` block will not be included except when querying data from the last five days.

#### API Key
The API key needs to be requested from <https://pirateweather.net/>. After signing up for the service, the forecast API needs to be subscribed to, by logging in and clicking subscribe. Once subscribed to the API, it can take up to 20 minutes for the change to propagate to the gateway to allow requests, so go grab a coffee and it should be ready shortly after. 
As a reminder, this key is secret, and unique to each user. Keep it secret, and do not have it hard-coded into an application's source, and definitely don't commit it to a git repo!

#### Location
The location is specified by a latitude (1st) and longitude (2nd) in decimal degrees (ex. `45.42,-75.69`). An unlimited number of decimal places are allowed; however, the API only returns data to the closest 13 km model square, so there's no benefit after 3 digits. While the recommended way to format this field is with positive (North/ West) and negative (South/ East) degrees, results should be valid when submitting longitudes from 0 to 360, instead of -180 to 180. 

If you are looking for a place to figure out the latitude and longitude, [https://www.latlong.net/](https://www.latlong.net/) is a good starting point.

#### Time
This field is required for the time machine request and it can be specified in one of three different ways:

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
Added as part of the V1.0 release, this parameter removes some of the data blocks from the reply. This can speed up the requests (especially if alerts are not needed!), and reduce the reply size. Exclude parameters can be added as a comma-separated list, with the options being:

* `currently`
* `minutely`
* `hourly`
* `daily`
* `alerts`

## Response
```
GET https://timemachine.pirateweather.net/forecast/1234567890abcdefghijklmnopqrstuvwxyz/45.42,-74.30,1654056000?&units=ca
{
  "latitude": 45.42,
  "longitude": -74.30000000000001,
  "timezone": "America/Toronto",
  "offset": -4.0,
  "currently": {
    "time": 1654056000,
    "summary": "clear-night",
    "icon": "clear-night",
    "precipIntensity": 0.0043,
    "precipType": "none",
    "temperature": 15.23,
    "apparentTemperature": 15.47,
    "dewPoint": 7.6,
    "pressure": 1006.3,
    "windSpeed": 15.15,
    "windBearing": 72,
    "cloudCover": 0.0
  },
  "hourly": {
    "data": [
      {
        "time": 1654056000.0,
        "icon": "clear-night",
        "summary": "clear-night",
        "precipAccumulation": 0.0,
        "precipType": "none",
        "temperature": 15.23,
        "apparentTemperature": 15.47,
        "dewPoint": 7.6,
        "pressure": 1006.3,
        "windSpeed": 15.15,
        "windBearing": 72,
        "cloudCover": 0.0
      },
     ...
    ]
  },
  "daily": {
    "data": [
      {
        "time": 1654056000.0,
        "icon": "rain",
        "summary": "rain",
        "sunriseTime": 1654074748,
        "sunsetTime": 1654130288,
        "moonPhase": 0.07,
        "precipAccumulation": 0.7263,
        "precipType": "rain",
        "temperatureHigh": 16.35,
        "temperatureHighTime": 1654102800,
        "temperatureLow": 12.41,
        "temperatureLowTime": 1654092000,
        "apparentTemperatureHigh": 18.95,
        "apparentTemperatureHighTime": 1654120800,
        "apparentTemperatureLow": 12.74,
        "apparentTemperatureLowTime": 13.01,
        "dewPoint": 9.74,
        "pressure": 1002.41,
        "windSpeed": 15.19,
        "windBearing": 0,
        "cloudCover": 0.38
        "temperatureMin": 12.41,
        "temperatureMinTime": 1654092000,
        "temperatureMax": 16.35
        "temperatureMaxTime": 1654102800,
        "apparentTemperatureMin": 12.73,
        "apparentTemperatureMinTime": 13.01,
        "apparentTemperatureMax": 18.94,
        "apparentTemperatureMaxTime": 1654120800
      }
    ]
  }
}
```

### Data Block
The API returns a JSON object with the following properties

### latitude
The requested latitude.

### longitude
The requested longitude.

### timezone
Ex. `America/Toronto`. The timezone name for the requested location. This is used to determine when the `hourly` and `daily` blocks start and calculating the text summaries.

### offset
The timezone offset in hours.

### elevation
The height above sea level in meters the requested location is.

### currently
A block containing the current weather for the requested location.

### minutely
A block containing the minute-by-minute precipitation intensity for the 60 minutes.

### hourly
A block containing the hour-by-hour forecasted conditions for the next 48 hours.

### daily
A block containing the day-by-day forecasted conditions for the next 7 days.

### alerts
A block containing any severe weather alerts if any for the current location.

### flags
A block containing miscellaneous data for the API request.

### Data Point

#### apparentTemperature
"Feels like" temperature, including either humidex if the temperature is greater than 10C or wind chill if less than 10C. Humidex is calculated using:
$$
h = (0.5555)*(e - 10.0)
$$

where $e$ is the vapor pressure in hPa, given by:
$$
e = 6.11 * exp[5417.7530 * ( (1/273.15) - (1/dewpoint) )]
$$
from: <https://en.wikipedia.org/wiki/Humidex>. Wind chill is calculated using the Environment Canada Model from <https://en.wikipedia.org/wiki/Wind_chill>:
$$
13.12 + 0.6215T – 11.37 (V^{0.16}) + 0.3965T (V^{0.16})
$$
where $T$ is the temperature in Celsius and $V$ is the Wind velocity in kilometres per hour. 

#### apparentTemperatureMax
**Only on `daily`**. The maximum "feels like" temperature during a day, from midnight to midnight. Note that this value is always forward looking, so for day 0 (the current day), it will return the highest value of the remaining hours in the day.

#### apparentTemperatureMaxTime
**Only on `daily`**. The time (in UTC) that the maximum "feels like" temperature occurs during a day, from 12:00 am and 11:59 pm. Note that this value is always forward looking, so for day 0 (the current day), it will return the highest value of the remaining hours in the day.

#### apparentTemperatureMin
**Only on `daily`**. The minimum "feels like" temperature during a day, from from 12:00 am and 11:59 pm. Note that this value is always forward looking, so for day 0 (the current day), it will return the highest value of the remaining hours in the day.

#### apparentTemperatureMinTime
**Only on `daily`**. The time (in UTC) that the minimum "feels like" temperature occurs during a day, from from 12:00 am and 11:59 pm. Note that this value is always forward looking, so for day 0 (the current day), it will return the highest value of the remaining hours in the day.

#### apparentTemperatureHigh
**Only on `daily`**. The maximum "feels like" temperature during the daytime, from 6:00 am to 6:00 pm. Note that this value is always forward looking, so for day 0 (the current day), it will return the highest value of the remaining hours in the day. If the forecast start time is after 6:00 pm, it will return the current temperature. 

#### apparentTemperatureHighTime
**Only on `daily`**. The time of the maximum "feels like" temperature during the daytime, from 6:00 am to 6:00 pm. Note that this value is always forward looking, so for day 0 (the current day), it will return the time of the highest value of the remaining hours in the day. If the forecast start time is after 6:00 pm, it will return the current time. 

#### apparentTemperatureLow
**Only on `daily`**. The minimum "feels like" temperature during the daytime, from 6:00 am to 6:00 pm. Note that this value is always forward looking, so for day 0 (the current day), it will return the lowest value of the remaining hours in the day. If the forecast start time is after 6:00 pm, it will return the current temperature. 

#### apparentTemperatureLowTime
**Only on `daily`**. 
The time of the minimum "feels like" temperature during the daytime, from 6:00 am to 6:00 pm. Note that this value is always forward looking, so for day 0 (the current day), it will return the time of the lowest value of the remaining hours in the day. If the forecast start time is after 6:00 pm, it will return the current time. 

#### cloudCover
Percentage of the sky that is covered in clouds. This value will be between 0 and 1 inclusive. Calculated from the the [GFS (#650)](https://www.nco.ncep.noaa.gov/pmb/products/gfs/gfs.t00z.pgrb2.1p00.f003.shtml) or [HRRR (#115)](https://rapidrefresh.noaa.gov/hrrr/HRRRv4_GRIB2_WRFTWO.txt) `TCDC` variable for the entire atmosphere.

#### dewPoint
The point in which the air temperature needs (assuming constant pressure) in order to reach a relative humidity of 100%. This is value is represented in degrees Celsius or Fahrenheit depending on the requested `units`. [See this resource for more information.](https://www.weather.gov/arx/why_dewpoint_vs_humidity)

#### humidity
Relative humidity expressed as a value between 0 and 1 inclusive. This is a percentage of the actual water vapor in the air compared to the total amount of water vapor that can exist at the current temperature. [See this resource for more information.](https://www.sciencedirect.com/topics/agricultural-and-biological-sciences/relative-humidity)

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

#### moonPhase
**Only on `daily`**. The fractional [lunation number](https://en.wikipedia.org/wiki/New_moon#Lunation_number) for the given day. `0.00` represents a new moon, `0.25` represents the first quarter, `0.50` represents a full moon and `0.75` represents the last quarter.

#### nearestStormBearing
**Only on `currently`**. The approximate direction in degrees in which a storm is travelling with 0° representing true north.

#### nearestStormDistance
**Only on `currently`**. The approximate distance to the nearest storm in kilometers or miles depending on the requested `units`.

#### ozone
The density of total atmospheric ozone at a given time in Dobson units.

#### precipAccumulation
**Only on `hourly` and `daily`**. The amount of liquid precipitation expected to fall over an hour or a day expressed in centimetres or inches depending on the requested `units`. 

#### precipIntensity
The rate in which liquid precipitation is falling. This value is expressed in millimeters per hour or inches per hour depending on the requested `units`. For `currently` and `minutely` forecast blocks, the HRRR "Precipitation Rate" variable  is used where available, otherwise averaged GEFS data is returned. For `hourly` and `daily` forecast blocks, GEFS is always used. This is done so that the `precipIntensityProbablity` variable is aligned with the intensity.

#### precipIntensityError
The standard deviation of the `precipitationIntensity`.

#### precipIntensityMax
**Only on `daily`**. The maximum value of `precipitationIntensity` for the given day.

#### precipIntensityMaxTime
**Only on `daily`**. The point in which the maximum `precipitationIntensity` occurs represented in UNIX time.

#### precipIntensityMin
**Only on `daily`**. The minimum value of `precipitationIntensity` for the given day.

#### precipIntensityMinTime
**Only on `daily`**. The point in which the minimum `precipitationIntensity` occurs represented in UNIX time.

#### precipProbability
The probability of precipitation occurring expressed as a decimal between 0 and 1 inclusive.

#### precipType
The type of precipitation occurring. If `precipIntensity` is greater than zero this property will have one of the following values: `rain`, `snow` or `sleet` otherwise the value will be `none`. `sleet` is defined as any precipitation which is neither rain nor snow.

#### pressure
The sea-level pressure represented in hectopascals or millibars depending on the requested `units`.

#### summary
A human-readable summary describing the weather conditions for a given data point.

#### sunriseTime
**Only on `daily`**. The time when the sun rises for a given day represented in UNIX time.

#### sunsetTime
**Only on `daily`**. The time when the sun sets for a given day represented in UNIX time.

#### temperature
The air temperature in degrees Celsius or degrees Fahrenheit depending on the requested `units`

#### temperatureHigh
**Only on `daily`**. The daytime high temperature calculated between 6:00 am and 6:00 pm local time. Note that this value is always forward looking, so for day 0 (the current day), it will return the highest value of the remaining hours in the day.

#### temperatureHighTime
**Only on `daily`**. The time in which the high temperature occurs represented in UNIX time.

#### temperatureLow
**Only on `daily`**. The overnight low temperature calculated between 6:00 pm and 6:00 am local time. Note that this value is always forward looking, so for day 0 (the current day), it will return the highest value of the remaining hours in the day.

#### temperatureLowTime
**Only on `daily`**. The time in which the low temperature occurs represented in UNIX time.

#### temperatureMax
**Only on `daily`**. The maximum temperature calculated between 12:00 am and 11:59 pm local time. Note that this value is always forward looking, so for day 0 (the current day), it will return the highest value of the remaining hours in the day.

#### temperatureMaxTime
**Only on `daily`**. The time in which the maximum temperature occurs represented in UNIX time.

#### temperatureMin
**Only on `daily`**. The minimum temperature calculated between 12:00 am and 11:59 pm local time. Note that this value is always forward looking, so for day 0 (the current day), it will return the highest value of the remaining hours in the day.

#### temperatureMinTime
**Only on `daily`**. The time in which the minimum temperature occurs represented in UNIX time.

#### time
The time in which the data point begins represented in UNIX time. The `currently` block represents the current time, the `minutely` block is aligned to the top of the minute, the `hourly` block the top of the hour and the `daily` block to midnight of the current day in the current time zone.

#### uvIndex
The measure of UV radiation as represented as an index starting from 0. `0` to `2` is Low, `3` to `5` is Moderate, `6` and `7` is High, `8` to `10` is Very High and `11+` is considered extreme. [See this resource for more information.](https://www.who.int/news-room/questions-and-answers/item/radiation-the-ultraviolet-(uv)-index#:~:text=What%20is%20the%20UV%20index,takes%20for%20harm%20to%20occur.)

#### uvIndexTime
**Only on `daily`**. The time in which the maximum `uvIndex` occurs during the day.

#### visibility
The visibility in kilometres or miles depending on the requested units. In the `daily` block the visibility is the average visibility for the day. This value is capped at 16 kilometres or 10 miles depending on the requested `units`.

#### windBearing
The direction in which the wind is blowing in degrees with 0° representing true north. To convert degrees to a cardinal direction you can refer [to this table](http://snowfence.umn.edu/Components/winddirectionanddegrees.htm).

#### windGust
The wind gust in kilometres per hour or miles per hour depending on the requested `units`.

#### windGustTime
**Only on `daily`**. The time in which the maximum wind gust occurs during the day represented in UNIX time.

#### windSpeed
The current wind speed in kilometres per hour or miles per hour depending on the requested `units`.

### Alerts
#### title
A brief description of the alert.

#### regions
An array of strings containing all regions included in the weather alert.

#### severity
Indicates how severe the weather alert is. Possible values are:

* Extreme - Extraordinary threat to life or property
* Severe - Significant threat to life or property
* Moderate - Possible threat to life or property
* Minor - Minimal threat to life or property
* Unknown

#### time
The time in which the alert was issued represented in UNIX time.

#### expires
The time in which the alert expires represented in UNIX time.

#### description
A detailed description of the alert.

#### uri
A HTTP(S) url in which you can visit for more information about the alert.

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
