# API Docs
This page serves as the documentation for the Pirate Weather API call and response format. Since this service is designed to be a drop in replacement for the [Dark Sky API](https://web.archive.org/web/20200723173936/https://darksky.net/dev/docs), the goal is to match that as closely as possible, and any disagreement between their service and Pirate Weather will be treated as a bug. However, as Pirate Weather continues to evolve, I plan on adding small, non-breaking additions where I can, and they will be documented here! Plus, always better to have my own (open source and editable) version of the docs!

<!-- An alpha [Swagger UI](https://github.com/swagger-api/swagger-ui) for the API is also available at <https://api.pirateweather.net/docs>. -->

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
https://api.pirateweather.net/forecast/[apikey]/[latitude],[longitude],[time]?exclude=[excluded]&units=[unit]&extend=[hourly]&version=[2]&lang=[lang]
``` 

#### API Key
The API key needs to be requested from <https://pirateweather.net/>. After signing up for the service, the forecast API needs to be subscribed to, by logging in and clicking subscribe. Once subscribed to the API, it can take up to 20 minutes for the change to propagate to the gateway to allow requests, so go grab a coffee and it should be ready shortly after. 
As a reminder, this key is secret, and unique to each user. Keep it secret, and do not have it hard-coded into an application's source, and definitely don't commit it to a git repo!

Alternatively, you can also add the API key to the request headers by using the `apikey` header. You will still need to add a dummy API key to the URL so it would look like the following:

```
https://api.pirateweather.net/forecast/{anythingAtAll}/{lat},{lon}
```

#### Location
The location is specified by a latitude (1st) and longitude (2nd) in decimal degrees (ex. `45.42,-75.69`). An unlimited number of decimal places are allowed; however, the API only returns data to the closest 13 km model square, so there's no benefit after 3 digits. While the recommended way to format this field is with positive (North/East) and negative (South/West) degrees, results should be valid when submitting longitudes from 0 to 360, instead of -180 to 180. 

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

For compatibility with Dark Sky, `us` (Imperial units) are the default if nothing is specified.

| Units | si | ca | uk | us |
|---|---|---|---|---|
| summary | Temperatures in degrees Celsius or accumulation in centimetres | Temperatures in degrees Celsius or accumulation in centimetres | Temperatures in degrees Celsius or accumulation in centimetres | Temperatures in degrees Fahrenheit or accumulation in inches |
| precipIntensity | Millimetres per hour | Millimetres per hour | Millimetres per hour | Inches per hour |
| precipIntensityMax | Millimetres per hour | Millimetres per hour | Millimetres per hour | Inches per hour |
| precipAccumulation | Centimetres | Centimetres | Centimetres | Inches |
| liquidAccumulation   | Centimetres | Centimetres | Centimetres | Inches |
| snowAccumulation | Centimetres | Centimetres | Centimetres | Inches |
| iceAccumulation | Centimetres | Centimetres | Centimetres | Inches |
| temperature | Degrees Celsius | Degrees Celsius | Degrees Celsius | Degrees Fahrenheit |
| temperatureMin | Degrees Celsius | Degrees Celsius | Degrees Celsius | Degrees Fahrenheit |
| temperatureMax | Degrees Celsius | Degrees Celsius | Degrees Celsius | Degrees Fahrenheit |
| apparentTemperature | Degrees Celsius | Degrees Celsius | Degrees Celsius | Degrees Fahrenheit |
| dewPoint | Degrees Celsius | Degrees Celsius | Degrees Celsius | Degrees Fahrenheit |
| windSpeed | Meters per second | Kilometres per hour | Miles per hour | Miles per hour |
| windGust | Meters per second | Kilometres per hour | Miles per hour | Miles per hour |
| pressure | Hectopascals | Hectopascals | Hectopascals | Millibars |
| visibility | Kilometres | Kilometres | Kilometres | Miles |

#### Exclude
Added as part of the V1.0 release, this parameter removes some of the data blocks from the reply. This can speed up the requests (especially if alerts are not needed!), and reduce the reply size. Exclude parameters can be added as a comma-separated list, with the options being:

* `currently`
* `minutely`
* `hourly`
* `daily`
* `alerts`
* `summary` - Allows you to get the summaries in the old format before the translations module was added.

Some models can also be excluded, which will force data from the fallback sources to be used:

*  `hrrr`
*  `nbm`

#### Extend
If `extend=hourly` is included, hourly data for the next 168 hours will be included, instead of the standard 48! This adds some time (~0.3s) to the response, since additional processing is required.   

#### Version
If `version=2` is included fields which were not part of the Dark Sky API will be included. These fields are `smoke`, `smokeMax`, `smokeMaxTime`, `fireIndex`, `fireIndexMax`, `fireIndexMaxTime`, `liquidAccumulation`, `snowAccumulation`, `iceAccumulation`, `dawnTime`, `duskTime`, `currentDayIce`, `currentDayLiquid` and `currentDaySnow`. It also includes `nearestStormDistance` and `nearestStormBearing` to each of the hourly blocks and `sourceIDX` where you can see the X/Y and lat/long coordinate for each returned model.

#### Language
Added as part of the V2.5 release, this parameter allows you to sepecify what language the text summaries use. The possible values for language may be:

??? note "Language"

	* `ar`: Arabic
	* `az`: Azerbaijani
	* `be`: Belarusian
	* `bg`: Bulgarian
	* `bn`: Bengali
	* `bs`: Bosnian
	* `ca`: Catalan
	* `cs`: Czech
	* `cy`: Welsh
	* `da`: Danish
	* `de`: German
	* `el`: Greek
	* `en`: English (which is the default)
	* `eo`: Esperanto
	* `es`: Spanish
	* `et`: Estonian
	* `fa`: Persian
	* `fi`: Finnish
	* `fr`: French
	* `ga`: Irish
	* `gd`: Gaelic
	* `he`: Hebrew
	* `hi`: Hindi
	* `hr`: Croatian
	* `hu`: Hungarian
	* `id`: Indonesian
	* `is`: Icelandic
	* `it`: Italian
	* `ja`: Japanese
	* `ka`: Georgian
	* `kn`: Kannada
	* `ko`: Korean
	* `kw`: Cornish
	* `lv`: Latvian
	* `ml`: Malayam
	* `mr`: Marathi
	* `nl`: Dutch
	* `no`: Norwegian Bokmål
	* `pa`: Punjabi
	* `pl`: Polish
	* `pt`: Portuguese
	* `ro`: Romanian
	* `ru`: Russian
	* `sk`: Slovak
	* `sl`: Slovenian
	* `sr`: Serbian
	* `sv`: Swedish
	* `ta`: Tamil
	* `te`: Telugu
	* `tet: Tetum
	* `tr`: Turkish
	* `uk`: Ukrainian
	* `ur`: Urdu
	* `vi`: Vietnamese
	* `x-pig-latin`: Igpay Atinlay
	* `zh`: simplified Chinese
	* `zh-tw`: traditional Chinese

If you require a language not listed above, please consider contributing to the [API translation module](https://github.com/Pirate-Weather/translations).

#### Icon
If you add `icon=pirate` to the list of parameters you can get an expanded icon set with icons that were not available in the Dark Sky API.

### API Response Example
```
	GET https://api.pirateweather.net/forecast/1234567890abcdefghijklmnopqrstuvwxyz/45.42,-74.30?&units=ca
	"latitude": 45.42,
	"longitude": -74.3,
	"timezone": "America/Toronto",
	"offset": -4,
	"elevation": 77,
	"currently": {
		"time": 1749319080,
		"summary": "Mostly Clear",
		"icon": "clear-day",
		"nearestStormDistance": 19.51,
		"nearestStormBearing": 270,
		"precipIntensity": 0,
		"precipProbability": 0,
		"precipIntensityError": 0.16,
		"precipType": "none",
		"temperature": 23.28,
		"apparentTemperature": 21.64,
		"dewPoint": 11.48,
		"humidity": 0.52,
		"pressure": 1009.92,
		"windSpeed": 13.05,
		"windGust": 17.5,
		"windBearing": 30,
		"cloudCover": 0.26,
		"uvIndex": 5.48,
		"visibility": 16.09,
		"ozone": 361.16
	},
	"minutely": {
		"summary": "Mostly clear for the hour.",
		"icon": "clear-day",
		"data": [
		{
			"time": 1749319080,
			"precipIntensity": 0,
			"precipProbability": 0,
			"precipIntensityError": 0.16,
			"precipType": "none"
		},
	   ...
	  ]
	},
	"hourly": {
		"summary": "Mostly clear until tomorrow morning.",
		"icon": "clear-day",
		"data": [
			{
				"time": 1749315600,
				"summary": "Mostly Clear",
				"icon": "clear-day",
				"precipIntensity": 0,
				"precipProbability": 0,
				"precipIntensityError": 0.116,
				"precipAccumulation": 0,
				"precipType": "rain",
				"temperature": 23.73,
				"apparentTemperature": 22.68,
				"dewPoint": 12.1,
				"humidity": 0.48,
				"pressure": 1009.92,
				"windSpeed": 8.64,
				"windGust": 15.84,
				"windBearing": 30,
				"cloudCover": 0.32,
				"uvIndex": 6.99,
				"visibility": 16.09,
				"ozone": 356.59
			},
	    	...
		]
	},
	"daily": {
	"summary": "Light rain on Monday and Tuesday, with high temperatures falling to 21°C next Saturday.",
	"icon": "rain",
	"data": [
		{
			"time": 1749268800,
			"summary": "Mostly clear starting in the afternoon.",
			"icon": "clear-day",
			"sunriseTime": 1749287384,
			"sunsetTime": 1749343376,
			"moonPhase": 0.38,
			"precipIntensity": 0,
			"precipIntensityMax": 0,
			"precipIntensityMaxTime": 1749268800,
			"precipProbability": 0,
			"precipAccumulation": 0,
			"precipType": "rain",
			"temperatureHigh": 24.73,
			"temperatureHighTime": 1749326400,
			"temperatureLow": 12.41,
			"temperatureLowTime": 1749373200,
			"apparentTemperatureHigh": 23.1,
			"apparentTemperatureHighTime": 1749326400,
			"apparentTemperatureLow": 10,
			"apparentTemperatureLowTime": 1749373200,
			"dewPoint": 11.8,
			"humidity": 0.6,
			"pressure": 1009.94,
			"windSpeed": 6.22,
			"windGust": 11.68,
			"windGustTime": 1749322800,
			"windBearing": 134,
			"cloudCover": 0.52,
			"uvIndex": 6.99,
			"uvIndexTime": 1749315600,
			"visibility": 13.15,
			"temperatureMin": 16.35,
			"temperatureMinTime": 1749283200,
			"temperatureMax": 24.73,
			"temperatureMaxTime": 1749326400,
			"apparentTemperatureMin": 15.77,
			"apparentTemperatureMinTime": 1749351600,
			"apparentTemperatureMax": 23.1,
			"apparentTemperatureMaxTime": 1749326400
		},
	    ...
	  ]
	}
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
			"hrrrsubh",
			"hrrr_0-18",
			"nbm",
			"nbm_fire",
			"hrrr_18-48",
			"gefs"
		],
		"sourceTimes": {
			""hrrr_subh": "2025-06-07 16Z",
			"hrrr_0-18": "2025-06-07 15Z",
			"nbm": "2025-06-07 15Z",
			"nbm_fire": "2025-06-07 12Z",
			"hrrr_18-48": "2025-06-07 12Z",
			"gfs": "2025-06-07 12Z",
			"gefs": "2025-06-07 00Z"
		},
		"nearest-station": 0,
		"units": "ca",
		"version": "V2.7.7"
  	}
```

### Time Machine Request
The Time Machine uses either archived 1-hour model results (past four months) or the [NCAR AWS ERA5 dataset](https://registry.opendata.aws/nsf-ncar-era5/) which is updated monthly and is approximately three to four months behind realtime. The forecast request can be extended in several ways by adding parameters to the URL. The full set of URL options is:

```
      https://timemachine.pirateweather.net/forecast/[apikey]/[latitude],[longitude],[time]?exclude=[excluded]&units=[unit]
```

Crucially, there's now three different ways a request could be handled:

1. Pre 3 or 4 months behind realtime: ERA5 data via the NCAR S3 archive.
	* 24 hours
	* Subset of variables
	* Slowish (~10 seconds)
2. 3 or 4 months behind realtime, to T-minus 24 hours: GFS/HRRR/NBM 1-hour forecast data from the PW archive
	* Provides more data and resolution than is available on ERA5
	* Can provide the range of PW forecast variables via the `tmextra` parameter
	* Avoids the ERA5 production time lag
	* Slow (~30 seconds), since it needs to open and read many zarr files on S3
3. T-minus 24 hours onward: merged 1-hour forecast data with foreward looking forecast data, responding with the full 7 day forecast.
	* Same process as before!
	* Very fast (10 ms), since this is optimized for fast reads in one location

The response format is the same as the forecast except:

* The `currently` block will refer to the requested time and not the present time.
* The `minutely` block is not present except when querying data from the last 24h.
* The `hourly` block will return data from midnight of the requested day to midnight the next day.
* The `daily` block will return the data for the current day except when querying data from the last 24h.
* The `alerts` block is not included.
* The `flags` block will show the sources used in the request, the requested `units` and the API version.

When requesting data from the PW archive (3-4 months trailing), the optional `tmextra` query parameter controls which variables are returned. When it is included, same variables that are present in a forecast request (except alerts) are returned. When it is not included (by default), the same range of parameters returned by ERA5 requests is included.

## Response
```
GET https://timemachine.pirateweather.net/forecast/1234567890abcdefghijklmnopqrstuvwxyz/45.42,-74.30,1654056000?&units=ca
{
  "latitude": 45.42,
  "longitude": -74.3,
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
	"windGust": 17.15,
    "windBearing": 72,
    "cloudCover": 0.0
  },
  "hourly": {
    "data": [
      {
        "time": 1654056000,
        "icon": "clear-night",
        "summary": "clear-night",
        "precipAccumulation": 0.0,
        "precipType": "none",
        "temperature": 15.23,
        "apparentTemperature": 15.47,
        "dewPoint": 7.6,
        "pressure": 1006.3,
        "windSpeed": 15.15,
		"windGust": 17.15,
        "windBearing": 72,
        "cloudCover": 0.0,
		"snowAccumulation": 0.0
      },
     ...
    ]
  },
  "daily": {
    "data": [
      {
        "time": 1654056000,
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
		"windGust": 16,
		"windGustTime": 1654092000,
        "windBearing": 0,
        "cloudCover": 0.38
        "temperatureMin": 12.41,
        "temperatureMinTime": 1654092000,
        "temperatureMax": 16.35
        "temperatureMaxTime": 1654102800,
        "apparentTemperatureMin": 12.73,
        "apparentTemperatureMinTime": 13.01,
        "apparentTemperatureMax": 18.94,
        "apparentTemperatureMaxTime": 1654120800,
		"snowAccumulation":0.0
      }
    ]
  },
  "flags": {
	"sources":"ERA5",
	"nearest-station":0,
	"units":"us",
	"version":"V2.7.7",
	"sourceIDX":[
		"x":1120,
		"y":216
		],
	"processTime":408339
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
A block containing the hour-by-hour forecasted conditions for the next 48 hours. If `extend=hourly` is used then the hourly block gives hour-by-hour forecasted conditions for the next 168 hours.

### daily
A block containing the day-by-day forecasted conditions for the next 7 days.

### alerts
A block containing any severe weather alerts if any for the current location.

### flags
A block containing miscellaneous data for the API request.

### Data Point

#### apparentTemperature
Temperature adjusted for wind and humidity, based the [Steadman 1994](http://www.bom.gov.au/jshess/docs/1994/steadman.pdf) approach used by the Australian Bureau of Meteorology. Implemented using the [Breezy Weather approach](https://github.com/breezy-weather/breezy-weather/discussions/1085#discussioncomment-9734935) without solar radiation, which follows this equation:

$$ AT = Ta + 0.33 × rh / 100 × 6.105 × exp(17.27 × Ta / (237.7 + Ta)) − 0.70 × ws − 4.00$$

- $Ta$ is the ambient temperature in °C
- $ws$ is the wind speed in m/s

This equation produces results that are similar to heat index and wind chill values; however, may vary from other sources that incorporate solar radiation to produce higher apparent temperatures.

#### apparentTemperatureMax
**Only on `daily`**. The maximum "feels like" temperature during a day, from midnight to midnight.

#### apparentTemperatureMaxTime
**Only on `daily`**. The time (in UTC) that the maximum "feels like" temperature occurs during a day, from 12:00 am and 11:59 pm.

#### apparentTemperatureMin
**Only on `daily`**. The minimum "feels like" temperature during a day, from from 12:00 am and 11:59 pm.

#### apparentTemperatureMinTime
**Only on `daily`**. The time (in UTC) that the minimum "feels like" temperature occurs during a day, from from 12:00 am and 11:59 pm.

#### apparentTemperatureHigh
**Only on `daily`**. The maximum "feels like" temperature during the daytime, from 6:00 am to 6:00 pm.

#### apparentTemperatureHighTime
**Only on `daily`**. The time of the maximum "feels like" temperature during the daytime, from 6:00 am to 6:00 pm.

#### apparentTemperatureLow
**Only on `daily`**. The minimum "feels like" temperature during the daytime, from 6:00 am to 6:00 pm.

#### apparentTemperatureLowTime
**Only on `daily`**. 
The time of the minimum "feels like" temperature during the daytime, from 6:00 am to 6:00 pm.

#### cloudCover
Percentage of the sky that is covered in clouds. This value will be between 0 and 1 inclusive. Calculated from the the [GFS (#650)](https://www.nco.ncep.noaa.gov/pmb/products/gfs/gfs.t00z.pgrb2.1p00.f003.shtml) or [HRRR (#115)](https://rapidrefresh.noaa.gov/hrrr/HRRRv4_GRIB2_WRFTWO.txt) `TCDC` variable for the entire atmosphere.

#### currentDayIce
**Only on `currently`**. The ice precipitation that has accumulated so far during the day, from midnight until the forecast request time.

#### currentDayLiquid
**Only on `currently`**. The liquid precipitation that has accumulated so far during the day, from midnight until the forecast request time.

#### currentDaySnow
**Only on `currently`**. The snow precipitation that has accumulated so far during the day, from midnight until the forecast request time.

#### dawnTime
**Only on `daily`**. The time when the the sun is a specific (6 degrees) height above the horizon after sunrise. Calculated from [Astal dawn defaults](https://astral.readthedocs.io/en/latest/package.html?highlight=dawn#astral.sun.dawn).

#### dewPoint
The point in which the air temperature needs (assuming constant pressure) in order to reach a relative humidity of 100%. This is value is represented in degrees Celsius or Fahrenheit depending on the requested `units`. [See this resource for more information.](https://www.weather.gov/arx/why_dewpoint_vs_humidity)

#### duskTime
**Only on `daily`**. The time when the the sun is a specific (6 degrees) height above the horizon before sunset. Calculated from [Astal dusk defaults](https://astral.readthedocs.io/en/latest/package.html?highlight=dusk#astral.sun.dusk).

#### feelsLike
The apparent temperature from the GFS or NBM models.

#### fireIndex
**Only on `currently` and `hourly`.** **Only available for the US and parts of Canada. Outside of these locations this will return -999.** The [Fosburg fire index](https://www.spc.noaa.gov/exper/firecomp/INFO/fosbinfo.html). Notably, this 0-100 index deals only with conditions, not fuels, and so a high index area is not necessarily high risk for fires.

#### fireIndexMax
**Only on `daily`.** The maximum `fireIndex` for the given day.

#### fireIndexMaxTime
**Only on `daily`.** the time in which the maximum `fireIndex` occurs represented in UNIX time.

#### humidity
Relative humidity expressed as a value between 0 and 1 inclusive. This is a percentage of the actual water vapour in the air compared to the total amount of water vapour that can exist at the current temperature. [See this resource for more information.](https://www.sciencedirect.com/topics/agricultural-and-biological-sciences/relative-humidity)

#### iceAccumulation
**Only on `hourly` and `daily`**. The amount of ice precipitation expected to fall over an hour or a day expressed in centimetres or inches depending on the requested `units`. 

#### icon
One of a set of icons to provide a visual display of what's happening. This could be one of: 
`clear-day, clear-night, rain, snow, sleet, wind, fog, cloudy, partly-cloudy-day and partly-cloudy-night` and may include `thunderstorm`, `hail` or `mixed` in the future. In some rare cases the API may return `none` as an icon which could be defined as Not Available.

If `icon=pirate` is added as a query string parameter the icon set is expanded to include:

* `mostly-clear-day`
* `mostly-clear-night`
* `mostly-cloudy-day`
* `mostly-cloudy-night`
* `possible-rain-day`
* `possible-rain-night`
* `possible-snow-day`
* `possible-snow-night`
* `possible-sleet-day`
* `possible-sleet-night`
* `possible-precipitation-day`
* `possible-precipitation-night`
* `precipitation`
* `drizzle`
* `light-rain`
* `heavy-rain`
* `flurries`
* `light-snow`
* `heavy-snow`
* `very-light-sleet`
* `light-sleet`
* `heavy-sleet`
* `breezy`
* `dangerous-wind`
* `mist`
* `haze`
* `smoke`

Note that `smoke` and `haze` may be moved to the default icon set in the future, at which point they will be removed from this expanded list.

The daily icon is calculated between 4:00 am and 4:00 am local time. The algorithm here is straightforward, coming from this [NOAA resource](https://weather.com/science/weather-explainers/news/common-weather-terms-used-incorrectly):

##### Currently:

* If precipitation accumulation is greater than 0.02 mm, then the precipitation type.
* If visibility is less than 10 km, then `fog`.
* If winds are greater than 6.7056 m/s, then `wind`.
* If cloud cover is greater than 87.5%, then `cloudy`.
* If cloud cover is greater than 37.5% and less than 87.5%, then `partly-cloudy-day` or `partly-cloudy-night`.
* If cloud cover is less than 37.5%, then `clear`.
  
##### Hourly:

* If precipitation probability is greater than 25% and accumulation is greater than 0.02 mm, then the precipitation type.
* If visibility is less than 10 km, then `fog`.
* If winds are greater than 6.7056 m/s, then `wind`.
* If cloud cover is greater than 87.5%, then `cloudy`.
* If cloud cover is greater than 37.5% and less than 87.5%, then `partly-cloudy-day` or `partly-cloudy-night`.
* If cloud cover is less than 37.5%, then `clear`.

##### Daily:

With the daily summaries being introduced in version 2.7 the day icon now considers the day as a whole rather than using daily averages. The icon shown will generally be whichever condition comes first so if the morning is foggy and the evening is windy the fog icon will be shown. The cloud cover icons will only be shown as long as no other conditions are forecasted for the day.

**Precipitaion**

The precipitation icon logic is as follows:

* If max probability is greater than 25% in any hour
* The total accumulation depends on the number of periods has precipitation forecasted
	* Total precipitation needs to be 0.25 mm for one period
	* Total precipitation needs to be 0.50 mm for two periods
	* Total precipitation needs to be 0.75 mm for three periods
	* Total precipitation needs to be 1 mm for four periods

The precipitation with the most accumulation forecasted is generally the icon which is shown unless:

* If more than 10 mm of rain is forecast, then `rain`
* If more than 5 mm of snow is forecast, then `snow`
* Else, if more than 1 mm of ice is forecast, then `sleet`

**Fog and Wind**

The fog and wind icons are shown if at least one period has at least half of its hours (or three or more hours for longer periods) as foggy or windy and there is no precipitation then the icon is shown.

* If visibility is less than 10 km then `fog`.
* If wind speed is greater than 6.7056 m/s, then `wind`.

**Cloud Cover**

The average cloud cover is calculated for each period and the most common level (clear, mostly clear, partly cloudy, mostly cloudy or overcast) is chosen as the icon. The exception is if all of the periods have a different level. In this case the following logic is used:

* If the maximum cloud cover occurs in the last period then use the lowest cloud cover level
* Otherwise use the maximum cloud cover level for the day

The cloud cover icon thresholds are the following:

* If cloud cover is greater than 87.5%, then `cloudy`.
* If cloud cover is greater than 37.5% and less than 87.5%, then `partly-cloudy-day`.
* If cloud cover is less than 37.5%, then `clear`.

For additional details, see [issue #3](https://github.com/alexander0042/pirateweather/issues/3).

#### liquidAccumulation
**Only on `hourly` and `daily`**. The amount of liquid precipitation expected to fall over an hour or a day expressed in centimetres or inches depending on the requested `units`. 

#### moonPhase
**Only on `daily`**. The fractional [lunation number](https://en.wikipedia.org/wiki/New_moon#Lunation_number) for the given day. `0.00` represents a new moon, `0.25` represents the first quarter, `0.50` represents a full moon and `0.75` represents the last quarter.

#### nearestStormBearing
The approximate direction in degrees in which a storm is travelling with 0° representing true north. Calculated with the excellent [XArray-Spatial](https://github.com/makepath/xarray-spatial) package using a 0.2 mm/h water equivalent (so 2 mm/h of snow or 0.2 mm/h of rain) threshold for a storm. 

#### nearestStormDistance
The approximate distance to the nearest storm in kilometers or miles depending on the requested `units`. Calculated with the excellent [XArray-Spatial](https://github.com/makepath/xarray-spatial) package using a 0.2 mm/h water equivalent (so 2 mm/h of snow or 0.2 mm/h of rain) threshold for a storm. Note that the distance is calculated from the midpoint of a GFS model cell to the midpoint of a model cell with a "storm".  

#### ozone
**Only on `currently` and `hourly`**. The density of total atmospheric ozone at a given time in Dobson units.

#### precipAccumulation
**Only on `hourly` and `daily`**. The total amount of precipitation expected to fall over an hour or a day expressed in centimetres or inches depending on the requested `units`. For day 0, this is the precipitation during the remaining hours of the day.
A 1:10 snowfall ratio is used and already factored into this parameter:

  * 5 cm (50 mm) of snow is forecasted for an hour, `precipAccumulation`, in cm, will return 5.
  * 5 mm of rain is forecasted for an hour, `precipAccumulation`, in cm, will return 0.5.
  * 5 mm of rain and 5 cm of snow is forecasted for an hour, `precipAccumulation`, in cm, will return 5.5. This illustrates the value of using the `liquidAccumulation`, `snowAccumulation`, and `iceAccumulation` parameters instead of `precipAccumulation`.

#### precipIntensity
Precipitation intensity units have been revised to reflect the Dark Sky style. This means that intensity is always reported in **liquid water equivalent**, and this should be reflected when displaying the data.

  * So if 5 cm (50 mm) of snow is forecasted for an hour, `precipIntensity`, in mm, will return 5, as 5 mm of rain provides 50 mm of snow.
    * If 5 mm of rain is forecasted for an hour, `precipIntensity`, in mm, will return 5, for 5 mm of rain.
  * See [this thread for details](https://github.com/Pirate-Weather/pirate-weather-code/pull/53#issuecomment-2661603131).
  * In the future, `snowIntensity`, `sleetIntensity`, and `rainIntensity` will be added to clarify this.

#### precipIntensityError
The standard deviation of the `precipIntensity` from the GEFS model.

#### precipIntensityMax
**Only on `daily`**. The maximum value of `precipIntensity` for the given day.

#### precipIntensityMaxTime
**Only on `daily`**. The point in which the maximum `precipIntensity` occurs represented in UNIX time.

#### precipIntensityMin
**Only on `daily`**. The minimum value of `precipIntensity` for the given day.

#### precipIntensityMinTime
**Only on `daily`**. The point in which the minimum `precipIntensity` occurs represented in UNIX time.

#### precipProbability
The probability of precipitation occurring expressed as a decimal between 0 and 1 inclusive.

- Currently `precipProbability` is the chance of precipitation occurring at the requested time.
- Hourly `precipProbability` is the chance of precipitation occurring in that hour.
- Daily `precipProbability` is the maximum chance of precipitation occurring in that day. If the maximum `precipProbability` for a day is 80% then the daily `precipProbability` would be 80%. For day 0, this is the probability of precipitation during the remaining hours of the day.

You can get a probability >0 with no precipitation. It's because they're sometimes coming from different sources or different models, and the ensemble will sometimes show a chance of something but not confident in any amount. Basically, one is probabilistic, the other deterministic. 

#### precipType
The type of precipitation occurring. If `precipIntensity` is greater than zero this property will have one of the following values: `rain`, `snow` or `sleet` otherwise the value will be `none`. `sleet` is defined as any precipitation which is neither rain nor snow. For the `daily` block, the following process is used to assess a type when multiple precipitation types are expected:

1. If more than 1 mm of ice is forecast, then ice. Otherwise:
2. If there is more than 5 cm of snow, then snow. Otherwise:
3. If there is more than 10 mm of rain, then rain Otherwise:
4. Use the most common precipitation type.

See [this issue](https://github.com/Pirate-Weather/pirateweather/issues/413) for additional discussion.

#### pressure
The sea-level pressure represented in hectopascals or millibars depending on the requested `units`.

#### snowAccumulation
**Only on `hourly` and `daily`**. The amount of snow precipitation expected to fall over an hour or a day expressed in centimetres or inches depending on the requested `units`.

#### smoke
**Only on `currently` and `hourly`**. **Only available for the US and parts of Canada. Only returns data for the next 36-hours. If there is no data this will return -999.** The amount of near-surface (8 m) smoke represented in µg/m<sup>3</sup>.

#### smokeMax
**Only on `daily`.** The maxiumum `smoke` for the given day.

#### smokeMaxTime
**Only on `daily`.** the time in which the maxiumum `smoke` occurs represented in UNIX time.

#### summary
A human-readable summary describing the weather conditions for a given data point. The daily summary is calculated between 4:00 am and 4:00 am local time. For a full list of possible summary values you can view [Appendex A in the translations repository](https://github.com/Pirate-Weather/translations?tab=readme-ov-file#appendix-a-pirate-weather-summary-format).

#### sunriseTime
**Only on `daily`**. The time when the sun rises for a given day represented in UNIX time.

#### sunsetTime
**Only on `daily`**. The time when the sun sets for a given day represented in UNIX time.

#### temperature
The air temperature in degrees Celsius or degrees Fahrenheit depending on the requested `units`

#### temperatureHigh
**Only on `daily`**. The daytime high temperature calculated between 6:01 am and 6:00 pm local time.

#### temperatureHighTime
**Only on `daily`**. The time in which the high temperature occurs represented in UNIX time.

#### temperatureLow
**Only on `daily`**. The overnight low temperature calculated between 6:01 pm and 6:00 am local time.

#### temperatureLowTime
**Only on `daily`**. The time in which the low temperature occurs represented in UNIX time.

#### temperatureMax
**Only on `daily`**. The maximum temperature calculated between 12:00 am and 11:59 pm local time.

#### temperatureMaxTime
**Only on `daily`**. The time in which the maximum temperature occurs represented in UNIX time.

#### temperatureMin
**Only on `daily`**. The minimum temperature calculated between 12:00 am and 11:59 pm local time.

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
Note that alerts are only supported in the United States at the moment.

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
The time in which the alert was issued represented in UNIX time. From the NWS `effective` time.

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

#### sourceIDX
The X,Y coordinate and the lat, lon coordinate for the grid cell used for each model used to generate the forecast.

#### nearest-station
Not implemented, and will always return 0.

#### units
Indicates which units were used in the forecasts.

#### version
The version of Pirate Weather used to generate the forecast.

### Response Headers

#### Cache-Control
The directive on how the response data can be cached.

#### Ratelimit-Limit
The number of API calls you can do per month.

#### Ratelimit-Remaining
The number of API calls remaining for the month.

#### Ratelimit-Reset
The time in seconds until your rate limit resets.

#### X-Forecast-API-Calls
The number of API calls your key has done for the month.

#### X-Node-Id
Shows which node processed your API call.

#### X-Response-Time
The time taken to process the request in milliseconds.

### Error Codes

#### 400 Bad Request
You may encounter this error if you query the API using an invalid latitude or longitude.

#### 401 Unauthorized
You may encounter this error if you try to query an endpoint your API key does not have access to or if you did not include an API key in your request.

#### 404 Not Found
You may encounter this error if query the API using an invalid route or if you do not supply a latitude or longitude in your request.

#### 429 Too Many Requests
You may encounter this error if your API key has hit the quota for the month.

#### 500 Internal Server Error
If the API returns a 500 error you can retry the request to see if the API will return a 500 error again. If the issue persists please check the [GitHub issues](https://github.com/Pirate-Weather/pirateweather/issues) to see if the issue has been reported otherwise create a [bug report](https://github.com/Pirate-Weather/pirateweather/issues/new?assignees=&labels=bug%2CNeeds+Review&projects=&template=report_bug.yml) and the issue will be investigated.
