# Roadmap
1. Weather maps from new Zarr datafiles.
2. Add in alerts for Canada/ EU/ other.
3. Add in a Air Quality Index as suggested in [issue #92](https://github.com/Pirate-Weather/pirateweather/issues/92)
4. Add source data.
	* [ECMWF](https://herbie.readthedocs.io/en/stable/gallery/ecmwf_models/ecmwf.html)
		* This is already being ingested, so underlying data is there
	* Canadian models ([HRDPS](https://herbie.readthedocs.io/en/stable/gallery/eccc_models/hrdps.html), [GDPS](https://herbie.readthedocs.io/en/stable/gallery/eccc_models/gdps.html) and [RDPS](https://herbie.readthedocs.io/en/stable/gallery/eccc_models/rdps.html))
	* [NBM-Alaska/ Hawaii/ Puerto Rico/ Guam](https://herbie.readthedocs.io/en/stable/gallery/noaa_models/nbm.html)
	* [RTMA/ URMA](https://herbie.readthedocs.io/en/stable/gallery/noaa_models/rtma-urma.html)
	* [NOAA GraphCast](https://herbie.readthedocs.io/en/stable/gallery/noaa_models/gfs.html#GFS-GraphCast)?
	* [DWD ICON](https://www.dwd.de/EN/ourservices/nwp_forecast_data/nwp_forecast_data.html)
	* [KNMI HARMONIE](https://dataplatform.knmi.nl/group/weather-forecast?q=UWC&sort=metadata_modified+desc)?
	* [DMI HARMONIE](https://opendatadocs.dmi.govcloud.dk/Data/Forecast_Data_Weather_Model_HARMONIE_DINI_IG)?
	* [RRFS](https://herbie.readthedocs.io/en/stable/gallery/noaa_models/rrfs.html) and [3D-RTMA/3D-URMA](https://vlab.noaa.gov/web/ufs-r2o/srw-cam)
		* Waiting for the full release to launch before integrating.
5. Add in a day/night forecast as suggested in [issue #49](https://github.com/Pirate-Weather/pirateweather/issues/49)
6. Add in water-related data as suggested in [issue #160](https://github.com/Pirate-Weather/pirateweather/issues/160)
7. Investigate using radar data/station data.
	*  Investigate if it's feasible to use radar data and/or station data for the currently conditions. This is a suggestion in [issue #10](https://github.com/alexander0042/pirateweather/issues/10).
