# Pirate Weather Repo
This is the primary repository for the Pirate Weather API, a free and open API designed to serve weather forecast data using the same syntax as Dark Sky. 

To sign up, a free API key can be requested at <https://pirateweather.net>. Documentation is at <https://pirateweather.readthedocs.io>. A front end is available at <https://weather.pirateweather.net/>.

## Why

1. Weather forecasts are produced by government agencies using computational models; however, the data is hard to work with. Instead, there are a bunch of companies that take this data, process it, and provide easier to work with APIs. However, the steps that the data goes through aren't public or documented (for example, what do they mean by "percent of precipitation"?!?). I put this service together in order to provide a better way for people to know where their weather data is coming from and how it is being processed! 
2. The Dark Sky API is great, and widely used. Unfortunately, it will shut down at the end of 2022, so in order to keep legacy services operating, I wanted to put a service together that would be drop-in compatible

## What
In this repository, I've included:
    * The Docker image for processing:
     * <https://github.com/alexander0042/pirateweather/tree/main/wgrib2>
 * The processing scripts:
     * <https://github.com/alexander0042/pirateweather/tree/main/scripts>
 * API Documentation:
     * <https://github.com/alexander0042/pirateweather/tree/main/docs>

## Support
Keeping this free and running isn't free, so [donations to support this project](https://github.com/sponsors/alexander0042) are greatly appreciated! Plus, recurring monthly donations let me raise a API limit, allowing more frequent weather refreshes! 