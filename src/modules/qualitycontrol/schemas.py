from pydantic import BaseModel, Field, condecimal, computed_field, ConfigDict
from typing import Optional, List, Annotated, Dict
from decimal import Decimal
from datetime import datetime as datetime_cls, date as date_cls
from ..metadata.schemas import MetadataPostgreSQLBase, StationSiteQualityBase


## Response Schemas ##

class GeometryBase(BaseModel):
    """
    **Geometry Model for Geographic Coordinates**

    This schema defines a standard representation for geographic point data,
    typically used to describe the location of a station or sensor.

    Attributes:
    - **type** (`str`): The type of geometry. For a single location, this is typically "Point".
    - **coordinates** (`List[float]`): A list representing the geographic coordinates.
      It follows the [longitude, latitude] order, consistent with GeoJSON standards.
      An optional third element can represent altitude.

    Example:
    ```json
    {
      "type": "Point",
      "coordinates": [106.8271, -6.1745, 1.0]
    }
    ```
    """
    type: str = Field(..., description="Type of geometry, e.g., 'Point'")
    coordinates: List[float] = Field(..., description="List of coordinates [longitude, latitude, (optional) altitude]")
    
class QcResultSummaryResponseBase(BaseModel):
    """
    **QC Result Summary Response Model**

    This schema provides a summarized overview of Quality Control (QC) results for a station
    on a specific date. It integrates core QC metrics with related station metadata and
    site quality information, utilizing computed fields to flatten data from nested objects.

    Attributes:
    - **station_metadata** (`MetadataPostgreSQLBase`): Internal field representing the full PostgreSQL metadata. Excluded from direct JSON output.
    - **station_site_quality** (`StationSiteQualityBase`): Internal field representing the full station site quality data. Excluded from direct JSON output.
    - **date** (`datetime_cls`): The date for which the QC summary applies.
    - **code** (`str`): The unique station code.
    - **quality_percentage** (`float`): The overall data quality percentage for the given date.
    - **result** (`str`): A textual summary of the QC result (e.g., "Good", "Poor", "Missing").
    - **details** (`str`): More detailed information or remarks about the QC result.

    Computed Fields:
    - **network** (`Optional[str]`): The seismic network of the station, derived from `station_metadata`.
    - **site_quality** (`Optional[str]`): The overall site quality description, derived from `station_site_quality`.
    - **network_group** (`Optional[str]`): The broader network grouping, derived from `station_metadata`.
    - **balai** (`Optional[int]`): The Balai (regional office) identifier, derived from `station_metadata`.
    - **upt** (`Optional[str]`): The UPT (Technical Implementation Unit) identifier, derived from `station_metadata`.
    - **communication** (`Optional[str]`): The communication type used by the station, derived from `station_metadata`.
    - **digitizer** (`Optional[str]`): The digitizer type used at the station, derived from `station_metadata`.
    - **year** (`Optional[str]`): The year of station installation, derived from `station_metadata`.
    - **geometry** (`Optional[GeometryBase]`): The geographic coordinates of the station as a `Point` geometry, derived from `station_metadata`.

    Config:
    - `from_attributes = True`: Enables mapping from ORM models (SQLAlchemy) to Pydantic models.
    """
    station_metadata: MetadataPostgreSQLBase = Field(..., exclude=True, description="Internal field for PostgreSQL station metadata (not directly serialized)")
    station_site_quality: StationSiteQualityBase = Field(..., exclude=True, description="Internal field for station site quality data (not directly serialized)")

    date: datetime_cls = Field(..., description="The date for which the QC summary applies")
    code: str = Field(..., description="The unique station code")
    quality_percentage: float = Field(..., description="The overall data quality percentage for the given date")
    result: str = Field(..., description="A textual summary of the QC result (e.g., 'Good', 'Poor', 'Missing')")
    details: str = Field(..., description="More detailed information or remarks about the QC result")
    
    @computed_field
    @property
    def network(self) -> Optional[str]:
        """The seismic network of the station, derived from station_metadata."""
        if hasattr(self, 'station_metadata') and self.station_metadata:
            return self.station_metadata.network
        return None
    
    @computed_field
    @property
    def site_quality(self) -> Optional[str]:
        """The overall site quality description, derived from station_site_quality."""
        if hasattr(self, 'station_site_quality') and self.station_site_quality:
            return self.station_site_quality.site_quality
        return None
    
    @computed_field
    @property
    def network_group(self) -> Optional[str]:
        """The broader network grouping, derived from station_metadata."""
        if hasattr(self, 'station_metadata') and self.station_metadata:
            return self.station_metadata.network_group
        return None

    @computed_field
    @property
    def balai(self) -> Optional[int]:
        """The Balai (regional office) identifier, derived from station_metadata."""
        if hasattr(self, 'station_metadata') and self.station_metadata:
            return self.station_metadata.balai
        return None

    @computed_field
    @property
    def upt(self) -> Optional[str]:
        """The UPT (Technical Implementation Unit) identifier, derived from station_metadata."""
        if hasattr(self, 'station_metadata') and self.station_metadata:
            return self.station_metadata.upt
        return None

    @computed_field
    @property
    def communication(self) -> Optional[str]:
        """The communication type used by the station, derived from station_metadata."""
        if hasattr(self, 'station_metadata') and self.station_metadata:
            return self.station_metadata.communication_type
        return None
    
    @computed_field
    @property
    def digitizer(self) -> Optional[str]:
        """The digitizer type used at the station, derived from station_metadata."""
        if hasattr(self, 'station_metadata') and self.station_metadata:
            return self.station_metadata.digitizer_type
        return None
    
    @computed_field
    @property
    def year(self) -> Optional[int]:
        """The year of station installation, derived from station_metadata."""
        if hasattr(self, 'station_metadata') and self.station_metadata:
            return self.station_metadata.year
        return None
    
    @computed_field
    @property
    def geometry(self) -> Optional[GeometryBase]:
        """
        The geographic coordinates of the station as a Point geometry,
        derived from station_metadata's latitude and longitude.
        """
        if hasattr(self, 'station_metadata') and self.station_metadata:
            if self.station_metadata.latitude is not None and self.station_metadata.longitude is not None:
                return GeometryBase(
                    type="Point",
                    coordinates=[float(self.station_metadata.longitude), float(self.station_metadata.latitude), 1.0]
                )
        return None

    class Config:
        from_attributes = True

class StationsQCDetailsResponseBase(BaseModel):
    """
    **Stations QC Details Response Model**

    This schema represents a detailed record of Quality Control (QC) metrics
    for a specific channel of a station on a given date. It covers various
    aspects of data quality, including signal characteristics, gaps, and noise levels.

    Attributes:
    - **id** (`str`): Unique identifier for the QC detail record (Primary Key).
    - **code** (`str`): The unique station code.
    - **date** (`date`): The date for which the QC metrics are reported.
    - **channel** (`str`): The specific channel (e.g., HHZ, HHE, HHN) to which these QC metrics apply.
    - **rms** (`Decimal`): Root Mean Square (RMS) value of the signal.
    - **amplitude_ratio** (`Decimal`): Ratio of amplitudes, often used for data quality assessment.
    - **availability** (`Decimal`): Percentage of data availability.
    - **num_gap** (`int`): Number of data gaps detected.
    - **num_overlap** (`int`): Number of data overlaps detected.
    - **num_spikes** (`int`): Number of spikes detected in the data.
    - **perc_below_nlnm** (`Decimal`): Percentage of time the signal is below the New Low Noise Model (NLNM).
    - **perc_above_nhnm** (`Decimal`): Percentage of time the signal is above the New High Noise Model (NHNM).
    - **linear_dead_channel** (`Decimal`): Metric indicating linearity for dead channel detection.
    - **gsn_dead_channel** (`Decimal`): Metric indicating GSN-based dead channel detection.
    - **sp_percentage** (`Decimal`): Short Period data percentage.
    - **bw_percentage** (`Decimal`): Broad Band data percentage.
    - **lp_percentage** (`Decimal`): Long Period data percentage.

    Config:
    - `from_attributes = True`: Enables mapping from ORM models (SQLAlchemy) to Pydantic models.
    """
    id: str = Field(..., description="Unique identifier for the QC detail record (Primary Key)")
    code: str = Field(..., description="The unique station code")
    date: date_cls = Field(..., description="The date for which the QC metrics are reported")
    channel: str = Field(..., description="The specific channel (e.g., HHZ, HHE, HHN) to which these QC metrics apply")
    rms: Annotated[Decimal, condecimal(max_digits=7, decimal_places=2)] = Field(..., description="Root Mean Square (RMS) value of the signal")
    amplitude_ratio: Annotated[Decimal, condecimal(max_digits=7, decimal_places=2)] = Field(..., description="Ratio of amplitudes, often used for data quality assessment")
    availability: Annotated[Decimal, condecimal(max_digits=5, decimal_places=2)] = Field(..., description="Percentage of data availability")
    num_gap: int = Field(..., description="Number of data gaps detected")
    num_overlap: int = Field(..., description="Number of data overlaps detected")
    num_spikes: int = Field(..., description="Number of spikes detected in the data")
    perc_below_nlnm: Annotated[Decimal, condecimal(max_digits=5, decimal_places=2)] = Field(..., description="Percentage of time the signal is below the New Low Noise Model (NLNM)")
    perc_above_nhnm: Annotated[Decimal, condecimal(max_digits=5, decimal_places=2)] = Field(..., description="Percentage of time the signal is above the New High Noise Model (NHNM)")
    linear_dead_channel: Annotated[Decimal, condecimal(max_digits=7, decimal_places=2)] = Field(..., description="Metric indicating linearity for dead channel detection")
    gsn_dead_channel: Annotated[Decimal, condecimal(max_digits=7, decimal_places=2)] = Field(..., description="Metric indicating GSN-based dead channel detection")
    sp_percentage: Annotated[Decimal, condecimal(max_digits=5, decimal_places=2)] = Field(..., description="Short Period data percentage")
    bw_percentage: Annotated[Decimal, condecimal(max_digits=5, decimal_places=2)] = Field(..., description="Broad Band data percentage")
    lp_percentage: Annotated[Decimal, condecimal(max_digits=5, decimal_places=2)] = Field(..., description="Long Period data percentage")

    class Config:
        from_attributes = True

# Respon schemas for time-based data retrieval
class DataItemSchemas(BaseModel):
    """
    **Data Item Schema for Time-Based Retrieval**

    This schema represents a single data item with a timestamp and value,
    typically used for time-series data retrieval.

    Attributes:
    - **timestamp** (`datetime_cls`): The timestamp of the data item.
    """
    model_config = ConfigDict(extra="allow")
    timestamp: datetime_cls = Field(..., description="The timestamp of the data item")

class MetaSchemas(BaseModel):
    """
    **Metadata Schema for Time-Based Retrieval**

    This schema represents metadata associated with a time-based data retrieval,
    including the station code and a list of data items.

    Attributes:
    - **station_code** (`str`): The unique code of the station.
    - **data** (`List[DataItemSchemas]`): A list of data items, each containing a timestamp and value.
    - **count** (`int`): The number of data items retrieved.
    """
    code: str = Field(..., description="The unique code of the station")
    count: int = Field(..., description="The number of data items retrieved")
                                        
class AvailabilityResponseBase(BaseModel):
    """
    **Availability Response Model**

    This schema represents the availability of data for a specific station
    over a given time period, including the station code and a list of data items.

    Attributes:
    - **meta** (`str`): The metadata of the data retrieval.
    - **data** (`List[DataItemSchemas]`): A list of data items, each containing a timestamp and value.
    """
    meta: MetaSchemas = Field(..., description="Metadata about the data retrieval, including station code and count")
    data: List[DataItemSchemas] = Field(..., description="A list of data items with timestamps and values")

class AllStationsAvailabilityMeta(BaseModel):
    """
    **Metadata Schema for All-Station Availability Retrieval**

    This schema represents metadata for retrieving availability data across all stations.

    Attributes:
    - **station_count** (`int`): The total number of stations returned.
    - **total_records** (`int`): The total number of daily records across all stations.
    """
    station_count: int = Field(..., alias='stationCount', description="The total number of stations returned.")
    total_records: int = Field(..., alias='totalRecords', description="The total number of daily records across all stations.")


class AllStationsAvailabilityResponse(BaseModel):
    """
    **All-Station Availability Response Model**

    This schema represents the availability data for all stations over a given time period.
    The data is structured as a dictionary where keys are station codes.

    Attributes:
    - **meta** (`AllStationsAvailabilityMeta`): Metadata about the data retrieval.
    - **data** (`Dict[str, List[DataItemSchemas]]`): A dictionary of station data.
    """
    meta: AllStationsAvailabilityMeta
    data: Dict[str, List[DataItemSchemas]]