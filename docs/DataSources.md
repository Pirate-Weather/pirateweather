# API Docs
This page serves as the documentation for the underlying data source algorithm for the Pirate Weather API- in sort, it explains which parameter comes from where. Since the goal of this API to to provide raw model data with as little processing as possible, results from the API should very closely match the model described in this document, with some minor differences due to interpolation. 

## Data sources
Several models are used to produce the forecast. Most are hosted on [AWS's Open Data Platform](https://registry.opendata.aws/collab/noaa/), and the fantastic [Herbie package](https://github.com/blaylockbk/Herbie) is used to download and perform initial processing for many of them.    

#### RTMA Rapid Update
The Real-Time Mesoscale Analysis Rapid Update [(RTMA-RU)](https://emc.ncep.noaa.gov/emc/pages/numerical_forecast_systems/rtma.php) provides real time analysis for the continental US and parts of Canada. The model runs every 15-minutes and combines the HRRR first guess with observations from satellites and station observations.

RTMA-RU blends a rapidly updating HRRR first guess with whatever observations are available at each 15-minute cycle, the analyses can sometimes show noticeable jumps from one update to the next. Changes in observation availability, timing, or quality—as well as shifts in how strongly the system weights those observations relative to the HRRR first guess—can cause sudden increases or decreases in the analyzed values. These cycle-to-cycle fluctuations are a normal artifact of the rapid-update data assimilation process, and they can appear in any variable, especially in areas with sparse or intermittent observational coverage.

#### NBM
The National Blend of Models [(NBM)](https://vlab.noaa.gov/web/mdl/nbm) is a calibrated blend of both NOAA and non-NOAA weather models from around the world. Running every hour for about 7 days, the NBM produces a forecast that aims to leverage strengths from each of the source models, as well as providing some probabilistic forecasts. For most weather elements in the US and Canada, this is the primary source. 

#### HRRR
The High Resolution Rapid Refresh [(HRRR)](https://rapidrefresh.noaa.gov/hrrr/) provides forecasts over all of the continental US, as well as most of the Canadian population. 15-minute forecasts every 3 km are provided every hour for 18 hours, and every 6 hours a 48-hour forecast is run, all at a 3 km resolution. This was perfect for this project, since Dark Sky provided a minute-by-minute forecast for 1 hour, which can be loosely approximated using the 15-minute HRRR forecasts.

#### GFS
The Global Forecast System [(GFS)](https://www.ncdc.noaa.gov/data-access/model-data/model-datasets/global-forcast-system-gfs) is NOAA's global weather model. Running with a resolution of about 30 km (0.25 degrees), the GFS model provides hourly forecasts out of 120 hours, and 3-hour forecasts out to 240 hours. Here, GFS data is used for anywhere in the world not covered by the HRRR model, and for all results past 48 hours. 

The GFS model also underpins the Global Ensemble Forecast System [(GEFS)](https://www.ncdc.noaa.gov/data-access/model-data/model-datasets/global-ensemble-forecast-system-gefs), which is the 30-member ensemble (the website says 21, but there are 30 data files) version of the GFS. This means that 30 different "versions" of the model are run, each with slightly different starting assumptions. The API uses the GEFS to get precipitation type, quantity, and probability, since it seemed like the most accurate way of determining this. I have no idea how Dark Sky did it, and I am very open to feedback about other ways it could be assigned, since getting the precipitation probability number turned out to be one of the most complex parts of the entire setup! 

#### GEFS
The Global Ensemble Forecast System [(GEFS)](https://www.ncei.noaa.gov/products/weather-climate-models/global-ensemble-forecast) is the ensemble version of NOAA's GFS model. By running different variations parameters and inputs, 30 different versions of this model are run at the same time, providing 3-hour forecasts out to 240 hours. The API uses the GEFS to get precipitation type, quantity, and probability, since it seemed like the most accurate way of determining this. I have no idea how Dark Sky did it, and I am very open to feedback about other ways it could be assigned, since getting the precipitation probability number turned out to be one of the most complex parts of the entire setup! 

#### ECMWF IFS
The European Centre for Medium-Range Weather Forecasts Integrated Forecasting System [(ECMWF IFS)](https://www.ecmwf.int/en/forecasts/documentation-and-support/changes-ecmwf-model) is a global numerical weather prediction model used for medium-range to long-range atmospheric forecasting. It combines a spectral atmospheric model, an ocean model, and advanced data assimilation techniques to produce some of the most accurate weather forecasts in the world. Probability results are also included from the Ensemble version of this forecast.

The ECMWF IFS underpins many operational forecasting systems worldwide, serving as a benchmark for global models due to its strong performance in forecast skill, particularly for medium-range (3–10 days) predictions and ensemble probabilistic guidance.

#### ECMWF AIFS
The ECMWF Artificial Intelligence/Integrated Forecasting System [(ECMWF AIFS)](https://www.ecmwf.int/en/about/media-centre/aifs-blog) is a machine-learning-based global weather model developed by ECMWF. Trained on ERA5 reanalysis and IFS operational data, AIFS produces deterministic medium-range forecasts at competitive accuracy to the IFS at a fraction of the computational cost.

!!! info "Availability"
    ECMWF AIFS is only available when enabled via a specific query parameter and may not be present for all forecast requests.

#### AIGFS / AIGEFS
The AI Global Forecast System [(AIGFS)](https://www.emc.ncep.noaa.gov/emc/pages/numerical_forecast_systems/gfs.php) and AI Global Ensemble Forecast System [(AIGEFS)](https://www.emc.ncep.noaa.gov/emc/pages/numerical_forecast_systems/gefs.php) are NOAA's machine-learning-based global weather prediction models. Built using deep learning techniques trained on decades of reanalysis and operational data, these models provide competitive global forecasts at reduced computational cost.

!!! info "Availability"
    AIGFS/AIGEFS is only available when enabled via a specific query parameter and may not be present for all forecast requests.

#### DWD MOSMIX
Deutscher Wetterdienst Model Output Statistics-MIX [(DWD MOSMIX)](https://www.dwd.de/EN/ourservices/met_application_mosmix/met_application_mosmix.html;jsessionid=B502689E741CA864089DA8955635E33B.live21064) is a statistically post-processed forecast product produced by the German Weather Service. Rather than a single numerical model, MOSMIX blends output from several global and regional models and applies bias corrections based on historical station observations. The result is high-quality point forecasts optimized for specific locations.

MOSMIX provides hourly forecasts for thousands of stations worldwide, though not all parameters are available at every station. Here, MOSMIX data is used wherever it is available, offering refined, observation-tuned guidance—particularly strong within Europe, where DWD’s station network is most comprehensive.

!!! note "Note"
    DWD MOSMIX uses a fairly aggressive filtering algorithm whenever confidence in the data is low or inputs are missing. If the gaps between data points are greater than 6 hours, the variable will be discarded from DWD MOSMIX and a fallback source used instead. 

### ERA5
To provide historic weather data, the [Google European Reanalysis 5 Dataset](https://console.cloud.google.com/marketplace/product/bigquery-public-data/arco-era5) is used, specifically their `full_37-1h-0p25deg-chunk-1.zarr-v3` product. Details on the Google implementation are available in [their repository](https://github.com/google-research/arco-era5). In the medium term, I'll be exploring adding a local copy of this repository, which would significantly improve performance.

## Forecast element sources
Every Pirate Weather forecast element for each time block (`currently`, `minutely`, `hourly`, or `daily`) is listed below, along with the ordered fallback chain for each region. Fallback sources are used if model data is intentionally excluded, the request point is outside of the primary model coverage area, or if there is some sort of data interruption.

For most weather elements the general approach is: NBM → HRRR → ECMWF IFS → GEFS → GFS → DWD MOSMIX. Where AI models are available they slot in above ECMWF IFS (AIGFS/AIGEFS in North America) or above DWD MOSMIX (ECMWF AIFS globally), but only for the specific parameters each model provides. For `currently` and `minutely` blocks, sub-hourly HRRR and RTMA-RU data are preferred when available.

### Currently

#### North America
| Parameter | Priority |
| :--- | :--- |
| apparentTemperature | RTMA-RU > HRRR_SubH > NBM > ECMWF IFS > GFS > DWD MOSMIX |
| cape | HRRR_SubH > NBM > GFS |
| cloudCover | RTMA-RU > NBM > HRRR > ECMWF IFS > GFS > DWD MOSMIX |
| currentDayIce | NBM > HRRR > AIGEFS > ECMWF IFS > GEFS > GFS |
| currentDayLiquid | NBM > HRRR > AIGEFS > ECMWF IFS > GEFS > GFS |
| currentDaySnow | NBM > HRRR > AIGEFS > ECMWF IFS > GEFS > GFS |
| dewPoint | RTMA-RU > HRRR_SubH > NBM > ECMWF IFS > GFS > DWD MOSMIX |
| feelsLike | NBM > GFS |
| fireIndex | Derived from temperature, humidity, and windSpeed |
| humidity | RTMA-RU > HRRR > NBM > ECMWF IFS > GFS > DWD MOSMIX |
| nearestStormBearing | GFS |
| nearestStormDistance | GFS |
| ozone | GFS |
| precipIntensity | HRRR_SubH > NBM > AIGEFS > ECMWF IFS > GEFS > DWD MOSMIX |
| precipIntensityError | AIGEFS > ECMWF IFS > GEFS |
| precipProbability | NBM > AIGEFS > ECMWF IFS > GEFS |
| precipType | HRRR_SubH > NBM > AIGEFS > ECMWF IFS > GEFS > DWD MOSMIX |
| pressure | HRRR > AIGFS > ECMWF IFS > GFS > DWD MOSMIX |
| smoke | HRRR |
| solar | HRRR_SubH > NBM > GFS > DWD MOSMIX |
| temperature | RTMA-RU > HRRR_SubH > NBM > AIGFS > ECMWF IFS > GFS > DWD MOSMIX |
| uvIndex | GFS |
| visibility | RTMA-RU > HRRR_SubH > NBM > GFS > DWD MOSMIX |
| windBearing | RTMA-RU > HRRR_SubH > NBM > AIGFS > ECMWF IFS > GFS > DWD MOSMIX |
| windGust | RTMA-RU > HRRR_SubH > NBM > GFS > DWD MOSMIX |
| windSpeed | RTMA-RU > HRRR_SubH > NBM > AIGFS > ECMWF IFS > GFS > DWD MOSMIX |

#### Global / Standard
| Parameter | Priority |
| :--- | :--- |
| apparentTemperature | RTMA-RU > HRRR_SubH > NBM > ECMWF AIFS > DWD MOSMIX > ECMWF IFS > GFS |
| cape | HRRR_SubH > NBM > GFS |
| cloudCover | RTMA-RU > NBM > HRRR > ECMWF AIFS > DWD MOSMIX > ECMWF IFS > GFS |
| currentDayIce | NBM > HRRR > ECMWF AIFS > ECMWF IFS > GEFS > GFS |
| currentDayLiquid | NBM > HRRR > ECMWF AIFS > ECMWF IFS > GEFS > GFS |
| currentDaySnow | NBM > HRRR > ECMWF AIFS > ECMWF IFS > GEFS > GFS |
| dewPoint | RTMA-RU > HRRR_SubH > NBM > DWD MOSMIX > GFS |
| feelsLike | NBM > GFS |
| fireIndex | Derived from temperature, humidity, and windSpeed |
| humidity | RTMA-RU > HRRR > NBM > ECMWF AIFS > DWD MOSMIX > ECMWF IFS > GFS |
| nearestStormBearing | GFS |
| nearestStormDistance | GFS |
| ozone | GFS |
| precipIntensity | HRRR_SubH > NBM > ECMWF AIFS > DWD MOSMIX > ECMWF IFS > GEFS |
| precipIntensityError | ECMWF AIFS > ECMWF IFS > GEFS |
| precipProbability | NBM > ECMWF AIFS > ECMWF IFS > GEFS |
| precipType | HRRR_SubH > NBM > ECMWF AIFS > DWD MOSMIX > ECMWF IFS > GEFS |
| pressure | HRRR > ECMWF AIFS > DWD MOSMIX > ECMWF IFS > GFS |
| smoke | HRRR |
| solar | HRRR_SubH > NBM > DWD MOSMIX > GFS |
| temperature | RTMA-RU > HRRR_SubH > NBM > ECMWF AIFS > DWD MOSMIX > ECMWF IFS > GFS |
| uvIndex | GFS |
| visibility | RTMA-RU > HRRR_SubH > NBM > DWD MOSMIX > GFS |
| windBearing | RTMA-RU > HRRR_SubH > NBM > ECMWF AIFS > DWD MOSMIX > ECMWF IFS > GFS |
| windGust | RTMA-RU > HRRR_SubH > NBM > DWD MOSMIX > GFS |
| windSpeed | RTMA-RU > HRRR_SubH > NBM > ECMWF AIFS > DWD MOSMIX > ECMWF IFS > GFS |

### Minutely

#### North America
| Parameter | Priority |
| :--- | :--- |
| precipIntensity | HRRR_SubH > NBM > AIGEFS > ECMWF IFS > GEFS > DWD MOSMIX |
| precipIntensityError | AIGEFS > ECMWF IFS > GEFS |
| precipProbability | NBM > AIGEFS > ECMWF IFS > GEFS |
| precipType | HRRR_SubH > NBM > AIGEFS > ECMWF IFS > GEFS > DWD MOSMIX |

#### Global / Standard
| Parameter | Priority |
| :--- | :--- |
| precipIntensity | HRRR_SubH > NBM > ECMWF AIFS > DWD MOSMIX > ECMWF IFS > GEFS |
| precipIntensityError | ECMWF AIFS > ECMWF IFS > GEFS |
| precipProbability | NBM > ECMWF AIFS > ECMWF IFS > GEFS |
| precipType | HRRR_SubH > NBM > ECMWF AIFS > DWD MOSMIX > ECMWF IFS > GEFS |

### Hourly / Daily / Day/Night

#### North America
| Parameter | Priority |
| :--- | :--- |
| apparentTemperature | NBM > HRRR > ECMWF IFS > GFS > DWD MOSMIX |
| cape | NBM > HRRR > GFS |
| cloudCover | NBM > HRRR > ECMWF IFS > GFS |
| dewPoint | NBM > HRRR > ECMWF IFS > GFS |
| feelsLike | NBM > GFS |
| fireIndex | Derived from temperature, humidity, and windSpeed |
| humidity | NBM > HRRR > ECMWF IFS > GFS > DWD MOSMIX |
| iceAccumulation | NBM > HRRR > AIGEFS > ECMWF IFS > GEFS > GFS > DWD MOSMIX |
| liquidAccumulation | NBM > HRRR > AIGEFS > ECMWF IFS > GEFS > GFS > DWD MOSMIX |
| nearestStormBearing | NBM > HRRR > ECMWF IFS > GEFS > GFS > DWD MOSMIX |
| nearestStormDistance | GFS |
| ozone | GFS |
| precipAccumulation | NBM > HRRR > AIGEFS > ECMWF IFS > GEFS > GFS > DWD MOSMIX |
| precipIntensity | NBM > HRRR > AIGEFS > ECMWF IFS > GEFS > DWD MOSMIX |
| precipIntensityError | AIGEFS > ECMWF IFS > GEFS |
| precipProbability | NBM > AIGEFS > ECMWF IFS > GEFS |
| precipType | NBM > HRRR > AIGEFS > ECMWF IFS > GEFS > DWD MOSMIX |
| pressure | HRRR > AIGFS > ECMWF IFS > GFS > DWD MOSMIX |
| smoke | HRRR |
| snowAccumulation | NBM > HRRR > AIGEFS > ECMWF IFS > GEFS > GFS > DWD MOSMIX |
| solar | NBM > HRRR > GFS > DWD MOSMIX |
| temperature | NBM > HRRR > AIGFS > ECMWF IFS > GFS > DWD MOSMIX |
| uvIndex | GFS |
| visibility | NBM > HRRR > GFS > DWD MOSMIX |
| windBearing | NBM > HRRR > AIGFS > ECMWF IFS > GFS > DWD MOSMIX |
| windGust | NBM > HRRR > GFS > DWD MOSMIX |
| windSpeed | NBM > HRRR > AIGFS > ECMWF IFS > GFS > DWD MOSMIX |

#### Global / Standard
| Parameter | Priority |
| :--- | :--- |
| apparentTemperature | NBM > HRRR > ECMWF AIFS > DWD MOSMIX > ECMWF IFS > GFS |
| cape | NBM > HRRR > GFS |
| cloudCover | NBM > HRRR > ECMWF AIFS > DWD MOSMIX > ECMWF IFS > GFS |
| dewPoint | NBM > HRRR > DWD MOSMIX > GFS |
| feelsLike | NBM > GFS |
| fireIndex | Derived from temperature, humidity, and windSpeed |
| humidity | NBM > HRRR > ECMWF AIFS > DWD MOSMIX > ECMWF IFS > GFS |
| iceAccumulation | NBM > HRRR > ECMWF AIFS > DWD MOSMIX > ECMWF IFS > GEFS > GFS |
| liquidAccumulation | NBM > HRRR > ECMWF AIFS > DWD MOSMIX > ECMWF IFS > GEFS > GFS |
| nearestStormBearing | NBM > HRRR > DWD MOSMIX > ECMWF IFS > GEFS > GFS |
| nearestStormDistance | GFS |
| ozone | GFS |
| precipAccumulation | NBM > HRRR > ECMWF AIFS > DWD MOSMIX > ECMWF IFS > GEFS > GFS |
| precipIntensity | NBM > HRRR > ECMWF AIFS > DWD MOSMIX > ECMWF IFS > GEFS |
| precipIntensityError | ECMWF AIFS > ECMWF IFS > GEFS |
| precipProbability | NBM > ECMWF AIFS > ECMWF IFS > GEFS |
| precipType | NBM > HRRR > ECMWF AIFS > DWD MOSMIX > ECMWF IFS > GEFS |
| pressure | HRRR > ECMWF AIFS > DWD MOSMIX > ECMWF IFS > GFS |
| smoke | HRRR |
| snowAccumulation | NBM > HRRR > ECMWF AIFS > DWD MOSMIX > ECMWF IFS > GEFS > GFS |
| solar | NBM > HRRR > DWD MOSMIX > GFS |
| temperature | NBM > HRRR > ECMWF AIFS > DWD MOSMIX > ECMWF IFS > GFS |
| uvIndex | GFS |
| visibility | NBM > HRRR > DWD MOSMIX > GFS |
| windBearing | NBM > HRRR > ECMWF AIFS > DWD MOSMIX > ECMWF IFS > GFS |
| windGust | NBM > HRRR > DWD MOSMIX > GFS |
| windSpeed | NBM > HRRR > ECMWF AIFS > DWD MOSMIX > ECMWF IFS > GFS |

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
| ECMWF IFS            | 0,12            | 8:00  | 8,20                  |
| DWD MOSMIX           | 0-24            | 1:00  | 1:00-0:00             |
| ECMWF AIFS           | 0,6,12,18       | 8:00  | 8,16,20,2             |
| AIGFS                | 0,6,12,18       | 5:00  | 5,11,17,23            |
| AIGEFS               | 0,6,12,18       | 7:00  | 7,13,19,1             |
