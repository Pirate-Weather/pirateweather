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

### day_night
A block containing a day and night forecast for the next 7 days. The day portion of the forecast is calculated from 4:00 am to 4:59 pm and the night portion is calculated from 5:00 pm to 3:59 am. The data is included as a 16 item list, alternating between the day and night forecast starting from the current day.

### daily
A block containing the day-by-day forecasted conditions for the next 7 days.

### alerts
A block containing any severe weather alerts if any for the current location.

### flags
A block containing miscellaneous data for the API request.

### Data Point

#### apparentTemperature
Temperature adjusted for wind and humidity, based the [Steadman 1994](http://www.bom.gov.au/jshess/docs/1994/steadman.pdf) approach used by the Australian Bureau of Meteorology. Implemented using the [Breezy Weather approach](https://github.com/breezy-weather/breezy-weather/discussions/1085#discussioncomment-9734935) with solar radiation, which follows this equation:

$$ AT = Ta + 0.348 × rh / 100 × 6.105 × exp(17.27 × Ta / (237.7 + Ta)) − 0.70 × ws + 0.70 × Q / (ws + 10) − 4.25$$

- $Ta$ is the ambient temperature in °C
- $ws$ is the wind speed in m/s
- $Q$ is solar radiation in W/m^2

This equation produces results that are similar to heat index and wind chill values.

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

#### cape
The Convective Available Potential Energy measured in J/kg.

#### capeMaxTime
**Only on `daily`.** the time in which the maximum `cape` occurs represented in UNIX time.

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
**Only on `currently` and `hourly`.** The [Fosberg Fire Weather Index](https://www.spc.noaa.gov/exper/firecomp/INFO/fosbinfo.html), calculated from temperature, relative humidity, and wind speed. The API converts these inputs internally to the units used by the Fosberg formula, applies the equilibrium moisture model, and returns a 0-100 style index clipped to the API's normal fire index bounds. This index deals only with weather conditions, not fuels, and so a high index area is not necessarily high risk for fires. If any required input is unavailable, this may return -999.

#### fireIndexMax
**Only on `daily`.** The maximum hourly `fireIndex` for the given day.

#### fireIndexMaxTime
**Only on `daily`.** The time when the maximum hourly `fireIndex` occurs represented in UNIX time.

#### humidity
Relative humidity expressed as a value between 0 and 1 inclusive. This is a percentage of the actual water vapour in the air compared to the total amount of water vapour that can exist at the current temperature. [See this resource for more information.](https://www.sciencedirect.com/topics/agricultural-and-biological-sciences/relative-humidity)

#### iceAccumulation
**Only on `hourly` and `daily`**. The amount of ice precipitation expected to fall over an hour or a day expressed in centimetres or inches depending on the requested `units`. 

### iceIntensity
The intensity of ice precipitation expected to fall over an hour or a day expressed in millimetres or inches depending on the requested `units`. When using data from GEFS/ECMWF, note that for currently/ minutely blocks, modelled intensity is used directly (where available). For hourly/ daily blocks, accumulation is used as the underlying source for this field.


### iceIntensityMax
**Only on `day_night` and `daily`**. The UNIX time the maximum ice intensity occurs.

#### icon
One of a set of icons to provide a visual display of what's happening. This could be one of: 
`clear-day, clear-night, thunderstorm, rain, snow, sleet, wind, fog, cloudy, partly-cloudy-day and partly-cloudy-night` and may include `hail` in the future. In some rare cases the API may return `none` as an icon which could be defined as Not Available.

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
* `possible-thunderstorm-day`
* `possible-thunderstorm-night`
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
* `mixed`

Note that `smoke` and `haze` may be moved to the default icon set in the future, at which point they will be removed from this expanded list.

The daily icon is calculated between 4:00 am and 4:00 am local time. The algorithm here is straightforward, coming from this [NOAA resource](https://weather.com/science/weather-explainers/news/common-weather-terms-used-incorrectly):

##### Currently:

* If precipitation accumulation is greater than 0.02 mm, then the precipitation type.
	* If CAPE is greater than or equal to 2500J/kg then `thunderstorm`.
* If visibility is less than 10 km, then `fog`.
* If winds are greater than 6.7056 m/s, then `wind`.
* If cloud cover is greater than 87.5%, then `cloudy`.
* If cloud cover is greater than 37.5% and less than 87.5%, then `partly-cloudy-day` or `partly-cloudy-night`.
* If cloud cover is less than 37.5%, then `clear`.
  
##### Hourly:

* If precipitation probability is greater than 25% and accumulation is greater than 0.02 mm, then the precipitation type.
	* If CAPE is greater than or equal to 2500J/kg then `thunderstorm`.
* If visibility is less than 10 km, then `fog`.
* If winds are greater than 6.7056 m/s, then `wind`.
* If cloud cover is greater than 87.5%, then `cloudy`.
* If cloud cover is greater than 37.5% and less than 87.5%, then `partly-cloudy-day` or `partly-cloudy-night`.
* If cloud cover is less than 37.5%, then `clear`.

##### Daily and Day/Night:

With the daily summaries being introduced in version 2.7 the day icon now considers the day as a whole rather than using daily averages. The icon shown will generally be whichever condition comes first so if the morning is foggy and the evening is windy the fog icon will be shown. The cloud cover icons will only be shown as long as no other conditions are forecasted for the day.

**Precipitation**

The precipitation icon logic is as follows:

* If max probability is greater than 25% in any hour
* The total accumulation depends on the number of periods has precipitation forecasted
	* Total precipitation needs to be 0.25 mm for one period
	* Total precipitation needs to be 0.50 mm for two periods
	* Total precipitation needs to be 0.75 mm for three periods
	* Total precipitation needs to be 1 mm for four periods

The precipitation with the most accumulation forecasted is generally the icon which is shown unless:

* If maximum CAPE (with precipitation) is greater than 2500J/kg then `thunderstorm`.
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
**Only on `currently`, `hourly` and `day_night`**. The density of total atmospheric ozone at a given time in Dobson units.

#### precipAccumulation
**Only on `hourly`, `day_night` and `daily`**. The total amount of precipitation expected to fall over an hour or a day expressed in centimetres or inches depending on the requested `units`. For day 0, this is the precipitation during the remaining hours of the day.

Snow accumulation is estimated using a [density formulation](https://github.com/Pirate-Weather/pirateweather/issues/89), adjusting based on the temperature and wind speed when the snow falls. It tends to be around 1:10, but will vary when it's a warm, slushy snowfall. 

  * 5 cm (50 mm) of snow is forecasted for an hour, `precipAccumulation`, in cm, will return 5.
  * 5 mm of rain is forecasted for an hour, `precipAccumulation`, in cm, will return 0.5.
  * 5 mm of rain and 5 cm of snow is forecasted for an hour, `precipAccumulation`, in cm, will return 5.5. This illustrates the value of using the `liquidAccumulation`, `snowAccumulation`, and `iceAccumulation` parameters instead of `precipAccumulation`.

#### precipIntensity
Precipitation intensity units have been revised to reflect the Dark Sky style. This means that intensity is always reported in **liquid water equivalent**, and this should be reflected when displaying the data.

  * So if 5 cm (50 mm) of snow is forecasted for an hour, `precipIntensity`, in mm, will return 5, as 5 mm of rain provides 50 mm of snow.
    * If 5 mm of rain is forecasted for an hour, `precipIntensity`, in mm, will return 5, for 5 mm of rain.
  * See [this thread for details](https://github.com/Pirate-Weather/pirate-weather-code/pull/53#issuecomment-2661603131).
  * It is **strongly** recommended to use the type specific intensities.

When using data from GEFS/ECMWF, note that for currently/ minutely blocks, modelled intensity is used directly (where available). For hourly/ daily blocks, accumulation is used as the underlying source for this field.


#### precipIntensityError
The standard deviation of the `precipIntensity` from the GEFS/ECMWF IFS model.

#### precipIntensityMax
**Only on `day_night` and `daily`**. The maximum value of `precipIntensity` for the given day.

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
The type of precipitation occurring. If `precipIntensity` is greater than zero this property will have one of the following values: `rain`, `snow`, or `sleet`. For requests with `version>1`, `ice` and `mixed` are also possible values. If `precipIntensity` is zero, the value will be `none`. `sleet` is defined as any precipitation which is neither rain nor snow. For the `daily` block, the following process is used to assess a type when multiple precipitation types are expected:

1. If more than 1 mm of ice is forecast, then ice. Otherwise:
2. If there is more than 5 cm of snow, then snow. Otherwise:
3. If there is more than 10 mm of rain, then rain Otherwise:
4. Use the most common precipitation type.

If querying the API with `version>1` then the precipitation types are expanded to include `ice` and `mixed`. The `ice` precipitation type is defined as freezing rain and `mixed` is defined as `rain`, `snow` and `ice` precipitation occurring.

See [this issue](https://github.com/Pirate-Weather/pirateweather/issues/413) for additional discussion.

#### pressure
The sea-level pressure represented in hectopascals or millibars depending on the requested `units`.

### rainIntensity
The intensity of rain precipitation expected to fall over an hour or a day expressed in millimetres or inches depending on the requested `units`. When using data from GEFS/ECMWF, note that for currently/ minutely blocks, modelled intensity is used directly (where available). For hourly/ daily blocks, accumulation is used as the underlying source for this field.


### rainIntensityMax
**Only on `day_night` and `daily`**. The UNIX time the maximum rain intensity occurs.

#### snowAccumulation
**Only on `hourly`, `day_night` and `daily`**. The amount of snow precipitation expected to fall over an hour or a day expressed in centimetres or inches depending on the requested `units`. For hourly/ daily blocks, accumulation is used as the underlying source for this field. For minutely and currently blocks, a 10x liquid-water factor is used, while a [physics based approach](https://github.com/Pirate-Weather/pirate-weather-code/blob/87b3a25e8cc614794f552fa327740cabd53fcb41/API/PirateTextHelper.py#L757) is used for the other blocks.

### snowIntensity
The intensity of snow precipitation expected to fall over an hour or a day expressed in centimetres or inches depending on the requested `units`. When using data from GEFS/ECMWF, note that for currently/ minutely blocks, modelled intensity is used directly (where available). For hourly/ daily blocks, accumulation is used as the underlying source for this field. For minutely and currently blocks, a 10x liquid-water factor is used, while a physics based approach is used for the other blocks.

### snowIntensityMax
**Only on `day_night` and `daily`**. The UNIX time the maximum snow intensity occurs.

#### smoke
The amount of near-surface (8 m) smoke represented in µg/m<sup>3</sup>.

#### smokeMax
**Only on `daily`.** The maximum `smoke` for the given day.

#### smokeMaxTime
**Only on `daily`.** the time in which the maximum `smoke` occurs represented in UNIX time.

#### solar
The Downward Short-Wave Radiation Flux measured in W/m^2.

#### solarMax
**Only on `daily`.** the time in which the maximum `solar` occurs represented in UNIX time.

#### stationPressure
**Hidden by default behind the `extraVars=stationPressure` queryparam**.
The station pressure represented in hectopascals or millibars depending on the requested `units`.

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

