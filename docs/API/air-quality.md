### Air Quality Elements

#### airQualityIndex
The air quality index for the requested location. The specific index format used automatically updates depending on the requested units:

- **US / Default:** Uses the [United States Environmental Protection Agency Air Quality Index (AQI)](https://www.airnow.gov/aqi/aqi-basics/).
- **CA:** Uses the [ECCC Air Quality Health Index (AQHI)](https://www.canada.ca/en/environment-climate-change/services/air-quality-health-index/about.html).
- **UK:** Uses the [UK Daily Air Quality Index (DAQI)](https://uk-air.defra.gov.uk/air-pollution/daqi).
- **SI:** Uses the [EU Common Air Quality Index (CAQI)](https://www.airqualitynow.eu/about_indices_definition.php).

*How they are calculated:*
<ul>
<li><strong>US EPA AQI</strong>: Calculated using a 12-hour Nowcast (where the most recent hours are weighted more heavily) for PM<sub>2.5</sub> and PM<sub>10</sub>, an 8-hour average for O<sub>3</sub> and CO, and a 1-hour average for NO<sub>2</sub> and SO<sub>2</sub>. The overall index value matches whichever individual pollutant has the highest score.</li>
<li><strong>ECCC AQHI</strong>: Calculated using a formula based on 3-hour rolling averages of PM<sub>2.5</sub>, O<sub>3</sub>, and NO<sub>2</sub>. Unlike the US index, these three values are combined into a single health risk calculation rather than just taking the maximum.</li>
<li><strong>UK DAQI</strong>: Calculated by assigning a 1–10 band to each of NO<sub>2</sub>, SO<sub>2</sub>, O<sub>3</sub>, PM<sub>2.5</sub>, and PM<sub>10</sub> based on concentration thresholds. The overall index is the maximum band value across all pollutants.</li>
<li><strong>EU EAQI</strong>: Calculated using hourly (1-hour) averages for PM<sub>2.5</sub>, PM<sub>10</sub>, O<sub>3</sub>, NO<sub>2</sub>, and SO<sub>2</sub>. The overall index value represents the maximum value among all four sub-indices.</li>
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
    | **10** | Very High Risk | Dark Burgundy |

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
