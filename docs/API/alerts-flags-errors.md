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
The time in which the alert was issued represented in UNIX time. From the `effective` time.

#### expires
The time in which the alert expires represented in UNIX time. Note: -999 will be returned for alerts without an expires time.

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
Distance to the closest DWD MOSMIX station to your location in kilometres or miles depending on the units. If there are no stations for your location this will return -999.

#### units
Indicates which units were used in the forecasts.

#### version
The version of Pirate Weather used to generate the forecast.

#### processTime
The time taken to process the request in milliseconds.

#### ingestVersion
The ingest version of Pirate Weather used to generate the forecast.

#### nearestCity
The name of the closest city to your location.

#### nearestCountry
The name of the closest country to your location.

#### nearestSubNational
The name of the closest state or province to your location.

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


