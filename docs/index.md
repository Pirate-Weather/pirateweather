<div class="imageContainer">
  <div class="text-block">
    <h1 style="color: white;">Pirate Weather</h1>
  </div>
</div>

[Get an API key](https://pirate-weather.apiable.io/){ .md-button .md-button--primary }

## Quick Links
* To [**register for the API**](https://pirate-weather.apiable.io/)
* [Get a weather forecast in the Dark Sky style](https://merrysky.net/)
* [Home Assistant Integration](https://github.com/alexander0042/pirate-weather-hacs)
* [API repo](https://github.com/alexander0042/pirateweather)
* [Open Source code repo](https://github.com/Pirate-Weather/pirate-weather-code)
* [Changelog](https://pirateweather.net/en/latest/changelog/)
* [Status page](https://pirateweather.xitoring.io/)


#### Publications and Press
* [AWS blog post](https://aws.amazon.com/blogs/publicsector/making-weather-forecasts-accessible-serverless-infrastructure-open-data-aws/)
* [TLDR Newsletter](https://tldr.tech/tech/2023-01-11)
* [BoingBoing](https://boingboing.net/2023/01/10/pirate-weather-api-has-more-features.html)
* [Hacker News Front Page](https://news.ycombinator.com/item?id=34329988)

# Who is using PirateWeather?

- [MerrySky](https://merrysky.net) - Get a Forecast DarkSky Style
- [PW-forecast](https://github.com/ktrue/PW-forecast) and [https://saratoga-weather.org/scripts-PWforecast.php](https://saratoga-weather.org/scripts-PWforecast.php)
- [Breezy Weather](https://github.com/breezy-weather/breezy-weather)
- [Weathergraph](https://weathergraph.app/) - Graphical hour-by-hour forecast & widget for iOS, Apple Watch and mac

## Libraries
- [python-pirate-weather](https://github.com/cloneofghosts/python-pirate-weather) - A thin Python Wrapper for the Pirate Weather API forked from the [forecastio python library](https://github.com/ZeevG/python-forecast.io).
- [pirate-weather-python](https://github.com/Pirate-Weather/pirate-weather-python)

Do you use PirateWeather? Open a [pull request](https://github.com/Pirate-Weather/pirateweather/compare) to add it to the list.

# Introduction 
Weather forecasts are primarily found using models run by government agencies, but the [outputs](https://weather.gc.ca/grib/what_is_GRIB_e.html) aren't easy to use or in formats built for the web.
To try to address this, I've put together a service that reads weather forecasts and serves it following the [Dark Sky API](https://web.archive.org/web/20200723173936/https://darksky.net/dev/docs) style. 

Before going any farther, I wanted to add a [link to sign up and support this project](https://pirate-weather.apiable.io/products/weather-data)! Running this on AWS means that it scales beautifully and is much more reliable than if I was trying to host this, but also costs real money. I'd love to keep this project going long-term, but I'm still paying back my student loans, which limits how much I can spend on this! Anything helps, and a $2 monthly donation lets me raise your API limit from 10,000 calls/ month to 20,000 calls per month.

Alternatively, I also have a GitHub Sponsorship page set up on my [profile](https://github.com/sponsors/alexander0042/)! This gives the option to make a one-time donation to contribute this project. This project (especially the free tier) wouldn't be possible without the ongoing support from the project sponsors, so they're the [heros here](https://github.com/sponsors/alexander0042/)! 

<iframe src="https://github.com/sponsors/alexander0042/card" title="Sponsor alexander0042" height="225" width="600" style="border: 0;"></iframe>

## Recent Updates- Winter 2025
Up to version 2.9! As always, details are available in the [changelog](https://pirateweather.net/en/latest/changelog/).

* Added more fallback ingest sources as per [PR #483](https://github.com/Pirate-Weather/pirate-weather-code/pull/483).
* Fix ERA5 Rounding for precipitation type as per [PR #477](https://github.com/Pirate-Weather/pirate-weather-code/pull/477).
* Add ice/mixed precipitation types as per [PR #467](https://github.com/Pirate-Weather/pirate-weather-code/pull/467).
* Fix an issue where some v2 fields were displaying in v1 requests as per [PR #450](https://github.com/Pirate-Weather/pirate-weather-code/pull/450).
* Add support for DWD MOSMIX forecasts where available as per [PR #449](https://github.com/Pirate-Weather/pirate-weather-code/pull/449).
* Refactor the codebase to break out the functions and simplify the code as [PR #438](https://github.com/Pirate-Weather/pirate-weather-code/pull/438).

## Background
This project started from two points: as part of my [PhD](https://coastlines.engineering.queensu.ca/dunexrt), I had to become very familiar with working with NOAA forecast results (<https://orcid.org/0000-0003-4725-3251>). Separately, an old tablet set up as a "Magic Mirror,” and was using a [weather module](https://github.com/jclarke0000/MMM-DarkSkyForecast) that relied on the Dark Sky API, as well as my [Home Assistant](https://www.home-assistant.io/) setup. So when I heard that it was [shutting down](https://blog.darksky.net/dark-sky-has-a-new-home/), I thought, "I wonder if I could do this.” Plus, I love learning new things (<http://alexanderrey.ca/>), and I had been looking for a project to learn Python on, so this seemed like the perfect opportunity!
Spoiler alert, but it was way more difficult than I thought, but learned a lot throughout the process, and I think the end result turned out really well! 

## Why?
This API is designed to be a drop in replacement/ alternative to the Dark Sky API, and as a tool for assessing GFS, HRRR and NBM forecasts via a JSON API. This solves two goals:

1. It will also allow **legacy** applications to continue running after the Dark Sky shutdown, since as Home Assistant Integrations, Magic Mirror cards, and a whole host of other applications that have been developed over the years.
2. For anyone that is interested in knowing **exactly** how your weather forecasts are generated, this is the "show me the numbers" approach, since the data returned is directly from NOAA models, and every processing step I do is [documented](https://blog.pirateweather.net/). There are [lots](https://openweathermap.org/) [of](https://www.theweathernetwork.com) [existing](https://weather.com) [services](https://www.accuweather.com/) that provide custom forecasts using their own unique technologies, which can definitely improve accuracy, but I'm an engineer, so I wanted to be able to know what's going into the forecasts I'm using. If you're the sort of person who wants a [dense 34-page PowerPoint](http://rapidrefresh.noaa.gov/pdf/Alexander_AMS_NWP_2020.pdf) about why it rained when the forecast said it wouldn't, then this might be for you.
3. I wanted to provide a more **community focused** source of weather data. Weather is local, but I'm only in one spot, so I rely on people filing [issues](https://github.com/alexander0042/pirateweather/issues) to help improve the forecast!
