from datetime import date, timedelta
from typing import List, Dict
from fastapi import APIRouter
from fastapi.responses import FileResponse
from src.core.dependencies import DbPg
from src.modules.qualitycontrol import services
from . import schemas
from ..metadata import schemas as metadata_schemas
from src.auth.dependencies import qc_read_required

router = APIRouter()

@router.get(
    "/data/summary/{date_str}",
    response_model=List[schemas.QcResultSummaryResponseBase],
    dependencies=[qc_read_required],
    summary="Get Daily Quality Summary"
)
async def get_summary(
    db: DbPg,
    date_str: date = date.today() - timedelta(days=1),
):
    """Retrieves a summary of quality control results for all stations on a specific date."""
    return services.get_qc_summary_by_date(db, summary_date=date_str)

@router.get(
    "/data/detail/{code}/{date_str}",
    response_model=List[schemas.StationsQCDetailsResponseBase],
    dependencies=[qc_read_required],
    summary="Get QC Details by Station Code and Date"
)
async def get_qc_details_by_code_and_date(
    db: DbPg,
    code: str,
    date_str: date,
):
    """Retrieves detailed quality control information for a specific station (or 'All') on a given date."""
    return services.get_sorted_qc_details(db, station_code=code, detail_date=date_str)

@router.get(
    "/data/history/{code}/{year}",
    response_model=Dict[str, int],
    dependencies=[qc_read_required],
    summary="Get Quality History for a Station and Year"
)
async def get_quality_history(
    db: DbPg,
    code: str,
    year: int,
):
    """Retrieves the quality history for a specific station over a given year."""
    return services.get_station_quality_history(db, station_code=code, year=year)

@router.get(
    "/site/summary",
    response_model=List[metadata_schemas.StationSiteQualityBase],
    dependencies=[qc_read_required],
    summary="Retrieve All Station Site Quality Data"
)
async def get_all_station_site_qualities(db: DbPg):
    """Retrieves a list of all station site quality records from the database."""
    return services.get_all_site_qualities(db)

@router.get(
    "/site/detail/{code}",
    response_model=List[metadata_schemas.StationSiteQualityBase],
    dependencies=[qc_read_required],
    summary="Get Site Details by Station Code"
)
async def get_site_details_by_code(
    db: DbPg,
    code: str,
):
    """Retrieves site-specific details for a given station code."""
    return services.get_site_quality_by_code(db, station_code=code)

@router.get(
    "/data/psd/{date_str}/{code}/{channel}",
    response_class=FileResponse,
    dependencies=[qc_read_required],
    summary="Get Power Spectral Density (PSD) Image"
)
async def get_psd_image(
    date_str: date,
    code: str,
    channel: str
):
    """Retrieves a securely located Power Spectral Density (PSD) image."""
    file_path = services.get_image_filepath("psd", image_date=date_str, code=code, channel=channel)
    return FileResponse(file_path)

@router.get(
    "/data/signal/{date_str}/{code}/{channel}",
    response_class=FileResponse,
    dependencies=[qc_read_required],
    summary="Get Signal Image"
)
async def get_signal_image(
    date_str: date,
    code: str,
    channel: str
):
    """Retrieves a securely located signal image."""
    file_path = services.get_image_filepath("signal", image_date=date_str, code=code, channel=channel)
    return FileResponse(file_path)

@router.get(
    "/data/availability/{station_code}", # The year is removed from the path
    response_model=schemas.AvailabilityResponseBase,
    dependencies=[qc_read_required],
    summary="Get Station Availability by Channel in Date Range"
)
def get_station_availability_endpoint(
    station_code: str,
    start_date: date,
    end_date: date,
    db: DbPg
):
    """
    Retrieves the availability/quality data for a station within a specific
    date range, pivoted by channel for each day.
    """
    data_list = services.get_station_availability_by_date(
        db=db,
        station_code=station_code,
        start_date=start_date,
        end_date=end_date
    )

    meta_data = {
        "code": station_code,
        "count": len(data_list)
    }

    # 3. Return the final response
    return {
        "meta": meta_data,
        "data": data_list
    }

@router.get(
    "/data/availability/",  # Note: The path is now at the root level without a station code
    response_model=schemas.AllStationsAvailabilityResponse,
    dependencies=[qc_read_required],
    summary="Get All Stations Availability by Channel in Date Range"
)
def get_all_stations_availability_endpoint(
    start_date: date,
    end_date: date,
    db: DbPg
):
    """
    Retrieves the availability/quality data for ALL stations within a specific
    date range, pivoted by channel for each day. The result is a dictionary
    keyed by station code.
    """
    data_dict = services.get_all_stations_availability_by_date(
        db=db,
        start_date=start_date,
        end_date=end_date
    )

    # Calculate total records across all stations for metadata
    total_records = sum(len(v) for v in data_dict.values())

    meta_data = {
        "stationCount": len(data_dict),
        "totalRecords": total_records
    }

    return {"meta": meta_data, "data": data_dict}