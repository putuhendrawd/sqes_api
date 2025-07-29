from datetime import datetime as datetime_cls
from typing import List, Optional, Dict
from fastapi import APIRouter, Query
from src.core.dependencies import DbMySQL, DbPg
from src.modules.metadata import services, schemas
from src.auth.dependencies import metadata_read_required

router = APIRouter(dependencies=[metadata_read_required])


# @router.get(
#     "/mysql/all",
#     response_model=List[schemas.MetadataMySQLBase],
#     summary="Get All Metadata from MySQL"
# )
# async def get_all_mysql_metadata(db: DbMySQL):
#     """Retrieves all station metadata records from the MySQL database."""
#     return services.get_all_mysql_metadata(db)


# @router.get(
#     "/mysql/{sta_code}",
#     response_model=schemas.MetadataMySQLBase,
#     summary="Get Metadata of Specific Station from MySQL"
# )
# async def get_mysql_metadata(sta_code: str, db: DbMySQL):
#     """Retrieves metadata for a specific station from the MySQL database."""
#     return services.get_mysql_metadata_by_station(db, sta_code)


# @router.get(
#     "/pg/all",
#     response_model=List[schemas.MetadataPostgreSQLBase],
#     summary="Get All Metadata from PostgreSQL"
# )
# async def get_all_pg_metadata(db: DbPg):
#     """Retrieves all station metadata records from the PostgreSQL database."""
#     return services.get_all_pg_metadata(db)


# @router.get(
#     "/pg/{sta_code}",
#     response_model=schemas.MetadataPostgreSQLBase,
#     summary="Get Metadata of Specific Station from PostgreSQL"
# )
# async def get_pg_metadata(sta_code: str, db: DbPg):
#     """Retrieves metadata for a specific station from the PostgreSQL database."""
#     return services.get_pg_metadata_by_station(db, sta_code)


@router.get(
    "/pg-combined/all",
    response_model=List[schemas.CombinedStationDataPostgreSQLBase],
    summary="Get All Combined PostgreSQL Data"
)
async def get_all_postgresql_combined_data(db: DbPg):
    """Fetches and combines data from multiple PostgreSQL tables for all stations."""
    return services.get_all_combined_pg_data(db)


@router.get(
    "/pg-combined/{sta_code}",
    response_model=schemas.CombinedStationDataPostgreSQLBase,
    summary="Get Combined PostgreSQL Data for a Single Station"
)
async def get_single_postgresql_combined_data(sta_code: str, db: DbPg):
    """Fetches and combines data for a single station from multiple PostgreSQL tables."""
    return services.get_combined_pg_data_by_station(db, sta_code)


@router.get(
    "/sensors/{sta_code}",
    response_model=List[schemas.StationSensorBase],
    summary="Retrieve Station Sensor Information"
)
async def read_station_sensors(sta_code: str, db: DbPg):
    """Retrieves a list of sensor information for a specific station by its code."""
    return services.get_sensors_by_station(db, sta_code)


@router.get(
    "/latency/{sta_code}/{channel}",
    response_model=Dict[datetime_cls, int],
    summary="Retrieve Latency Data for a Specific Station and Channel"
)
async def read_station_sensor_latency(
    sta_code: str,
    channel: str,
    db: DbPg,
    start_datetime: Optional[datetime_cls] = Query(None, description="Start datetime (ISO format). Defaults to 7 days ago."),
    end_datetime: Optional[datetime_cls] = Query(None, description="End datetime (ISO format). Defaults to now."),
):
    """Fetches latency records for a station and channel within a specified time range."""
    return services.get_latency_by_station_channel(
        db=db,
        sta=sta_code,
        channel=channel,
        start_dt=start_datetime,
        end_dt=end_datetime
    )

