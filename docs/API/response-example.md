### API Response Example
```
	GET https://api.pirateweather.net/forecast/1234567890abcdefghijklmnopqrstuvwxyz/45.42,-74.30?&units=ca
	"latitude": 45.42,
	"longitude": -74.3,
	"timezone": "America/Toronto",
	"offset": -5,
	"elevation": 77,
	"currently": {
		"time": 1762718100,
		"summary": "Light Snow",
		"icon": "snow",
		"nearestStormDistance": 17.88,
		"nearestStormBearing": 270,
		"precipIntensity": 0.5321,
		"precipProbability": 0.61,
		"precipIntensityError": 0.159,
		"precipType": "snow",
		"temperature": -0.88,
		"apparentTemperature": -6.77,
		"dewPoint": -3.5,
		"humidity": 0.82,
		"pressure": 1015.24,
		"windSpeed": 17.73,
		"windGust": 46.84,
		"windBearing": 41,
		"cloudCover": 0.81,
		"uvIndex": 0.38,
		"visibility": 16.09,
		"ozone": 311.75
	},
	"minutely": {
		"summary": "Flurries for the hour.",
		"icon": "snow",
		"data": [
		{
			"time": 1762718100,
			"precipIntensity": 0.5321,
			"precipProbability": 0.61,
			"precipIntensityError": 0.159,
			"precipType": "snow"
		},
	   ...
	  ]
	},
	"hourly": {
		"summary": "Sleet (with a chance of 6–8 cm. of snow) until tomorrow morning and foggy tomorrow afternoon.",
		"icon": "sleet",
		"data": [
			{
				"time": 1762714800,
				"summary": "Light Snow",
				"icon": "snow",
				"precipIntensity": 0.508,
				"precipProbability": 0.47,
				"precipIntensityError": 0.15,
				"precipAccumulation": 0.2985,
				"precipType": "snow",
				"temperature": -0.49,
				"apparentTemperature": -7.05,
				"dewPoint": -3.38,
				"humidity": 0.81,
				"pressure": 1015.9,
				"windSpeed": 21.6,
				"windGust": 35.28,
				"windBearing": 50,
				"cloudCover": 0.93,
				"uvIndex": 0.52,
				"visibility": 4.05,
				"ozone": 313.39
			},
	    	...
		]
	},
	"day_night": {
		"data": [
			{
				"time": 1762678800,
				"summary": "Snow (1–3 cm.) in the afternoon.",
				"icon": "snow",
				"precipIntensity": 0.2345,
				"precipIntensityMax": 1.778,
				"precipProbability": 0.81,
				"precipAccumulation": 1.8828,
				"precipType": "snow",
				"temperature": 0.04,
				"apparentTemperature": -5.22,
				"dewPoint": -4.69,
				"humidity": 0.76,
				"pressure": 1016.93,
				"windSpeed": 16.62,
				"windGust": 28.36,
				"windBearing": 56,
				"cloudCover": 0.87,
				"uvIndex": 0.53,
				"visibility": 10.96,
				"ozone": 314.77,
				"smoke": 0,
			},
	    	...
		]
	},
	"daily": {
	"summary": "Mixed precipitation today through Wednesday and next Sunday, with high temperatures peaking at 3°C on Thursday.",
	"icon": "sleet",
	"data": [
		{
			"time": 1762664400,
			"summary": "Sleet (with a chance of 6–8 cm. of snow) starting in the afternoon.",
			"icon": "sleet",
			"sunriseTime": 1762688903,
			"sunsetTime": 1762723986,
			"moonPhase": 0.65,
			"precipIntensity": 0.7514,
			"precipIntensityMax": 3.81,
			"precipIntensityMaxTime": 1762732800,
			"precipProbability": 1,
			"precipAccumulation": 7.5957,
			"precipType": "sleet",
			"rainIntensityMax": 1.27,
			"temperatureHigh": 0.04,
			"temperatureHighTime": 1762704000,
			"temperatureLow": -1.29,
			"temperatureLowTime": 1762732800,
			"apparentTemperatureHigh": -5.22,
			"apparentTemperatureHighTime": 1762704000,
			"apparentTemperatureLow": -7.92,
			"apparentTemperatureLowTime": 1762732800,
			"dewPoint": -3.96,
			"humidity": 0.81,
			"pressure": 1015.02,
			"windSpeed": 15.36,
			"windGust": 26.74,
			"windGustTime": 1762725600,
			"windBearing": 62,
			"cloudCover": 0.89,
			"uvIndex": 1.8,
			"uvIndexTime": 1762704000,
			"visibility": 9.29,
			"temperatureMin": -2.81,
			"temperatureMinTime": 1762664400,
			"temperatureMax": 0.04,
			"temperatureMaxTime": 1762704000,
			"apparentTemperatureMin": -7.92,
			"apparentTemperatureMinTime": 1762732800,
			"apparentTemperatureMax": -5.22,
			"apparentTemperatureMaxTime": 1762704000
		},
	    ...
	  ]
	}
	"alerts": [
		{
			"title": "avertissement de neige en vigueur",
			"regions": [
				"secteur de Soulanges"
			],
			"severity": "Moderate",
			"time": 1762704172,
			"expires": 1762761772,
			"description": "Première bordée de neige de la saison\n\nQuoi : jusqu'à 10 centimètres de neige sont possibles\n\nQuand : d'aujourd'hui à tard ce soir\n\nOù : sud de la province\n\nInformations supplémentaires :\nLa neige pourrait devenir mêlée de grésil par moments. Un court épisode de pluie verglaçante est possible ce soir. Les précipitations se changeront en pluie tard ce soir.\n\nCes conditions pourraient rendre les routes enneigées et glissantes, compliquant ainsi les déplacements dimanche et lundi.\n\n###\n\nLa visibilité sera probablement réduite par moments.\n\nUn avertissement de neige est émis lorsqu’on prévoit des impacts significatifs en raison d’une accumulation de neige.\n\nVeuillez continuer à surveiller les alertes et les prévisions émises par Environnement Canada. Pour signaler du temps violent, envoyez un courriel à meteoQC@ec.gc.ca ou publiez un message sur X en utilisant #meteoqc.",
			"uri": "https://severeweather.wmo.int/v2/cap-alerts/ca-msc-xx/2025/11/09/16/09/12-3372a8228b861e43112cdf50691d180.xml"
		},
	]
	"flags": {
		"sources": [
			"ETOPO1",
			"hrrrsubh",
			"rtma_ru",
			"hrrr_0-18",
			"nbm",
			"nbm_fire",
			"ecmwf_ifs",
			"hrrr_18-48",
			"gfs",
			"gefs"
		],
		"sourceTimes": {
			"hrrr_subh": "2025-11-09 17Z",
			"rtma_ru": "2025-11-09 19:30Z",
			"hrrr_0-18": "2025-11-09 17Z",
			"nbm": "2025-11-09 17Z",
			"nbm_fire": "2025-11-09 12Z",
			"ecmwf_ifs": "2025-11-09 00Z",
			"hrrr_18-48": "2025-11-09 12Z",
			"gfs": "2025-11-09 12Z",
			"gefs": "2025-11-09 12Z"
		},
		"nearest-station": -999,
		"units": "ca",
		"version": "V2.10.0"
  	}
```

### Time Machine Request
The Time Machine uses either archived 1-hour model results (last 10 days) or the [Google ERA5 dataset](https://developers.google.com/earth-engine/datasets/catalog/ECMWF_ERA5_HOURLY) which is updated weekly and is approximately ten days behind realtime. The forecast request can be extended in several ways by adding parameters to the URL. The full set of URL options is:

```
      https://timemachine.pirateweather.net/forecast/[apikey]/[latitude],[longitude],[time]?exclude=[excluded]&units=[unit]
      https://timemachine.pirateweather.net/forecast/[apikey]/[city],[country],[time]?exclude=[excluded]&units=[unit]
```

Crucially, there's now three different ways a request could be handled:

1. Requests for the last 24 hours use all the sources and are unchanged;
2. Request for the last 10 days rely only on GFS data (although ECMWF would be easy to add) stored in the zip file on the server;
3. Requests >10 days rely on Google's ERA5 zarr dataset, which is a perfect source for this sort of application.

The response format is the same as the forecast except:

* The `currently` block will refer to the requested time and not the present time.
* The `minutely` block is not present except when querying data from the last 24h.
* The `hourly` block will return data from midnight of the requested day to midnight the next day.
* The `day_night` block is not included.
* The `daily` block will return the data for the current day except when querying data from the last 24h.
* The `alerts` block is not included.
* The `flags` block will show the sources used in the request, the requested `units` and the API version.

When requesting data from the PW archive, the optional `tmextra` query parameter controls which variables are returned. When it is included, same variables that are present in a forecast request (except alerts) are returned. When it is not included (by default), the same range of parameters returned by ERA5 requests is included.

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
	"summary": "Overcast",
	"icon": "cloudy",
	"precipIntensity": 0,
	"precipType": "none",
	"temperature": 15.2,
	"apparentTemperature": 11.61,
	"dewPoint": 7.57,
	"pressure": 1016.18,
	"windSpeed": 15.23,
	"windGust": 24.4,
	"windBearing": 72,
	"cloudCover": 1
  },
  "hourly": {
    "data": [
      {
        "time": 1654056000,
		"summary": "Overcast",
		"icon": "cloudy",
		"precipIntensity": 0,
		"precipAccumulation": 0,
		"precipType": "none",
		"temperature": 15.2,
		"apparentTemperature": 11.61,
		"dewPoint": 7.57,
		"pressure": 1016.18,
		"windSpeed": 15.23,
		"windGust": 24.4,
		"windBearing": 72,
		"cloudCover": 1
      },
     ...
    ]
  },
  "daily": {
    "data": [
      {
        "time": 1654056000,
		"summary": "Rain throughout the day.",
		"icon": "rain",
		"sunriseTime": 1654074749,
		"sunsetTime": 1654130288,
		"moonPhase": 0.06,
		"precipIntensity": 0.3127,
		"precipIntensityMax": 2.9816,
		"precipIntensityMaxTime": 1654088400,
		"precipAccumulation": 0.7526,
		"precipType": "rain",
		"rainIntensityMax": 2.9816,
		"temperatureHigh": 16.37,
		"temperatureHighTime": 1654102800,
		"temperatureLow": 12.39,
		"temperatureLowTime": 1654092000,
		"apparentTemperatureHigh": 16.27,
		"apparentTemperatureHighTime": 1654102800,
		"apparentTemperatureLow": 8.47,
		"apparentTemperatureLowTime": 1654077600,
		"dewPoint": 9.87,
		"pressure": 1012.11,
		"windSpeed": 15.03,
		"windGust": 30.69,
		"windGustTime": 1654102800,
		"windBearing": 72,
		"cloudCover": 0.98,
		"temperatureMin": 12.39,
		"temperatureMinTime": 1654092000,
		"temperatureMax": 16.37,
		"temperatureMaxTime": 1654102800,
		"apparentTemperatureMin": 8.47,
		"apparentTemperatureMinTime": 1654077600,
		"apparentTemperatureMax": 16.27,
		"apparentTemperatureMaxTime": 1654102800
      }
    ]
  },
  "flags": {
	"sources": [
		"ETOPO1",
		"era5"
	],
	"sourceTimes": {},
	"nearest-station": 0,
	"units": "ca",
	"version": "V2.10.0"
	}
}
```
