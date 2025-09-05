import logging
import os
from datetime import date
from typing import Dict, List, Any
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from src.core.config import settings
from . import models
from ..metadata import models as metadata_models
from .schemas import StationsQCDetailsResponseBase, DataItemSchemas

logger = logging.getLogger(__name__)

def get_qc_summary_by_date(db: Session, summary_date: date) -> List[models.StationsDataQualityPostgreSQL]:
    """Fetches the QC summary for all stations on a given date."""
    query = (
        select(models.StationsDataQualityPostgreSQL)
        .options(
            joinedload(models.StationsDataQualityPostgreSQL.station_metadata),
            joinedload(models.StationsDataQualityPostgreSQL.station_site_quality)
        )
        .where(models.StationsDataQualityPostgreSQL.date == summary_date)
    )
    data = db.execute(query).scalars().all()
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No quality summary data found for date '{summary_date.isoformat()}'."
        )
    return data

def get_sorted_qc_details(db: Session, station_code: str, detail_date: date) -> List[StationsQCDetailsResponseBase]:
    """Fetches and sorts QC details for a specific station or all stations on a given date."""
    query = select(models.StationsQCDetailsPostgreSQL).where(models.StationsQCDetailsPostgreSQL.date == detail_date)
    if station_code.lower() != "all":
        query = query.where(models.StationsQCDetailsPostgreSQL.code == station_code)
    
    qc_details = db.execute(query).scalars().all()

    if not qc_details:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No QC details found for code '{station_code}' on date '{detail_date.isoformat()}'"
        )

    def sort_key(item: StationsQCDetailsResponseBase):
        channel_last_char = item.channel[-1].upper() if item.channel else ''
        return {'E': 0, 'N': 1, 'Z': 2}.get(channel_last_char, 3)

    return sorted(qc_details, key=sort_key)

def get_station_quality_history(db: Session, station_code: str, year: int) -> Dict[str, int]:
    """Compiles a yearly quality history for a single station."""
    start_date = date(year, 1, 1)
    end_date = date(year, 12, 31)

    query = select(models.StationsDataQualityPostgreSQL).where(
        models.StationsDataQualityPostgreSQL.code == station_code,
        models.StationsDataQualityPostgreSQL.date.between(start_date, end_date)
    )
    records = db.execute(query).scalars().all()

    if not records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No quality history found for station '{station_code}' in year {year}"
        )

    result_map = {"Baik": 4, "Cukup Baik": 3, "Buruk": 2, "Mati": 1}
    history_dict = {
        record.date.isoformat(): result_map.get(record.result, 0)
        for record in records
    }
    return history_dict

def get_site_quality_by_code(db: Session, station_code: str) -> List[metadata_models.StationSiteQualityPostgreSQL]:
    """Retrieves site-specific details for a given station code."""
    query = select(metadata_models.StationSiteQualityPostgreSQL).where(metadata_models.StationSiteQualityPostgreSQL.code == station_code)
    site_details = db.execute(query).scalars().all()
    if not site_details:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No site details found for code '{station_code}'"
        )
    return site_details

def get_all_site_qualities(db: Session) -> List[metadata_models.StationSiteQualityPostgreSQL]:
    """Retrieves all records from the stations_site_quality table."""
    stations = db.execute(select(metadata_models.StationSiteQualityPostgreSQL)).scalars().all()
    if not stations:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No station site quality data found."
        )
    return stations

def get_image_filepath(image_type: str, image_date: date, code: str, channel: str) -> str:
    """Constructs and validates a secure file path for an image."""
    if image_type == "psd":
        base_path = os.path.join(settings.IMAGE_STORAGE_BASE_PATH, settings.PSD_IMAGE_SUBDIR)
        filename = f"{code}_{channel}_PDF.png"
    elif image_type == "signal":
        base_path = os.path.join(settings.IMAGE_STORAGE_BASE_PATH, settings.SIGNAL_IMAGE_SUBDIR)
        filename = f"{code}_{channel}_signal.png"
    else:
        logger.error(f"Invalid image type requested: {image_type}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image type specified.")

    if ".." in code or "/" in code or ".." in channel or "/" in channel:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid characters in code or channel.")
    
    date_str = image_date.strftime("%Y-%m-%d")
    full_path = os.path.join(base_path, date_str, filename)

    if not os.path.normpath(full_path).startswith(os.path.normpath(base_path)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File path is outside the allowed directory.")

    if not os.path.exists(full_path):
        logger.warning(f"Image file not found at path: {full_path}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image file not found.")

    return full_path

def get_station_availability_by_date(
    db: Session,
    station_code: str,
    start_date: date,
    end_date: date
) -> List[Dict[str, Any]]:
    """
    Compiles an availability history for a station within a date range, pivoted by channel.
    """
    query = select(models.StationsQCDetailsPostgreSQL).where(
        models.StationsQCDetailsPostgreSQL.code == station_code,
        models.StationsQCDetailsPostgreSQL.date.between(start_date, end_date)
    ).order_by(models.StationsQCDetailsPostgreSQL.date)

    records = db.execute(query).scalars().all()

    if not records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No availability history found for station '{station_code}' between {start_date} and {end_date}"
        )

    grouped_by_date = {}

    for record in records:
        date_str = record.date.isoformat()
        
        if date_str not in grouped_by_date:
            grouped_by_date[date_str] = {'timestamp': record.date}
        
        grouped_by_date[date_str][record.channel] = record.availability

    return list(grouped_by_date.values())

def get_all_stations_availability_by_date(
    db: Session,
    start_date: date,
    end_date: date
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Compiles an availability history for all stations within a date range.
    The result is a dictionary with station codes as keys, and the values are
    lists of availability data, pivoted by channel for each date.
    """
    query = select(models.StationsQCDetailsPostgreSQL).where(
        models.StationsQCDetailsPostgreSQL.date.between(start_date, end_date)
    ).order_by(models.StationsQCDetailsPostgreSQL.code, models.StationsQCDetailsPostgreSQL.date)

    records = db.execute(query).scalars().all()

    if not records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No availability history found for any station between {start_date} and {end_date}"
        )

    # This will hold the final structured data, e.g., {'STN1': [date_data_1, date_data_2]}
    all_stations_data = {}

    for record in records:
        station_code = record.code
        date_str = record.date.isoformat()
        
        # If the station is not yet in our dictionary, add it.
        # The value will be a dictionary to group records by date string.
        if station_code not in all_stations_data:
            all_stations_data[station_code] = {}
        
        # Get the dictionary that holds date-grouped data for the current station.
        station_dates = all_stations_data[station_code]
        
        # If the date is not yet a key for the current station, add it.
        if date_str not in station_dates:
            station_dates[date_str] = {'timestamp': record.date}
        
        # Add the channel availability to the corresponding date entry.
        station_dates[date_str][record.channel] = record.availability

    # The data is currently grouped like: {'STN1': {'2023-01-01': {...}, '2023-01-02': {...}}}
    # We need to convert the inner dictionaries of dates into lists.
    final_result = {}
    for station_code, dates_dict in all_stations_data.items():
        final_result[station_code] = list(dates_dict.values())

    return final_result