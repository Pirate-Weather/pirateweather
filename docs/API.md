# API Docs

This page serves as the documentation for the Pirate Weather API call and responce format. Since this service is designed to be a drop in replacement for the [Dark Sky API](https://web.archive.org/web/20200723173936/https://darksky.net/dev/docs), the goal is to match that as closely as possibile, and any disagrement between their service and Pirate Weather will be treated as a bug. However, as Pirate Weather continues to evolve, I plan on adding small, non-breaking additions where I can, and they will be documented here! Plus, always better to have my own (open source and editable) version of the docs!

## Forecast Request

The minimum structure for every request to this service is the same:
```
      https://api.pirateweather.net/forecast/[apikey]/[latitude],[longitude]
```	

This specifies the service (either `api` or `timemachine`), root url (`pirateweather.net/forecast`), the api key used in the request (`[apikey]`), and the location. There are many other ways to customise this request, but this is the minimum requirement!



### Example

### Request Parameters

### Time Machine Request


## Response

### Data Block


### Data Point


### Alerts


### Flags




