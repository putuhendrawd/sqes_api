import logging
from datetime import datetime as datetime_cls, timedelta
from typing import List, Dict, Optional

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from . import models, schemas

logger = logging.getLogger(__name__)


def get_all_mysql_metadata(db: Session) -> List[models.MetadataMySQL]:
    """Fetches all station metadata from the MySQL database."""
    metadata = db.execute(select(models.MetadataMySQL)).scalars().all()
    if not metadata:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No metadata found in MySQL.")
    return metadata

def get_mysql_metadata_by_station(db: Session, sta_code: str) -> models.MetadataMySQL:
    """Fetches metadata for a single station from MySQL."""
    metadata = db.execute(
        select(models.MetadataMySQL).where(models.MetadataMySQL.kode_sensor == sta_code)
    ).scalar_one_or_none()
    if not metadata:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Metadata for station '{sta_code}' not found in MySQL.")
    return metadata

def get_all_pg_metadata(db: Session) -> List[models.MetadataPostgreSQL]:
    """Fetches all station metadata from the PostgreSQL database."""
    metadata = db.execute(select(models.MetadataPostgreSQL)).scalars().all()
    if not metadata:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No metadata found in PostgreSQL.")
    return metadata

def get_pg_metadata_by_station(db: Session, sta_code: str) -> models.MetadataPostgreSQL:
    """Fetches metadata for a single station from PostgreSQL."""
    metadata = db.execute(
        select(models.MetadataPostgreSQL).where(models.MetadataPostgreSQL.code == sta_code)
    ).scalar_one_or_none()
    if not metadata:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Metadata for station '{sta_code}' not found in PostgreSQL.")
    return metadata


def _build_combined_pg_object(
    main_rec: models.MetadataPostgreSQL,
    visit_lookup: Dict,
    quality_lookup: Dict
) -> schemas.CombinedStationDataPostgreSQLBase:
    """Helper function to construct a single combined PostgreSQL data object."""
    join_key = main_rec.code
    visit_rec = visit_lookup.get(join_key)
    quality_rec = quality_lookup.get(join_key)

    data_dict = {
        **main_rec.__dict__,
        "visit_year": visit_rec.visit_year if visit_rec else "",
        "visit_count": visit_rec.visit_count if visit_rec else 0,
        "dominant_data_quality": quality_rec.dominant_data_quality if quality_rec else "Unknown"
    }
    return schemas.CombinedStationDataPostgreSQLBase(**data_dict)


def get_all_combined_pg_data(db: Session) -> List[schemas.CombinedStationDataPostgreSQLBase]:
    """Fetches and combines station data from multiple PostgreSQL tables."""
    main_records = db.execute(select(models.MetadataPostgreSQL)).scalars().all()
    if not main_records:
        raise HTTPException(status_code=404, detail="No primary station records found in PostgreSQL.")
        
    visit_records = db.execute(select(models.StationVisitPostgreSQL)).scalars().all()
    quality_records = db.execute(select(models.StationDominantDataQualityPostgreSQL)).scalars().all()

    visit_lookup = {rec.code: rec for rec in visit_records}
    quality_lookup = {rec.code: rec for rec in quality_records}

    return [_build_combined_pg_object(rec, visit_lookup, quality_lookup) for rec in main_records]


def get_combined_pg_data_by_station(db: Session, sta_code: str) -> schemas.CombinedStationDataPostgreSQLBase:
    """Fetches and combines data for a single station from PostgreSQL."""
    main_rec = get_pg_metadata_by_station(db, sta_code)
    
    visit_rec = db.execute(select(models.StationVisitPostgreSQL).where(models.StationVisitPostgreSQL.code == sta_code)).scalar_one_or_none()
    quality_rec = db.execute(select(models.StationDominantDataQualityPostgreSQL).where(models.StationDominantDataQualityPostgreSQL.code == sta_code)).scalar_one_or_none()
    
    visit_lookup = {sta_code: visit_rec} if visit_rec else {}
    quality_lookup = {sta_code: quality_rec} if quality_rec else {}

    return _build_combined_pg_object(main_rec, visit_lookup, quality_lookup)


def get_sensors_by_station(db: Session, sta_code: str) -> List[models.StationSensorPostgreSQL]:
    """Retrieves sensor information for a specific station."""
    sensors = db.execute(
        select(models.StationSensorPostgreSQL).where(models.StationSensorPostgreSQL.code == sta_code)
    ).scalars().all()
    if not sensors:
        raise HTTPException(status_code=404, detail=f"Station sensor data not found for code '{sta_code}'")
    return sensors

def get_latency_by_station_channel(
    db: Session,
    sta: str,
    channel: str,
    start_dt: Optional[datetime_cls],
    end_dt: Optional[datetime_cls]
) -> Dict[datetime_cls, int]:
    """Retrieves latency data with robust date filtering."""
    # Define the time range
    if start_dt is None and end_dt is None:
        end_dt = datetime_cls.now()
        start_dt = end_dt - timedelta(days=7)
    elif start_dt and not end_dt:
        end_dt = datetime_cls.now()
    elif not start_dt and end_dt:
        start_dt = end_dt - timedelta(days=7)

    query = select(models.StationSensorLatencyPostgreSQL).where(
        models.StationSensorLatencyPostgreSQL.sta == sta,
        models.StationSensorLatencyPostgreSQL.channel == channel,
        models.StationSensorLatencyPostgreSQL.datetime.between(start_dt, end_dt)
    )
    latencies = db.execute(query).scalars().all()
    if not latencies:
        raise HTTPException(
            status_code=404,
            detail="Latency data not available for the specified station, channel, and date range."
        )
    return {item.datetime: item.latency if item.latency is not None else -1 for item in latencies}


