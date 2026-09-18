# Air Quality

This page documents the air quality fields returned by the Pirate Weather API and provides reference tables for the regional air quality indexes used by each unit system. The index applied depends on the `units` parameter (or the `aqiunits` override), with separate indexes for US, Canadian, UK, and European standards.

### Air Quality Elements

#### airQualityIndex
The air quality index for the requested location. The specific index format used automatically updates depending on the requested units:

- **US / Default:** Uses the [United States Environmental Protection Agency Air Quality Index (AQI)](https://www.airnow.gov/aqi/aqi-basics/).
- **CA:** Uses the [ECCC Air Quality Health Index (AQHI)](https://www.canada.ca/en/environment-climate-change/services/air-quality-health-index/about.html).
- **UK:** Uses the [UK Daily Air Quality Index (DAQI)](https://uk-air.defra.gov.uk/air-pollution/daqi).
- **SI:** Uses the [EU Common Air Quality Index (CAQI)](https://www.airqualitynow.eu/about_indices_definition.php).
- **HK:** (`aqiunits="hk"`): Uses the Hong Kong Air Quality Health Index (AQHI).
- **IE:** (`aqiunits="ie"`): Uses the Ireland Air Quality Index for Health (AQIH).
- **IL:** (`aqiunits="il"`): Uses the Israel Air Quality Health Index (AQHI).
- **ID:** (`aqiunits="id"`): Uses the Indonesia Standard Pollutant Index (ISPU).
- **CN:** (`aqiunits="cn"`): Uses the China National Ambient Air Quality Index (AQI).
- **MY:** (`aqiunits="my"`): Uses the Malaysia Air Pollutant Index (API).
- **VN:** (`aqiunits="vn"`): Uses the Vietnam Air Quality Index (AQI).

*How they are calculated:*
<ul>
<li><strong>US EPA AQI</strong>: Calculated using a 12-hour Nowcast (where the most recent hours are weighted more heavily) for PM<sub>2.5</sub> and PM<sub>10</sub>, an 8-hour average for O<sub>3</sub> and CO, and a 1-hour average for NO<sub>2</sub> and SO<sub>2</sub>. The overall index value matches whichever individual pollutant has the highest score.</li>
<li><strong>ECCC AQHI</strong>: Calculated using a formula based on 3-hour rolling averages of PM<sub>2.5</sub>, O<sub>3</sub>, and NO<sub>2</sub>. Unlike the US index, these three values are combined into a single health risk calculation rather than just taking the maximum.</li>
<li><strong>UK DAQI</strong>: Calculated by assigning a 1–10 band to each of NO<sub>2</sub>, SO<sub>2</sub>, O<sub>3</sub>, PM<sub>2.5</sub>, and PM<sub>10</sub> based on concentration thresholds. The overall index is the maximum band value across all pollutants.</li>
<li><strong>EU EAQI</strong>: Calculated using hourly (1-hour) averages for PM<sub>2.5</sub>, PM<sub>10</sub>, O<sub>3</sub>, NO<sub>2</sub>, and SO<sub>2</sub>. The overall index value represents the maximum value among all four sub-indices.</li>
<li><strong>Hong Kong AQHI</strong>: Calculated using the sum of health risk increments based on 3-hour moving averages of gaseous pollutants (NO<sub>2</sub>, SO<sub>2</sub>, O<sub>3</sub>, CO) and particulate matter (PM2.5, PM10), mapped on a scale of 1 to 10+.</li>
<li><strong>Ireland AQIH</strong>: Calculated using hourly monitoring data across key pollutants (O<sub>3</sub>, NO<sub>2</sub>, PM<sub>2.5</sub>, PM<sub>10</sub>, and SO<sub>2</sub>), categorized into a relative health index scale from 1 (Good) to 10 (Very Poor) based on the highest individual pollutant score. The difference between the Ireland AQIH and the UK DAQI is the Ireland AQIH uses different breakpoints for SO<sub>2</sub>.</li>
<li><strong>Israel AQHI</strong>: Calculated using a scale that combines concentrations of major pollutants (including PM<sub>2.5</sub>, PM<sub>10</sub>, O<sub>3</sub>, NO<sub>2</sub>, and SO<sub>2</sub>). Each pollutant is assigned a sub-index value, and the overall air quality index dictates the overall score. The final AQI value is calculated by subtracting the previous AQI value from 100 meaning that 100 is the highest score and -400 the lowest.</li>
<li><strong>Indonesia ISPU</strong>: Calculated by converting ambient concentrations of key pollutants (PM<sub>2.5, PM<sub>10</sub>, SO<sub>2</sub>, CO, O<sub>3</sub>, and NO<sub>2</sub>) into standardized sub-index values, where the maximum sub-index determines the final ISPU score.</li>
<li><strong>China AQI</strong>: Calculated using individual air quality sub-indices (IAQI) for six standard pollutants (SO<sub>2</sub>, NO<sub>2</sub>, PM<sub>10</sub>, PM<sub>2.5</sub>, CO, and O<sub>3</sub>) based on varying averaging periods (such as 24-hour averages for particles and rolling 8-hour averages for ozone). The maximum IAQI value dictates the overall AQI.</li>
<li><strong>Malaysia API</strong>: Calculated using rolling 24-hour averages for PM<sub>2.5</sub>, PM<sub>10</sub>, CO, SO<sub>2</sub>, NO<sub>2</sub>, and O<sub>3</sub>. Each pollutant is assigned a sub-index value, and the highest sub-index determines the final daily API reading.</li>
<li><strong>Vietnam AQI</strong>: Calculated using individual pollutant sub-indices based on local ambient air quality standards for PM<sub>2.5</sub>, PM<sub>10</sub>, SO<sub>2</sub>, NO<sub>2</sub>, CO, and O<sub>3</sub> over specified averaging periods, with the overall index representing the highest sub-index value.</li>
</ul>

#### airQualityIndexMax
**Only on `daily`**. The maximum air quality index forecasted for the day, represented in the appropriate scale depending on the requested units.

#### airQualityIndexMin
**Only on `daily`**. The minimum air quality index forecasted for the day, represented in the appropriate scale depending on the requested units.

#### coConcentration
The carbon monoxide concentration represented in parts per billion (ppb).

#### no2Concentration
The nitrogen dioxide concentration represented in parts per billion (ppb).

#### ozoneConcentration
The ozone concentration represented in parts per billion (ppb).

#### pm25
The fine particulate matter concentration represented in micrograms per cubic meter (µg/m³).

#### pm10
The coarse particulate matter concentration represented in micrograms per cubic meter (µg/m³).

#### so2Concentration
The sulfur dioxide concentration represented in parts per billion (ppb).

### Index Reference Ranges

Because each regional index uses unique breakpoints, severities, and data scales, use the respective tables below to map UI labels and alert colors based on your query's `units` parameter or the `aqiunits` override parameter.

Each index is shown in a collapsible section below. As more regional indexes are added in the future, this keeps the page manageable — expand only the index that applies to your region.

??? note "US EPA AQI (Default / US Units)"

    Scale ranges from **0 to 500**. 

    | AQI Value | Severity Label | Suggested UI Color |
    | :--- | :--- | :--- |
    | **0 - 50** | Good | Green |
    | **51 - 100** | Moderate | Yellow |
    | **101 - 150** | Unhealthy for Sensitive Groups | Orange |
    | **151 - 200** | Unhealthy | Red |
    | **201 - 300** | Very Unhealthy | Purple |
    | **301 - 500** | Hazardous | Maroon |

??? note "ECCC AQHI (Canada / CA Units)"

    Scale ranges from **1 to 10+**.

    | AQHI Value | Risk Level | Suggested UI Color |
    | :--- | :--- | :--- |
    | **1 - 3** | Low Risk | Blue |
    | **4 - 6** | Moderate Risk | Yellow |
    | **7 - 10** | High Risk | Red |
    | **10+** | Very High Risk | Dark Burgundy |

??? note "UK DAQI (UK Units)"

    Scale ranges from **1 to 10**.

    | DAQI Value | Band | Suggested UI Color |
    | :--- | :--- | :--- |
    | **1 - 3** | Low | Green |
    | **4 - 6** | Moderate | Yellow |
    | **7 - 9** | High | Red |
    | **10** | Very High | Purple |

??? note "EU EAQI (SI Units)"

    Scale ranges from **0 to 100**.

    **Note**: The eaqi field is a normalized 0-100 representation of the European Air Quality Index rather than the official EAQI index. This format was adopted to maintain backward compatibility with earlier versions of the API that returned CAQI values on a 0-100 scale, allowing existing applications to transition to EAQI without changes to their UI thresholds or color mappings.

    | EAQI Value | Index Level | Suggested UI Color |
    | :--- | :--- | :--- |
    | **0 - 20** | Good | Green |
    | **21 - 40** | Fair | Light Green / Yellow-Green |
    | **41 - 60** | Moderate | Yellow |
    | **61 - 80** | Poor | Orange |
    | **81 - 100** | Very poor | Red |

??? note "Hong Kong AQHI (`aqiunits="hk"`)"

    Scale ranges from **1 to 10+**.

    | AQHI Value | Risk Level | Suggested UI Color |
    | :--- | :--- | :--- |
    | **1 - 3** | Low Risk | Green |
    | **4 - 6** | Low Risk | Orange |
    | **7** | High | Red |
    | **8 - 10** | Very high | Brown |
    | **10+** | Serious | Black |

??? note "Ireland AQIH (`aqiunits="ie"`)"

    Scale ranges from **1 to 10**.

    | DAQI Value | Band | Suggested UI Color |
    | :--- | :--- | :--- |
    | **1 - 3** | Low | Green |
    | **4 - 6** | Moderate | Yellow |
    | **7 - 9** | High | Red |
    | **10** | Very High | Purple |

??? note "Israel AQI (`aqiunits="il"`)"

    Scale ranges from **100 to -400**. 

    | AQI Value | Severity Label | Suggested UI Color |
    | :--- | :--- | :--- |
    | **100 - 51** | Good | Green |
    | **50 - 0** | Medium | Yellow |
    | **-1 - -200** | Low | Red |
    | **-201 - -400** | Very low | Brown |

??? note "Indonesia ISPU (`aqiunits="id"`)"

    Scale ranges from **0 to 300**. 

    | AQI Value | Severity Label | Suggested UI Color |
    | :--- | :--- | :--- |
    | **0 - 50** | Good | Green |
    | **51 - 100** | Moderate | Blue |
    | **101 - 200** | Not Healthy | Amber |
    | **201 - 300** | Very unhealhy | Red |
    | **301 - 500** | Dangerous | Black |

??? note "China AQI (`aqiunits="cn"`)"

    Scale ranges from **0 to 500**. 

    | AQI Value | Severity Label | Suggested UI Color |
    | :--- | :--- | :--- |
    | **0 - 50** | Excellent | Green |
    | **51 - 100** | Good | Yellow |
    | **101 - 150** | Lightly polluted | Orange |
    | **151 - 200** | Moderately polluted | Red |
    | **201 - 300** | Heavily polluted | Purple |
    | **301 - 500** | Severely polluted | Maroon |

??? note "Malaysia API (`aqiunits="my"`)"

    Scale ranges from **0 to 500**. 

    | AQI Value | Severity Label | Suggested UI Color |
    | :--- | :--- | :--- |
    | **0 - 50** | Good | Blue |
    | **51 - 100** | Moderate | Green |
    | **101 - 200** | Unhealthy | Yellow |
    | **201 - 300** | Very unhealthy | Orange |
    | **301 - 500** | Hazardous | Red |

??? note "Vietnam AQI (`aqiunits="vn"`)"

    Scale ranges from **0 to 500**. 

    | AQI Value | Severity Label | Suggested UI Color |
    | :--- | :--- | :--- |
    | **0 - 50** | Good | Green |
    | **51 - 100** | Moderate | Yellow |
    | **101 - 150** | Unhealthy for Sensitive Groups | Orange |
    | **151 - 200** | Unhealthy | Red |
    | **201 - 300** | Very Unhealthy | Purple |
    | **301 - 500** | Hazardous | Maroon |