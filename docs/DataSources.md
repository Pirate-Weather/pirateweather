# API Docs
This page serves as the documentation for the underlying data source algorithm for the Pirate Weather API - in short, it explains which parameter comes from where. Since the goal of this API to provide raw model data with as little processing as possible, results from the API should very closely match the model described in this document, with some minor differences due to interpolation. For detailed source-selection rules, see the [Forecast Source Selection README in the API code repository](https://github.com/Pirate-Weather/pirate-weather-code/tree/dev/docs/forecast-source-selection). 

## Data sources
Several models are used to produce the forecast. Most are hosted on [AWS's Open Data Platform](https://registry.opendata.aws/collab/noaa/), and the fantastic [Herbie package](https://github.com/blaylockbk/Herbie) is used to download and perform initial processing for many of them.    

### NOAA

#### RTMA Rapid Update
The Real-Time Mesoscale Analysis Rapid Update [(RTMA-RU)](https://emc.ncep.noaa.gov/emc/pages/numerical_forecast_systems/rtma.php) provides real time analysis for the continental US and parts of Canada. The model runs every 15-minutes and combines the HRRR first guess with observations from satellites and station observations.

RTMA-RU blends a rapidly updating HRRR first guess with whatever observations are available at each 15-minute cycle, the analyses can sometimes show noticeable jumps from one update to the next. Changes in observation availability, timing, or quality—as well as shifts in how strongly the system weights those observations relative to the HRRR first guess—can cause sudden increases or decreases in the analyzed values. These cycle-to-cycle fluctuations are a normal artifact of the rapid-update data assimilation process, and they can appear in any variable, especially in areas with sparse or intermittent observational coverage.

#### URMA
The UnRestricted Mesoscale Analysis [(URMA)](https://www.ncei.noaa.gov/access/metadata/landing-page/bin/iso?id=gov.noaa.ncdc%3AC01581) is NOAA's hourly surface weather analysis, combining model background fields with conventional and satellite-derived observations. It runs six hours after the analysis time to incorporate observations that arrived too late for RTMA. NOAA uses URMA to calibrate and verify the National Blend of Models.

URMA provides analyses for the continental US and Hawaii at 2.5 km resolution, Alaska at 3 km, and Puerto Rico at 1.25 km. Fields include temperature, dew point, wind speed and direction, gusts, surface pressure, visibility, and cloud cover. See [NOAA's RTMA/URMA overview](https://emc.ncep.noaa.gov/emc/pages/numerical_forecast_systems/rtma.php) for details of the analysis system.

Starting in version 2.10.1, Pirate Weather will use URMA for short-term historical requests less than 10 days old within the North America domain. The ingest job runs at 15 minutes past every hour UTC.

#### NBM
The National Blend of Models [(NBM)](https://vlab.noaa.gov/web/mdl/nbm) is a calibrated blend of both NOAA and non-NOAA weather models from around the world. Running every hour for about 7 days, the NBM produces a forecast that aims to leverage strengths from each of the source models, as well as providing some probabilistic forecasts. For most weather elements in the US and Canada, this is the primary source. 

#### HRRR
The High Resolution Rapid Refresh [(HRRR)](https://rapidrefresh.noaa.gov/hrrr/) provides forecasts over all of the continental US, as well as most of the Canadian population. 15-minute forecasts every 3 km are provided every hour for 18 hours, and every 6 hours a 48-hour forecast is run, all at a 3 km resolution. This was perfect for this project, since Dark Sky provided a minute-by-minute forecast for 1 hour, which can be loosely approximated using the 15-minute HRRR forecasts.

#### GFS
The Global Forecast System [(GFS)](https://www.ncdc.noaa.gov/data-access/model-data/model-datasets/global-forcast-system-gfs) is NOAA's global weather model. Running with a resolution of about 30 km (0.25 degrees), the GFS model provides hourly forecasts out of 120 hours, and 3-hour forecasts out to 240 hours. Here, GFS data is used for anywhere in the world not covered by the HRRR model, and for all results past 48 hours. 

The GFS model also underpins the Global Ensemble Forecast System [(GEFS)](https://www.ncdc.noaa.gov/data-access/model-data/model-datasets/global-ensemble-forecast-system-gefs), which is the 30-member ensemble (the website says 21, but there are 30 data files) version of the GFS. This means that 30 different "versions" of the model are run, each with slightly different starting assumptions. The API uses the GEFS to get precipitation type, quantity, and probability, since it seemed like the most accurate way of determining this. I have no idea how Dark Sky did it, and I am very open to feedback about other ways it could be assigned, since getting the precipitation probability number turned out to be one of the most complex parts of the entire setup! 

#### AIGFS / AIGEFS
The AI Global Forecast System [(AIGFS)](https://www.emc.ncep.noaa.gov/emc/pages/numerical_forecast_systems/gfs.php) and AI Global Ensemble Forecast System [(AIGEFS)](https://www.emc.ncep.noaa.gov/emc/pages/numerical_forecast_systems/gefs.php) are NOAA's machine-learning-based global weather prediction models. Built using deep learning techniques trained on decades of reanalysis and operational data, these models provide competitive global forecasts at reduced computational cost.

!!! info "Availability"
    AIGFS/AIGEFS is only available when enabled via a specific query parameter and may not be present for all forecast requests.

#### GEFS
The Global Ensemble Forecast System [(GEFS)](https://www.ncei.noaa.gov/products/weather-climate-models/global-ensemble-forecast) is the ensemble version of NOAA's GFS model. By running different variations parameters and inputs, 30 different versions of this model are run at the same time, providing 3-hour forecasts out to 240 hours. The API uses the GEFS to get precipitation type, quantity, and probability, since it seemed like the most accurate way of determining this. I have no idea how Dark Sky did it, and I am very open to feedback about other ways it could be assigned, since getting the precipitation probability number turned out to be one of the most complex parts of the entire setup! 

### ECMWF

#### ECMWF IFS
The European Centre for Medium-Range Weather Forecasts Integrated Forecasting System [(ECMWF IFS)](https://www.ecmwf.int/en/forecasts/documentation-and-support/changes-ecmwf-model) is a global numerical weather prediction model used for medium-range to long-range atmospheric forecasting. It combines a spectral atmospheric model, an ocean model, and advanced data assimilation techniques to produce some of the most accurate weather forecasts in the world. Probability results are also included from the Ensemble version of this forecast.

The ECMWF IFS underpins many operational forecasting systems worldwide, serving as a benchmark for global models due to its strong performance in forecast skill, particularly for medium-range (3–10 days) predictions and ensemble probabilistic guidance.

#### ECMWF AIFS
The ECMWF Artificial Intelligence/Integrated Forecasting System [(ECMWF AIFS)](https://www.ecmwf.int/en/about/media-centre/aifs-blog) is a machine-learning-based global weather model developed by ECMWF. Trained on ERA5 reanalysis and IFS operational data, AIFS produces deterministic medium-range forecasts at competitive accuracy to the IFS at a fraction of the computational cost.

!!! info "Availability"
    ECMWF AIFS is only available when enabled via a specific query parameter and may not be present for all forecast requests.

### ERA5
To provide historic weather data, the [Google European Reanalysis 5 Dataset](https://console.cloud.google.com/marketplace/product/bigquery-public-data/arco-era5) is used, specifically their `full_37-1h-0p25deg-chunk-1.zarr-v3` product. Details on the Google implementation are available in [their repository](https://github.com/google-research/arco-era5). In the medium term, I'll be exploring adding a local copy of this repository, which would significantly improve performance.

!!! info "Historical requests in 2.10.1"
    Starting in version 2.10.1, [URMA](#urma) will be used as the source for short-term historical requests less than 10 days old within the North America domain.

### CMC

#### HRDPS
The High Resolution Deterministic Prediction System (HRDPS) is maintained by Environment and Climate Change Canada (ECCC). It carries out detailed physics calculations to provide high-resolution deterministic forecasts of atmospheric elements—such as temperature, precipitation, cloud cover, and wind—across most of Canada at a horizontal resolution of about 2.5 km. Operating out to 48 hours, the HRDPS runs up to four times daily, providing localized, high-fidelity regional weather data.

#### REPS
The Regional Ensemble Prediction System ([REPS](https://eccc-msc.github.io/open-data/msc-data/nwp_reps/readme_reps_en/)) is ECCC's regional probabilistic prediction system. Covering Canada and the United States at a 10 km resolution, REPS runs four times daily out to 3 days. It generates forecasts using a control member alongside 20 perturbed ensemble members (incorporating initial/boundary conditions and physical tendency perturbations) to model atmospheric uncertainty and deliver robust probabilistic weather insights.

#### GDPS
The Global Deterministic Prediction System ([GDPS](https://eccc-msc.github.io/open-data/msc-data/nwp_gdps/readme_gdps_en/)) is Canada's primary global numerical weather prediction system, operated by ECCC. Utilizing a coupled atmosphere (GEM), ocean, and sea ice (NEMO-CICE) framework, the GDPS provides global deterministic forecasts at a ~15 km resolution out to 10 days. Running twice daily, it supplies large-scale global meteorological guidance and boundary conditions that feed into regional and high-resolution Canadian modeling pipelines.

#### GEPS
The Global Ensemble Prediction System ([GEPS](https://eccc-msc.github.io/open-data/msc-data/nwp_geps/readme_geps_en/)) is ECCC's global ensemble model, designed to estimate forecast uncertainties driven by the chaotic behavior of the atmosphere. Running twice daily, the GEPS produces global probabilistic forecasts out to 16 days (and up to 39 days twice weekly) using a control member and 20 ensemble members perturbed via stochastic parameter methods. It provides widespread probabilistic guidance on temperature, precipitation, wind, and humidity.

### RAQDPS
[Regional Air Quality Deterministic Prediction System](https://eccc-msc.github.io/open-data/msc-data/nwp_raqdps/readme_raqdps_en/) is maintained by Environment and Climate Change Canada (ECCC) and provides high-resolution regional chemical weather forecasts over North America. It runs twice daily, offering hourly forecasts at a 10 km resolution for up to 72 hours. This model is highly effective for projects needing to track the localized transport, diffusion, and chemical transformation of surface pollutants-specifically ground-level Ozone (O<sub>3</sub>), Nitrogen Dioxide (NO<sub>2</sub>), and fine particulate matter (PM<sub>2.5</sub>)-making it a great fit for calculating regional Air Quality Health Indices (AQHI) or tracking active wildfire smoke plumes.

### DWD

#### DWD MOSMIX
Deutscher Wetterdienst Model Output Statistics-MIX [(DWD MOSMIX)](https://www.dwd.de/EN/ourservices/met_application_mosmix/met_application_mosmix.html;jsessionid=B502689E741CA864089DA8955635E33B.live21064) is a statistically post-processed forecast product produced by the German Weather Service. Rather than a single numerical model, MOSMIX blends output from several global and regional models and applies bias corrections based on historical station observations. The result is high-quality point forecasts optimized for specific locations.

MOSMIX provides hourly forecasts for thousands of stations worldwide, though not all parameters are available at every station. Here, MOSMIX data is used wherever it is available, offering refined, observation-tuned guidance—particularly strong within Europe, where DWD’s station network is most comprehensive.

!!! note "Note"
    DWD MOSMIX uses a fairly aggressive filtering algorithm whenever confidence in the data is low or inputs are missing. If the gaps between data points are greater than 6 hours, the variable will be discarded from DWD MOSMIX and a fallback source used instead. 

### FMI

#### SILAM
[System for Integrated modeLling of Atmospheric coMposition](https://silam.fmi.fi) is a global-to-meso-scale dispersion model developed by the Finnish Meteorological Institute (FMI). It provides global coverage at a 20 km resolution, modeling over 100 chemical species and aerosols across the troposphere and stratosphere. Because it utilizes a hybrid Eulerian-Lagrangian approach, SILAM excels at simulating long-range, transboundary transport. It's uniquely suited for projects that need to account for dynamic, natural emissions alongside human ones-such as tracking desert dust storms, sea salt dispersion, global aviation safety risks, or real-time wildland fire emissions on a macro scale.

**Looking for a weather model that's not listed?** Check the [existing model requests](https://github.com/Pirate-Weather/pirateweather/issues?q=is%3Aissue%20state%3Aopen%20label%3A%22new%20source%22) first. If it hasn't already been requested, submit a [new source request](https://github.com/Pirate-Weather/pirateweather/issues/new?template=new_source.yml).

## Forecast element sources

The tables below summarize the [Forecast Source Selection documentation](https://github.com/Pirate-Weather/pirate-weather-code/tree/dev/docs/forecast-source-selection), which describes the API's source-selection rules in detail.

The API selects the first non-missing value for each forecast element and timestamp, rather than choosing one model for an entire response. Sources must cover the requested location, pass freshness checks, and not be excluded by the request. Their data is interpolated to the minute or hourly time grid before selection. A forecast can therefore combine models and fall back to different sources as values become unavailable.

`flags.sources` lists models available to the request; it does not identify the source of each output value. Daily and day/night values aggregate the selected hourly values without a separate model-selection pass. Time-machine requests use a separate historical-source path and do not use the real-time CMC, NBM, HRRR, or AI priorities below.

### Regions and priority modes

| Region | Definition |
| :--- | :--- |
| Canada box | Latitude 41.7 to 83.0 and longitude -141.0 to -52.0. This is a coverage box, not a political-border lookup. |
| North America outside the Canada box | North American coverage outside that box. |
| Global / standard | All other locations. |

All priorities run from highest to lowest. Only sources that cover the request point and supply the requested element are eligible. Regional models such as NBM, HRRR, RTMA-RU, and HRRR SubH are not global fallbacks simply because they appear in a generic ordering. HRRR SubH denotes the sub-hourly HRRR forecast.

Exclude the CMC group with `exclude=cmc` or `exclude=cmcmodels`, or exclude individual models with values such as `exclude=hrdps,gdps,geps,reps`.

`include=aimodels` enables an explicit AI priority mode for all forecast blocks and excludes HRDPS, GDPS, GEPS, and REPS before their grids are read. Supported AI values take precedence over conventional sources, including RTMA-RU, HRRR SubH, and NBM. Conventional sources fill missing or unsupported AI values.

| Region | AI priority |
| :--- | :--- |
| North America, including the Canada box | AIGFS leads deterministic GFS-compatible fields; AIGEFS leads ensemble precipitation fields. Their output is merged into the GFS and GEFS schemas, respectively. |
| Global / standard | ECMWF AIFS leads ECMWF-compatible fields, with its output merged into the ECMWF IFS schema. |

The conventional tables below apply when AI mode is disabled. Dedicated minutely AI priorities are listed separately. A "GFS-compatible source" includes AIGFS values merged into that schema when AI mode is enabled.

### Currently

For most current surface elements, the selector uses the following regional order, filtered to sources that supply the requested field.

| Region | Priority for compatible surface elements |
| :--- | :--- |
| Canada box | RTMA-RU > HRRR SubH > HRDPS > GDPS > NBM > HRRR > ECMWF IFS > GFS > DWD MOSMIX > ERA5 |
| North America outside the Canada box | RTMA-RU > HRRR SubH > NBM > HRRR > ECMWF IFS > GFS > GDPS > DWD MOSMIX > ERA5 > HRDPS |
| Global / standard | RTMA-RU > HRRR SubH > NBM > HRRR > DWD MOSMIX > ECMWF IFS > GFS > GDPS > ERA5 > HRDPS |

Current `precipIntensity`, `precipProbability`, `precipIntensityError`, and `precipType` are copied from the first minute of the minutely block and use the minutely priorities below.

| Parameter | Dedicated source logic |
| :--- | :--- |
| uvIndex | GFS-compatible source > ERA5 |
| ozone | GFS-compatible source > ERA5 |
| nearestStormBearing, nearestStormDistance | GFS-compatible source |
| smoke | HRRR > SILAM |
| feelsLike | NBM > GFS-compatible source |
| fireIndex | Derived from temperature, humidity, and windSpeed |

### Minutely

These priorities also supply the current precipitation fields.

#### Conventional mode in the Canada box

| Parameter | Priority |
| :--- | :--- |
| precipIntensity | HRRR SubH > NBM > DWD MOSMIX > ECMWF IFS > GEFS > GFS > GDPS > GEPS > ERA5 |
| precipType | HRRR SubH > NBM > ECMWF IFS > GFS > DWD MOSMIX > GEFS > GDPS > GEPS > ERA5 |
| precipProbability | REPS > GEPS > NBM > ECMWF IFS > GEFS > ERA5 |
| precipIntensityError | REPS > ECMWF IFS > GEFS > GEPS |

HRRR SubH leads conventional intensity and type wherever it is available, followed by NBM. REPS leads Canadian probability and error; HRDPS and GDPS do not provide precipitation probability.

#### Conventional mode outside the Canada box

| Parameter | North America outside the Canada box | Global / standard |
| :--- | :--- | :--- |
| precipIntensity | HRRR SubH > NBM > DWD MOSMIX > ECMWF IFS > GEFS > GFS > GDPS > GEPS > ERA5 | HRRR SubH > NBM > DWD MOSMIX > ECMWF IFS > GEFS > GFS > GDPS > GEPS > ERA5 |
| precipType | HRRR SubH > NBM > ECMWF IFS > GFS > DWD MOSMIX > GEFS > GDPS > GEPS > ERA5 | HRRR SubH > NBM > DWD MOSMIX > ECMWF IFS > GFS > GEFS > GDPS > GEPS > ERA5 |
| precipProbability | NBM > ECMWF IFS > GEFS > GEPS > ERA5 | NBM > ECMWF IFS > GEFS > GEPS > ERA5 |
| precipIntensityError | ECMWF IFS > GEFS > GEPS | ECMWF IFS > GEFS > GEPS |

GDPS and GEPS are late minutely fallbacks outside the Canada box, after the GFS/GEFS family.

#### AI mode

| Region | precipIntensity and precipType | precipProbability and precipIntensityError |
| :--- | :--- | :--- |
| North America, including the Canada box | AIGEFS > AIGFS > conventional fallback | AIGEFS > ECMWF IFS > NBM > conventional fallback |
| Global / standard | ECMWF AIFS > conventional fallback | ECMWF AIFS > conventional fallback |

AI models lead for every minutely element they support. CMC sources are not eligible in this mode.

### Hourly / Daily / Day/Night

Most hourly weather elements use the regional order below, filtered to compatible sources. For example, REPS and GEPS are skipped for temperature because they supply ensemble precipitation fields. Daily and day/night output aggregates the selected hourly values.

| Region | Conventional priority for compatible elements |
| :--- | :--- |
| Canada box | HRDPS > REPS > GDPS > GEPS > NBM > HRRR > ECMWF IFS > GFS > GEFS > DWD MOSMIX > ERA5 |
| North America outside the Canada box | NBM > HRRR > ECMWF IFS > GFS > GEFS > GDPS > GEPS > DWD MOSMIX > ERA5 > HRDPS > REPS |
| Global / standard | NBM > HRRR > DWD MOSMIX > ECMWF IFS > GFS > GEFS > GDPS > GEPS > ERA5 > HRDPS > REPS |

#### Precipitation in the Canada box, conventional mode

Hourly precipitation uses separate stacks for intensity, probability, type, accumulation, and error.

| Parameter | Effective priority |
| :--- | :--- |
| precipIntensity | HRDPS > GDPS > NBM > HRRR > ECMWF IFS > GEFS > GFS > DWD MOSMIX > ERA5 |
| precipProbability | REPS > GEPS > NBM > ECMWF IFS > GEFS > ERA5 |
| precipType | REPS > GEPS > HRDPS > GDPS > NBM > HRRR > ECMWF IFS > GEFS > GFS > DWD MOSMIX > ERA5 |
| Precipitation accumulation | HRDPS > REPS > GDPS > GEPS > NBM > HRRR > ECMWF IFS > GFS > GEFS > DWD MOSMIX > ERA5 |
| precipIntensityError | ECMWF IFS > GEFS > GEPS > REPS |

#### Precipitation outside the Canada box, conventional mode

For North America outside the Canada box, NBM and HRRR lead, followed by ECMWF IFS, GFS/GEFS, GDPS/GEPS, and global fallbacks, subject to each element's source coverage. For global locations, a valid DWD MOSMIX station forecast is considered before ECMWF IFS. GDPS and GEPS follow GFS/GEFS and precede lower-priority sources for the fields they support. See the linked [source-selection documentation](https://github.com/Pirate-Weather/pirate-weather-code/tree/dev/docs/forecast-source-selection#hourly-daily-and-daynight-precipitation) for the precipitation-specific rules.

#### Element-coverage exceptions

These hourly elements use dedicated source sets instead of the full generic regional stack.

| Parameter | Source logic |
| :--- | :--- |
| uvIndex | GFS-compatible source > HRDPS > GDPS > ERA5 |
| ozone | GFS-compatible source > GDPS > ERA5 |
| visibility | Regional stack filtered to NBM, HRRR, DWD MOSMIX, GFS-compatible source, and ERA5 |
| nearestStormBearing, nearestStormDistance | GFS-compatible source |
| feelsLike | NBM > GFS-compatible source |
| cape | NBM > HRRR > HRDPS > GDPS > GFS-compatible source > ERA5 |
| smoke | HRRR, with SILAM used for air-quality detail where applicable |
| fireIndex | Derived from temperature, humidity, and windSpeed |

### Air Quality

| Parameter | Priority |
| :--- | :--- |
| airQualityIndex | RAQDPS > SILAM |
| coConcentration | SILAM |
| no2Concentration | RAQDPS > SILAM |
| ozoneConcentration | RAQDPS > SILAM |
| so2Concentration | RAQDPS > SILAM |
| pm10 | RAQDPS > SILAM |
| pm25 | RAQDPS > SILAM |

## Data Pipeline

### Trigger
Forecasts are saved from NOAA onto the [AWS Public Cloud](https://registry.opendata.aws/collab/noaa/) into three buckets for the [HRRR](https://registry.opendata.aws/noaa-hrrr-pds/), [GFS](https://registry.opendata.aws/noaa-gfs-bdp-pds/), [GEFS](https://registry.opendata.aws/noaa-gefs/), [RTMA-RU](https://registry.opendata.aws/noaa-rtma/) and [ECMWF IFS](https://registry.opendata.aws/ecmwf-forecasts/) models. Since I couldn't find a good way to trigger processing tasks based on S3 events in a public bucket, the ingest system relies on timed events scheduled through [AWS EventBridge Rules](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-create-rule-schedule.html), with the timings shown in the table below:

| Model                | Run Times (UTC) | Delay | Ingest Times (UTC)    |
|----------------------|-----------------|-------|-----------------------|
| GFS                  | 0,6,12,18       | 5:00  | 5,11,17,23            |
| GEFS                 | 0,6,12,18       | 7:00  | 7,13,19,1             |
| NBM                  | 0-24            | 1:45  | 1:45-00:45            |
| HRRR- 48h            | 0,6,12,18       | 2:30  | 2:30,8:30,14:30,20:30 |
| HRRR- 18h/ SubHourly | 0-24            | 1:45  | 1:45-00:45        	 |
| RTMA-RU              | 0-24            | 0:25  | :25,:40,:55,:10       |
| URMA                 | 0-24            | 0:15  | :15 every hour        | 
| ECMWF IFS            | 0,12            | 8:00  | 8,20                  |
| DWD MOSMIX           | 0-24            | 1:00  | 1:00-0:00             |
| HRDPS                | 0,6,12,18       | 4:00  | 4,10,16,22            |
| REPS                 | 0,6,12,18       | 4:00  | 4,10,16,22            |
| GDPS                 | 0,12            | 5:00  | 5,17                  |
| GEPS                 | 0,12            | 7:00  | 7,19                  |
| ECMWF AIFS           | 0,6,12,18       | 8:00  | 8,16,20,2             |
| AIGFS                | 0,6,12,18       | 5:00  | 5,11,17,23            |
| RAQDPS               | 0,12            | 4:15  | 4:15,16:15            |
| SILAM                | 0               | 7:00  | 7                     |
