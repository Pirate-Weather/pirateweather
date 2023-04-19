This integration is designed to replace the defunct Dark Sky integration in Home Assistant with a modified and updated, but fully compatible version that relies on the [Pirate Weather API](https://pirateweather.net/en/latest/) instead!

While this integration is designed to be compatible with Dark Sky, the underlying code is significantly different. This version is designed to work with more modern versions of Home Assistant, and relies on asyncio, unified data update coordinators, and setup via the UI! A [legacy branch](https://github.com/alexander0042/pirate-weather-ha/tree/Legacy-Dark-Sky) that is a 1:1 replacement for the previous Dark Sky integration is also available, but is not recommended.

# Installation
There are two methods to install this installation:

## HACS Installation (easiest)
1. Add `https://github.com/alexander0042/pirate-weather-ha` as a custom repository
2. Restart Home Assistant
3. Register for a Pirate Weather API Key here: <https://pirate-weather.apiable.io>
4. Log into the Pirate Weather API interface (<https://pirate-weather.apiable.io>) and subscribe to the API!
5. Add the Pirate Weather on the Integrations page of your Home Assistant Installation following the steps below.

## Manual Installation 
1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_component` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `pirateweather`.
4. Download _all_ the files from the `custom_components/pirateweather/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant
7. Register for a Pirate Weather API Key here: <https://pirate-weather.apiable.io>
8. Log into the Pirate Weather API interface (<https://pirate-weather.apiable.io>), and subscribe to the API!
9. Add the Pirate Weather on the Integrations page of your Home Assistant Installation following the steps below.

## Configuration
The use to integration, click on the "Add Integration" button on the Integrations page in the Home Assistant Settings and search for Pirate Weather. This will open the add integration UI, shown below.

![Integration_Setup_A](https://github.com/alexander0042/pirate-weather-ha/blob/master/Integration_Setup_A.png?raw=true)

- The *API key* can be received from [Apiable](https://pirate-weather.apiable.io), and is only used to track usage and keep my AWS bills reasonable
- The *Integration Name* is what this weather source will be called. If you want to track the weather at multiple locations, change this. 
- The *Latitude* and *Longitude* for the forecast.
- The update interval the forecast (in seconds). Anything below 15 minutes will likely lead to running out of quota.
- Select if a *Weather Entity* and/or *Sensor Entity* is required. A Weather Entity creates the dashboard standard weather card, and can either provide a daily or hourly forecast. Selecting Sensor Entity will create separate sensors for each condition and forecast time. For example, a sensor for the temperature on day 0 (today), day 1, and day 2, for a total of three sensors. If unsure, start with leaving only the Weather Entity selected.

![Integration_Setup_B](https://github.com/alexander0042/pirate-weather-ha/blob/master/Integration_Setup_B.png?raw=true)

- The *Forecast Mode* for the Weather Entity, either forecasts every hour or every day.
- The language. At the moment, only English is supported.
- The days forecast sensors should be created for, in a csv list.
- The hours forecast sensors should be created for, in a csv list.
- The monitored conditions forecast sensors should be created for.
- If values should be rounded to the nearest integer.
- And which units the forecast sensors should be in. This integration works with the built-in Home Assistant units; however, this option allows rounding to be used.

### YAML Configuration
YAML configuration is still supported, but is depreciated and may be removed at some point in the future. If the integration detects an existing YAML integration, it will import and save it, allowing the yaml to be safely removed.

To use the integration via this approach, either add or edit to your `configuration.yaml` file with this block, using the new API key:

```yaml
weather:
  - platform: pirateweather
    api_key: <APIKEY>
    # Additional optional values:
    latitude: Location latitude
    longitude: Location longitude
    mode: "hourly" (default) or "daily"
    name: Custom name
    

# you can also get a sensor data
sensor:
  - platform: pirateweather
    api_key: <APIKEY>
    scan_interval: '00:15:00'
    monitored_conditions:
      - temperature
      - precip_probability
      - precip_type
      - humidity
      - cloud_cover
      - nearest_storm_distance
      - precip_intensity
      - wind_speed
```

## Documentation
In Progress.

## Frequently Asked Questions
### Can I update my API key or update interval after the initial setup?
No. the way HA stores the data and sets things up means that it's not possible to update the key/update interval after creation.
