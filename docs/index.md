# Pirate Weather: A Modern, Developer-Centric, Open-Source, Extensively Documented Weather API
<div class="imageContainer">
  <div class="text-block">
    <h1 style="color: white;">Pirate Weather</h1>
  </div>
</div>

[Get an API key](https://pirate-weather.apiable.io/products/weatherdata/plans){ .md-button .md-button--primary }
[Try It Now](TryItNow.md){ .md-button }

## Quick Links
* To [**register for the API**](https://pirate-weather.apiable.io/)
* [Connect the Pirate Weather MCP server](#mcp-server)
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

## Who is using Pirate Weather?

- [MerrySky](https://merrysky.net) - Get a Forecast DarkSky Style
- [PW-forecast](https://github.com/ktrue/PW-forecast) and [https://saratoga-weather.org/scripts-PWforecast.php](https://saratoga-weather.org/scripts-PWforecast.php)
- [Breezy Weather](https://github.com/breezy-weather/breezy-weather)
- [Weathergraph](https://weathergraph.app/) - Graphical hour-by-hour forecast & widget for iOS, Apple Watch and mac
- [Pirate Weather for KDE Plasma](https://github.com/txhammer68/pirateWeather) - KDE Plasma 6 weather widget
- [Chrome Pirate Weather Extension](https://chromewebstore.google.com/detail/pirate-weather-extension/akfgfkkfjpbpplibpcffankjdjgpkedd) - Chrome extension for precipitation alerts, forecasts, and saved locations.
- [AccessiWeather](https://github.com/Orinks/AccessiWeather) - Accessible cross-platform weather app with screen-reader-friendly forecasts, alerts, and Pirate Weather support.
- [Temperature Report](https://temperature.report/) - Weather website designed to make it easy to see an overview of upcoming weather.

## Libraries
- [python-pirate-weather](https://github.com/cloneofghosts/python-pirate-weather) - A thin Python Wrapper for the Pirate Weather API forked from the [forecastio python library](https://github.com/ZeevG/python-forecast.io).
- [pirate-weather-python](https://github.com/Pirate-Weather/pirate-weather-python)

Do you use Pirate Weather? Open a [pull request](https://github.com/Pirate-Weather/pirateweather/compare) to add it to the list.

# Introduction 
Weather forecasts are primarily found using models run by government agencies, but the [outputs](https://weather.gc.ca/grib/what_is_GRIB_e.html) aren't easy to use or in formats built for the web.
To try to address this, I've put together a service that reads weather forecasts and serves it following the [Dark Sky API](https://web.archive.org/web/20200723173936/https://darksky.net/dev/docs) style. 

Before going any farther, I wanted to add a [link to sign up and support this project](https://pirate-weather.apiable.io/products/weatherdata)! Running this on AWS means that it scales beautifully and is much more reliable than if I was trying to host this, but also costs real money. I'd love to keep this project going long-term, but I'm still paying back my student loans, which limits how much I can spend on this! Anything helps, and a $2 monthly donation lets me raise your API limit from 10,000 calls/ month to 20,000 calls per month.

Alternatively, I also have a GitHub Sponsorship page set up on my [profile](https://github.com/sponsors/alexander0042/)! This gives the option to make a one-time donation to contribute this project. This project (especially the free tier) wouldn't be possible without the ongoing support from the project sponsors, so they're the [heros here](https://github.com/sponsors/alexander0042/)! 

<iframe src="https://github.com/sponsors/alexander0042/card" title="Sponsor alexander0042" height="225" width="600" style="border: 0;"></iframe>

## Recent Updates- Spring 2026
Up to version 2.9.6! As always, details are available in the [changelog](https://pirateweather.net/en/latest/changelog/).

* Added the hosted MCP server as per [PR #638](https://github.com/Pirate-Weather/pirate-weather-code/pull/638) and [PR #641](https://github.com/Pirate-Weather/pirate-weather-code/pull/641).
* Added city/country location requests such as `Ottawa,Canada` or `New%20York,US` as per [PR #642](https://github.com/Pirate-Weather/pirate-weather-code/pull/642).
* Changed `fireIndex` to be calculated from temperature, humidity, and wind speed wherever those inputs are available as per [PR #643](https://github.com/Pirate-Weather/pirate-weather-code/pull/643).
* Added AI models behind the `include=aimodels` flag as per [PR #610](https://github.com/Pirate-Weather/pirate-weather-code/pull/610).
* Extended historic data requests back to 7 days using the `days=7` flag as per [PR #624](https://github.com/Pirate-Weather/pirate-weather-code/pull/624).

## MCP Server
In addition to the main REST endpoint, Pirate Weather exposes a new, hosted MCP server for apps and agents that support remote streamable HTTP MCP servers. Add it to your MCP client with this URL:

```
https://mcp.pirateweather.net/mcp?apikey=<APIKEY>
```

Replace `<APIKEY>` with your Pirate Weather API key. The MCP server uses the same API key as regular forecast requests, returns Pirate Weather API version 2 style responses, and adds a `timeISO` field next to returned UNIX `time` fields for easier reading.

The available tools include forecast, current weather, hourly forecast, minutely forecast, tomorrow forecast, daily forecast, alerts, historical weather, weather summary, API connection status, and subscription status helpers. Most forecast tools accept `units` and `lang`; supported units are `auto`, `us`, `si`, `ca`, `uk`, and `uk2`.

## Background
This project started from two points: as part of my [PhD](https://coastlines.engineering.queensu.ca/dunexrt), I had to become very familiar with working with NOAA forecast results (<https://orcid.org/0000-0003-4725-3251>). Separately, an old tablet set up as a "Magic Mirror,” and was using a [weather module](https://github.com/jclarke0000/MMM-DarkSkyForecast) that relied on the Dark Sky API, as well as my [Home Assistant](https://www.home-assistant.io/) setup. So when I heard that it was [shutting down](https://blog.darksky.net/dark-sky-has-a-new-home/), I thought, "I wonder if I could do this.” Plus, I love learning new things (<http://alexanderrey.ca/>), and I had been looking for a project to learn Python on, so this seemed like the perfect opportunity!
Spoiler alert, but it was way more difficult than I thought, but learned a lot throughout the process, and I think the end result turned out really well! 

## Why?
This API is designed to be a drop in replacement/ alternative to the Dark Sky API, and as a tool for assessing GFS, HRRR and NBM forecasts via a JSON API. This solves two goals:

1. It will also allow **legacy** applications to continue running after the Dark Sky shutdown, since as Home Assistant Integrations, Magic Mirror cards, and a whole host of other applications that have been developed over the years.
2. For anyone that is interested in knowing **exactly** how your weather forecasts are generated, this is the "show me the numbers" approach, since the data returned is directly from NOAA models, and every processing step I do is [documented](https://blog.pirateweather.net/). There are [lots](https://openweathermap.org/) [of](https://www.theweathernetwork.com) [existing](https://weather.com) [services](https://www.accuweather.com/) that provide custom forecasts using their own unique technologies, which can definitely improve accuracy, but I'm an engineer, so I wanted to be able to know what's going into the forecasts I'm using. If you're the sort of person who wants a [dense 34-page PowerPoint](http://rapidrefresh.noaa.gov/pdf/Alexander_AMS_NWP_2020.pdf) about why it rained when the forecast said it wouldn't, then this might be for you.
3. I wanted to provide a more **community focused** source of weather data. Weather is local, but I'm only in one spot, so I rely on people filing [issues](https://github.com/alexander0042/pirateweather/issues) to help improve the forecast!

