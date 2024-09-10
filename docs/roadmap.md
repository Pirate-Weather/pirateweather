# Roadmap
1. Open source API code and Docker containers to allow self-hosting.
	* Longer blog post on V2 processing flow using Herbie -> wgrib2 -> xarray -> Dask -> Zarr arrays on LMDB for data.  
2. Text summaries and translations
	* Based on the [existing repository](https://github.com/alexander0042/translations).
3. Weather maps from new Zarr datafiles.
4. Add in alerts for Canada/ EU/ other.
5. Add in a Air Quality Index as suggested in [issue #92](https://github.com/Pirate-Weather/pirateweather/issues/92)
6. Add source data.
	* Add in the Canadian models ([HRDPS](https://herbie.readthedocs.io/en/stable/gallery/eccc_models/hrdps.html), [GDPS](https://herbie.readthedocs.io/en/stable/gallery/eccc_models/gdps.html))
	* Add in the Canadian models ([HRDPS](https://herbie.readthedocs.io/en/stable/gallery/eccc_models/hrdps.html), [GDPS](https://herbie.readthedocs.io/en/stable/gallery/eccc_models/gdps.html) and [RDPS](https://herbie.readthedocs.io/en/stable/gallery/eccc_models/rdps.html))
	* [NBM-Alaska/ Hawaii/ Puerto Rico/ Guam](https://herbie.readthedocs.io/en/stable/gallery/noaa_models/nbm.html)
	* [RTMA/ URMA](https://herbie.readthedocs.io/en/stable/gallery/noaa_models/rtma-urma.html)
	* [ECMWF](https://herbie.readthedocs.io/en/stable/gallery/ecmwf_models/ecmwf.html)
	* [NOAA GraphCast](https://herbie.readthedocs.io/en/stable/gallery/noaa_models/gfs.html#GFS-GraphCast)?
	* [DWD ICON](https://www.dwd.de/EN/ourservices/nwp_forecast_data/nwp_forecast_data.html)
	* [KNMI HARMONIE](https://dataplatform.knmi.nl/group/weather-forecast?q=UWC&sort=metadata_modified+desc)?
	* [DMI HARMONIE](https://opendatadocs.dmi.govcloud.dk/Data/Forecast_Data_Weather_Model_HARMONIE_DINI_IG)?
	* [RRFS](https://herbie.readthedocs.io/en/stable/gallery/noaa_models/rrfs.html) and/or [3D-RTMA/3D-URMA](https://vlab.noaa.gov/web/ufs-r2o/srw-cam)
		* Waiting for the full release to launch before integrating.
7. Add in a day/night forecast as suggested in [issue #49](https://github.com/Pirate-Weather/pirateweather/issues/49)
8. Add in water-related data as suggested in [issue #160](https://github.com/Pirate-Weather/pirateweather/issues/160)
9. Investigate using radar data/station data.
