# API Docs
This page serves as the documentation for the Pirate Weather API call and response format. Since this service is designed to be a drop in replacement for the [Dark Sky API](https://web.archive.org/web/20200723173936/https://darksky.net/dev/docs), the goal is to match that as closely as possible, and any disagreement between their service and Pirate Weather will be treated as a bug. However, as Pirate Weather continues to evolve, I plan on adding small, non-breaking additions where I can, and they will be documented here! Plus, always better to have my own (open source and editable) version of the docs!

<!-- An alpha [Swagger UI](https://github.com/swagger-api/swagger-ui) for the API is also available at <https://api.pirateweather.net/docs>. -->

## Request
The minimum structure for every request to this service is the same:
```
https://api.pirateweather.net/forecast/[apikey]/[latitude],[longitude]
``` 
This specifies the service (either `api`, `dev` or `timemachine`), root url (`pirateweather.net/forecast`), the api key used in the request (`[apikey]`), and the location (`[latitude],[longitude]`). You can also request a location by city and country using `[city],[country]`. There are many other ways to customize this request, but this is the minimum requirement! Calling the API with this request will return a JSON data structure (described below) with the requested weather information!
All request attributes are contained within the URL. Request headers are not parsed by the API, and returned headers only contain debugging information, with all the data contained in the JSON payload. 

### Request Parameters
The forecast request can be extended in several ways by adding parameters to the URL. The full set of URL options is:
```
https://api.pirateweather.net/forecast/[apikey]/[latitude],[longitude],[time]?exclude=[excluded]&units=[unit]&extend=[hourly]&version=[2]&lang=[lang]&extraVars=[stationPressure]&include=[included]
https://api.pirateweather.net/forecast/[apikey]/[city],[country],[time]?exclude=[excluded]&units=[unit]&extend=[hourly]&version=[2]&lang=[lang]&extraVars=[stationPressure]&include=[included]
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

Alternatively, location can be specified by city and country using `[city],[country]` (ex. `Ottawa,Canada`, `New%20York,US` or `Paris,France,1704067200` with a time). Spaces and other special characters in the city name should be URL encoded. The country can be a supported country name or alias, an ISO 3166-1 alpha-2 code such as `US`, `CA`, `GB`, `FR`, or `AU`, or a supported alpha-3 alias. City/country requests use offline geocoding and may be slower or less precise than latitude/longitude requests, so latitude/longitude is still recommended when exact coordinates are available.

If you are looking for a place to figure out the latitude and longitude, [https://www.latlong.net/](https://www.latlong.net/) is a good starting point.

#### Time
The time field is optional for the forecast request, but mandatory for a historic request. If present, time can be specified in one of three different ways:

1. UNIX timestamp, or the number of seconds since midnight GMT on 1 Jan 1970 (this is the preferred way). Note that this can be a negative number for pre-1970 dates.
2. A datestring in the local time zone of the location being requested: `[YYYY]-[MM]-[DD]T[HH]:[MM]:[SS]`.
3. A datestring in UTC time: `[YYYY]-[MM]-[DD]T[HH]:[MM]:[SS]Z`
4. A time delta (in either seconds, hours, or days) from the current time: `-86400S` will return data for the previous day. 

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

Note that changing the units will also change the formula for how the air quality index (AQI) is calculated.

#### Exclude
Added as part of the V1.0 release, this parameter removes some of the data blocks from the reply. This can speed up the requests (especially if alerts are not needed!), and reduce the reply size. Exclude parameters can be added as a comma-separated list, with the options being:

* `currently`
* `minutely`
* `hourly`
* `daily`
* `alerts`
* `summary` - Allows you to get the summaries in the old format before the translations module was added. This also improves response times if detailed text is not needed.

Some models can also be excluded, which will force data from the fallback sources to be used:

*  `hrrr`
*  `nbm`
*  `gefs`
*  `gfs`
*  `rtma_ru`
*  `ecmwf_ifs`
*  `dwd_mosmix`
*  `ecmwf_aifs`
*  `aigefs`
*  `aigfs`
*  `raqdps`
*  `silam`

#### Extend
If `extend=hourly` is included, hourly data for the next 168 hours will be included, instead of the standard 48! This adds some time (~0.3s) to the response, since additional processing is required.   

#### Version
If `version>1` is included fields which were not part of the Dark Sky API will be included. These fields are `smoke`, `smokeMax`, `smokeMaxTime`, `fireIndex`, `fireIndexMax`, `fireIndexMaxTime`, `liquidAccumulation`, `snowAccumulation`, `iceAccumulation`, `dawnTime`, `duskTime`, `currentDayIce`, `currentDayLiquid`, `currentDaySnow`, `processTime`, `ingestVersion`, `nearestCity`, `nearestCountry`, `nearestSubNational`, `cape`, `solar`, `capeMax`, `solarMax`, `rainIntensity`, `snowIntensity`, `iceIntensity`, `rainIntensityMax`, `snowIntensityMax`, `iceIntensityMax`, `airQualityIndex`, `airQualityIndexMax` and `airQualityIndexMin`. It also includes `nearestStormDistance` and `nearestStormBearing` to each of the hourly blocks and `sourceIDX` where you can see the X/Y and lat/long coordinate for each returned model.

#### Language
Added as part of the V2.5 release, this parameter allows you to specify what language the text summaries use. The possible values for language may be:

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
	* `tet`: Tetum
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

#### Extra Variables 
`extraVars=` is used to show additional parameters that are not required for most users and may cause confusion. Currently, only `stationPressure` is allowed, but others may be added in the future. 

#### Include
`include=` is used to add additional data blocks not available in the Dark Sky API.  Currently, `day_night_forecast`, `aimodlels` and `airqualitydetails` are allowed, but others may be added in the future.

If `airqualitydetails` is added as an include flag the API will return full pollutant details for the following pollutants:

- `coConcentration`
- `no2Concentration`
- `ozoneConcentration`
- `so2Concentration`
- `pm10`
- `pm25`

If `day_night_forecast` is added as an include flag then the twice-daily forecast will be included.

If `aimodels` is added then results from the AI driven models (AIGFS/AIGEFS/ECMWF-AIFS) will be included.

#### AQI Unit Override
`aqiunits=` is used to override the default AQI scale for your selected units. The following values are accepted:

- `uk` for the UK DAQI scale
- `eu` for the modified EAQI scale
- `ca` for the AQHI scale
- `us` for the US EPA scale


