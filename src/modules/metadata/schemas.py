from pydantic import BaseModel, Field, condecimal, computed_field
from typing import Optional, List, Dict, Any, Annotated
from decimal import Decimal
from datetime import datetime as datetime_cls
from datetime import timedelta

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

# Pydantic Model for MetadataMySQL (tb_slmon)
class MetadataMySQLBase(BaseModel):
    """
    **Metadata from MySQL Database (tb_slmon)**

    This schema represents the structure of station metadata stored in the
    `tb_slmon` table within the MySQL database. It includes general information
    about the sensor, its location, status, and associated data quality metrics.

    Attributes:
    - **no_urut** (`int`): Sequential number.
    - **kode_sensor** (`Optional[str]`): Unique code for the sensor/station.
    - **lokasi_sensor** (`Optional[str]`): Textual description of the sensor's location.
    - **lat_sensor** (`Optional[str]`): Latitude of the sensor as a string.
    - **lon_sensor** (`Optional[str]`): Longitude of the sensor as a string.
    - **sistem_sensor** (`Optional[str]`): Type of sensor system.
    - **pj_sensor** (`Optional[str]`): Responsible person or team for the sensor.
    - **balai** (`Optional[str]`): Regional office or unit responsible.
    - **ket_sensor** (`Optional[str]`): Additional remarks or notes about the sensor.
    - **status_sensor** (`Optional[str]`): Current operational status of the sensor.
    - **last_data** (`Optional[str]`): Timestamp or indicator of the last data received.
    - **pic** (`Optional[str]`): Person in charge.
    - **sta_mag** (`Optional[str]`): Station magnitude information (e.g., related to seismic activity).
    - **geo** (`Optional[str]`): Path or link to geographical survey data.
    - **vs30** (`Optional[str]`): Path or link to Vs30 (shear wave velocity) data.
    - **photo** (`Optional[str]`): Path or link to station photos.
    - **hvsr** (`Optional[str]`): Path or link to Horizontal-to-Vertical Spectral Ratio (HVSR) data.
    - **psd** (`Optional[str]`): Path or link to Power Spectral Density (PSD) data.
    - **nilai** (`Optional[str]`): A value associated with the station (e.g., a score).
    - **keterangan2** (`Optional[str]`): Further description or additional notes.
    - **gval** (`Optional[int]`): Numeric value derived from 'geo' data.
    - **vval** (`Optional[int]`): Numeric value derived from 'vs30' data.
    - **pval** (`Optional[int]`): Numeric value derived from 'photo' data.
    - **hval** (`Optional[int]`): Numeric value derived from 'hvsr' data.
    - **psdval** (`Optional[int]`): Numeric value derived from 'psd' data.
    - **sensormerk** (`Optional[str]`): Brand or manufacturer of the sensor.
    - **digitizermerk** (`Optional[str]`): Brand or manufacturer of the digitizer.

    Config:
    - `from_attributes = True`: Enables mapping from ORM models (SQLAlchemy) to Pydantic models.
    """
    no_urut: int
    kode_sensor: Optional[str] = Field(None, max_length=30, description="Unique code for the sensor/station")
    lokasi_sensor: Optional[str] = Field(None, max_length=300, description="Textual description of the sensor's location")
    lat_sensor: Optional[str] = Field(None, max_length=30, description="Latitude of the sensor as a string")
    lon_sensor: Optional[str] = Field(None, max_length=30, description="Longitude of the sensor as a string")
    sistem_sensor: Optional[str] = Field(None, max_length=60, description="Type of sensor system")
    pj_sensor: Optional[str] = Field(None, max_length=30, description="Responsible person or team for the sensor")
    balai: Optional[str] = Field(None, max_length=30, description="Regional office or unit responsible")
    ket_sensor: Optional[str] = Field(None, max_length=60, description="Additional remarks or notes about the sensor")
    status_sensor: Optional[str] = Field(None, max_length=30, description="Current operational status of the sensor")
    last_data: Optional[str] = Field(None, max_length=60, description="Timestamp or indicator of the last data received")
    pic: Optional[str] = Field(None, max_length=30, description="Person in charge")
    sta_mag: Optional[str] = Field(None, max_length=15, description="Station magnitude information")
    geo: Optional[str] = Field(None, max_length=300, description="Path or link to geographical survey data")
    vs30: Optional[str] = Field(None, max_length=300, description="Path or link to Vs30 (shear wave velocity) data")
    photo: Optional[str] = Field(None, max_length=300, description="Path or link to station photos")
    hvsr: Optional[str] = Field(None, max_length=300, description="Path or link to Horizontal-to-Vertical Spectral Ratio (HVSR) data")
    psd: Optional[str] = Field(None, max_length=300, description="Path or link to Power Spectral Density (PSD) data")
    nilai: Optional[str] = Field(None, max_length=10, description="A value associated with the station")
    keterangan2: Optional[str] = Field(None, max_length=100, description="Further description or additional notes")
    gval: Optional[int] = Field(None, description="Numeric value derived from 'geo' data")
    vval: Optional[int] = Field(None, description="Numeric value derived from 'vs30' data")
    pval: Optional[int] = Field(None, description="Numeric value derived from 'photo' data")
    hval: Optional[int] = Field(None, description="Numeric value derived from 'hvsr' data")
    psdval: Optional[int] = Field(None, description="Numeric value derived from 'psd' data")
    sensormerk: Optional[str] = Field(None, max_length=50, description="Brand or manufacturer of the sensor")
    digitizermerk: Optional[str] = Field(None, max_length=50, description="Brand or manufacturer of the digitizer")

    class Config:
        from_attributes = True

# Pydantic Model for MetadataPostgreSQL (stations)
class MetadataPostgreSQLBase(BaseModel):
    """
    **Metadata from PostgreSQL Database (stations table)**

    This schema defines the core metadata for seismic stations as stored in the
    `stations` table in the PostgreSQL database. It focuses on general station
    identification, network details, and basic geographical information.

    Attributes:
    - **code** (`str`): Unique identifier code for the station.
    - **network** (`str`): The seismic network to which the station belongs.
    - **latitude** (`Decimal`): Geographic latitude of the station, with high precision.
    - **longitude** (`Decimal`): Geographic longitude of the station, with high precision.
    - **province** (`Optional[str]`): The province where the station is located.
    - **location** (`Optional[str]`): A more detailed textual description of the station's location.
    - **year** (`Optional[int]`): The year the station was established or installed.
    - **upt** (`Optional[str]`): The Unit Pelaksana Teknis (Technical Implementation Unit) responsible for the station.
    - **balai** (`Optional[int]`): An identifier for the Balai (regional office) responsible for the station.
    - **digitizer_type** (`Optional[str]`): Describes the type or model of digitizer used at the station.
    - **communication_type** (`Optional[str]`): Describes the primary method of data communication (e.g., VSAT, fiber).
    - **network_group** (`Optional[str]`): A broader grouping for the network.

    Config:
    - `from_attributes = True`: Enables mapping from ORM models (SQLAlchemy) to Pydantic models.
    """
    code: str = Field(..., max_length=10, description="Unique identifier code for the station")
    network: str = Field(..., max_length=10, description="The seismic network to which the station belongs")
    latitude: Annotated[Decimal, condecimal(max_digits=9, decimal_places=7)] = Field(..., description="Geographic latitude")
    longitude: Annotated[Decimal, condecimal(max_digits=8, decimal_places=5)] = Field(..., description="Geographic longitude")
    province: Optional[str] = Field(None, max_length=50, description="The province where the station is located")
    location: Optional[str] = Field(None, max_length=100, description="A more detailed textual description of the station's location")
    year: Optional[int] = Field(None, description="The year the station was established or installed")
    upt: Optional[str] = Field(None, max_length=100, description="The Unit Pelaksana Teknis (Technical Implementation Unit) responsible for the station")
    balai: Optional[int] = Field(None, description="An identifier for the Balai (regional office) responsible for the station")
    digitizer_type: Optional[str] = Field(None, max_length=100, description="Describes the type or model of digitizer used at the station")
    communication_type: Optional[str] = Field(None, max_length=100, description="Describes the primary method of data communication (e.g., VSAT, fiber)")
    network_group: Optional[str] = Field(None, max_length=100, description="A broader grouping for the network")

    class Config:
        from_attributes = True

# Pydatic Model for Combined Station Data PostgreSQL
class CombinedStationDataPostgreSQLBase(BaseModel):
    """
    **Combined Station Data from PostgreSQL Tables**

    This schema represents a comprehensive view of station data by combining
    information from three PostgreSQL tables: `stations`, `stations_visit`,
    and `stations_dominant_data_quality`. It provides a consolidated record
    for a station, including its core metadata, visit history, and overall
    data quality status.

    Attributes:
    - **code** (`str`): Unique identifier code for the station (from `stations` table).
    - **network** (`str`): Network identifier (from `stations` table).
    - **latitude** (`Decimal`): Geographic latitude (from `stations` table).
    - **longitude** (`Decimal`): Geographic longitude (from `stations` table).
    - **province** (`Optional[str]`): Province name (from `stations` table).
    - **location** (`Optional[str]`): Location description (from `stations` table).
    - **year** (`Optional[int]`): Year of station installation (from `stations` table).
    - **upt** (`Optional[str]`): UPT (Unit Pelaksana Teknis) identifier (from `stations` table).
    - **balai** (`Optional[int]`): Balai identifier (from `stations` table).
    - **digitizer_type** (`Optional[str]`): Type of digitizer used (from `stations` table).
    - **communication_type** (`Optional[str]`): Type of communication used (from `stations` table).
    - **network_group** (`Optional[str]`): Network group identifier (from `stations` table).
    - **visit_year** (`Optional[str]`): Year of station visit (from `stations_visit` table). Defaults to an empty string if not available.
    - **visit_count** (`Optional[int]`): Count of visits (from `stations_visit` table).
    - **dominant_data_quality** (`Optional[str]`): Dominant data quality (from `stations_dominant_data_quality` table).

    Config:
    - `from_attributes = True`: Enables mapping from ORM models (SQLAlchemy) to Pydantic models.
    """
    # Fields from MetadataPostgreSQL (stations)
    code: str = Field(..., description="Station Unique identifier code (from stations table)")
    network: str = Field(..., description="Network identifier (from stations table)")
    latitude: Annotated[Decimal, condecimal(max_digits=9, decimal_places=7)] = Field(..., description="Geographic latitude (from stations table)")
    longitude: Annotated[Decimal, condecimal(max_digits=8, decimal_places=5)] = Field(..., description="Geographic longitude (from stations table)")
    province: Optional[str] = Field(None, max_length=50, description="Province name (from stations table)")
    location: Optional[str] = Field(None, max_length=100, description="Location description (from stations table)")
    year: Optional[int] = Field(None, description="Year of station installation (from stations table)")
    upt: Optional[str] = Field(None, max_length=100, description="UPT (Unit Pelaksana Teknis) identifier (from stations table)")
    balai: Optional[int] = Field(None, description="Balai identifier (from stations table)")
    digitizer_type: Optional[str] = Field(None, max_length=100, description="Type of digitizer used (from stations table)")
    communication_type: Optional[str] = Field(None, max_length=100, description="Type of communication used (from stations table)")
    network_group: Optional[str] = Field(None, max_length=100, description="Network group identifier (from stations table)")

    # Fields from StationVisitPostgreSQL (stations_visit)
    visit_year: Optional[str] = Field("", description="Year of station visit (from stations_visit table). Defaults to empty string if null.") # Default to empty string
    visit_count: Optional[int] = Field(None, description="Count of visits (from stations_visit table)")

    # Fields from StationDominantDataQualityPostgreSQL (stations_dominant_data_quality)
    dominant_data_quality: Optional[str] = Field(None, description="Dominant data quality (from stations_dominant_data_quality table)")

    class Config:
        from_attributes = True

class CombinedStationDataBase(BaseModel):
    """
    **Combined Station Data from MySQL and PostgreSQL Databases**

    This schema provides a unified view of station metadata by combining relevant
    information from both the MySQL `tb_slmon` table and multiple PostgreSQL tables
    (`stations`, `stations_visit`, `stations_dominant_data_quality`). It flattens
    the data into a single, comprehensive structure.

    Attributes:
    - **station_code** (`str`): Unique identifier for the station, originating from MySQL's `kode_sensor` and also used as the join key for PostgreSQL data.
    - **network** (`Optional[str]`): Network identifier (from PostgreSQL).
    - **latitude** (`Optional[Decimal]`): Geographic latitude (from PostgreSQL, falls back to MySQL's `lat_sensor` if not found in PG).
    - **longitude** (`Optional[Decimal]`): Geographic longitude (from PostgreSQL, falls back to MySQL's `lon_sensor` if not found in PG).
    - **province** (`Optional[str]`): Province name (from PostgreSQL).
    - **location** (`Optional[str]`): Location description (from PostgreSQL, falls back to MySQL's `lokasi_sensor` if not found in PG).
    - **year** (`Optional[int]`): Year of station installation (from PostgreSQL).
    - **upt** (`Optional[str]`): UPT (Unit Pelaksana Teknis) identifier (from PostgreSQL).
    - **balai** (`Optional[int]`): Balai identifier (from PostgreSQL, falls back to MySQL's `balai` if not found in PG).
    - **digitizer_type** (`Optional[str]`): Type of digitizer used (from PostgreSQL).
    - **communication_type** (`Optional[str]`): Type of communication used (from PostgreSQL).
    - **network_group** (`Optional[str]`): Network group identifier (from PostgreSQL).
    - **visit_year** (`Optional[str]`): Year of station visit (from PostgreSQL `stations_visit`).
    - **visit_count** (`Optional[int]`): Count of visits (from PostgreSQL `stations_visit`).
    - **dominant_data_quality** (`Optional[str]`): Dominant data quality (from PostgreSQL `stations_dominant_data_quality`).
    - **geo** (`Optional[str]`): Geographical information URL/path (from MySQL).
    - **vs30** (`Optional[str]`): Vs30 data URL/path (from MySQL).
    - **photo** (`Optional[str]`): Photo URL/path (from MySQL).
    - **hvsr** (`Optional[str]`): Horizontal-to-Vertical Spectral Ratio (HVSR) data URL/path (from MySQL).
    - **psd** (`Optional[str]`): Power Spectral Density (PSD) data URL/path (from MySQL).

    Config:
    - `from_attributes = True`: Enables mapping from ORM models (SQLAlchemy) to Pydantic models.
    """
    # 1. station_code (common key from MySQL's kode_sensor, alias it for clarity)
    station_code: str = Field(..., description="Unique identifier for the station, from MySQL's kode_sensor")
    # Fields from PostgreSQL (all Optional, as a match might not exist)
    network: Optional[str] = Field(None, description="Network identifier (from PostgreSQL)")
    latitude: Optional[Annotated[Decimal, condecimal(max_digits=9, decimal_places=7)]] = Field(None, description="Geographic latitude (from PostgreSQL)")
    longitude: Optional[Annotated[Decimal, condecimal(max_digits=8, decimal_places=5)]] = Field(None, description="Geographic longitude (from PostgreSQL)")
    province: Optional[str] = Field(None, max_length=50, description="Province name (from PostgreSQL)")
    location: Optional[str] = Field(None, max_length=100, description="Location description (from PostgreSQL)")
    year: Optional[int] = Field(None, description="Year of station installation (from PostgreSQL)")
    upt: Optional[str] = Field(None, max_length=100, description="UPT (Unit Pelaksana Teknis) identifier (from PostgreSQL)")
    balai: Optional[int] = Field(None, description="Balai identifier (from PostgreSQL)")
    digitizer_type: Optional[str] = Field(None, max_length=100, description="Type of digitizer used (from PostgreSQL)")
    communication_type: Optional[str] = Field(None, max_length=100, description="Type of communication used (from PostgreSQL)")
    network_group: Optional[str] = Field(None, max_length=100, description="Network group identifier (from PostgreSQL)")

    # FIELDS FROM stations_visit (PostgreSQL)
    visit_year: Optional[str] = Field(None, description="Year of station visit (from PostgreSQL stations_visit)")
    visit_count: Optional[int] = Field(None, description="Count of visits (from PostgreSQL stations_visit)")

    # FIELDS FROM stations_dominant_data_quality (PostgreSQL)
    dominant_data_quality: Optional[str] = Field(None, description="Dominant data quality (from PostgreSQL stations_dominant_data_quality)")

    # Fields from MySQL
    geo: Optional[str] = Field(None, max_length=300, description="Geographical information (from MySQL)")
    vs30: Optional[str] = Field(None, max_length=300, description="Vs30 data (from MySQL)")
    photo: Optional[str] = Field(None, max_length=300, description="Photo URL/path (from MySQL)")
    hvsr: Optional[str] = Field(None, max_length=300, description="HVSR data (from MySQL)")
    psd: Optional[str] = Field(None, max_length=300, description="PSD data (from MySQL)")

    class Config:
        from_attributes = True

class StationSensorBase(BaseModel):
    """
    **Station Sensor Information**

    This schema defines the details for a seismic station's sensor, including
    its unique code, physical location, communication channel, and sensor type.

    Attributes:
    - **code** (`Optional[str]`): Unique code for the station sensor.
    - **location** (`Optional[str]`): Geographic or physical location description of the sensor.
    - **channel** (`Optional[str]`): The communication or data channel associated with the sensor (e.g., HHZ, HHE, HHN).
    - **sensor** (`Optional[str]`): The type or specific model name of the sensor.

    Config:
    - `from_attributes = True`: Enables mapping from ORM models (SQLAlchemy) to Pydantic models.
    """
    code: Optional[str] = Field(None, description="Unique code for the station sensor")
    location: Optional[str] = Field(None, description="Geographical location of the sensor")
    channel: Optional[str] = Field(None, description="Communication channel of the sensor")
    sensor: Optional[str] = Field(None, description="Type or name of the sensor")

    class Config:
        from_attributes = True

# Pydantic model for StationSensorLatency data (input/output)
class StationSensorLatencyBase(BaseModel):
    """
    **Station Sensor Latency Data**

    This schema represents a single record of latency for a seismic station's
    sensor channel. Latency indicates the delay in data transmission.

    Attributes:
    - **net** (`Optional[str]`): Network code of the station.
    - **sta** (`Optional[str]`): Station code.
    - **datetime** (`Optional[datetime_cls]`): Timestamp when the latency record was captured.
    - **channel** (`Optional[str]`): The specific channel (e.g., HHZ, HHE) for which latency is recorded.
    - **last_time_channel** (`Optional[datetime_cls]`): The last time data was successfully received on this channel.
    - **latency** (`Optional[int]`): The latency value in milliseconds.
    - **color_code** (`Optional[str]`): A color code (e.g., "green", "yellow", "red") indicating the severity or status of the latency.

    Config:
    - `from_attributes = True`: Enables mapping from ORM models (SQLAlchemy) to Pydantic models.
    """
    net: Optional[str] = Field(None, max_length=50, description="Network code")
    sta: Optional[str] = Field(None, max_length=50, description="Station code")
    datetime: Optional[datetime_cls] = Field(None, description="Timestamp of the latency record")
    channel: Optional[str] = Field(None, max_length=50, description="Channel name")
    last_time_channel: Optional[datetime_cls] = Field(None, description="Last time data was received on the channel")
    latency: Optional[int] = Field(None, description="Latency value in milliseconds")
    color_code: Optional[str] = Field(None, max_length=20, description="Color code indicating latency status")

    class Config:
        from_attributes = True

# New Pydantic model for the desired output format: {datetime: latency}
class StationSensorLatencyOutputBase(BaseModel):
    """
    **Station Sensor Latency Output Format**

    This schema is designed specifically for an API endpoint that returns
    latency data as a mapping of timestamps to latency values. It simplifies
    the `StationSensorLatencyBase` to only include the `datetime` and `latency` fields.

    Attributes:
    - **datetime** (`datetime_cls`): The timestamp of the latency record.
    - **latency** (`int`): The latency value in milliseconds.

    This model is typically used when the API response directly provides a dictionary
    where the key is the datetime and the value is the latency, like so:
    `{ "2023-01-01T10:00:00": 50, "2023-01-01T10:01:00": 60 }`.
    """
    datetime: datetime_cls = Field(..., description="Timestamp of the latency record")
    latency: int = Field(..., description="Latency value in milliseconds")

class StationSiteQualityBase(BaseModel):
    """
    **Station Site Quality and Computed Geometry**

    This schema represents the quality assessment of a station's site,
    integrating various environmental and operational parameters. It also
    dynamically computes the station's geographic geometry based on its
    associated `station_metadata`.

    Attributes:
    - **station_metadata** (`MetadataPostgreSQLBase`): The full PostgreSQL metadata for the station.
      This field is `exclude=True` from the Pydantic output, meaning it's used
      internally for computation but not serialized in the API response.
    - **code** (`str`): The unique station code.
    - **geology** (`Optional[str]`): Description of the local geology, defaulting to "Unknown".
    - **geoval** (`Optional[int]`): Numeric value associated with geology assessment.
    - **vs30** (`Optional[str]`): Description or value of Vs30 (shear wave velocity at 30 meters depth), defaulting to "Unknown".
    - **vs30val** (`Optional[int]`): Numeric value associated with Vs30 assessment.
    - **photovoltaic** (`Optional[str]`): Status or details about the photovoltaic (solar power) system, defaulting to "Unknown".
    - **photoval** (`Optional[int]`): Numeric value associated with photovoltaic assessment.
    - **hvsr** (`Optional[float]`): Horizontal-to-Vertical Spectral Ratio (HVSR) value.
    - **hvsrval** (`Optional[int]`): Numeric value associated with HVSR assessment.
    - **psd** (`Optional[float]`): Power Spectral Density (PSD) value.
    - **psdval** (`Optional[int]`): Numeric value associated with PSD assessment.
    - **score** (`Optional[float]`): Overall site quality score.
    - **site_quality** (`Optional[str]`): General qualitative assessment of the site quality, defaulting to "Unknown".

    Computed Fields:
    - **geometry** (`Optional[GeometryBase]`): A dynamically computed `GeometryBase` object representing
      the station's point location (`[longitude, latitude, 1.0]`). This field is
      derived from the `latitude` and `longitude` in `station_metadata`. It will
      be `None` if `station_metadata` or its coordinates are missing.

    Config:
    - `from_attributes = True`: Enables mapping from ORM models (SQLAlchemy) to Pydantic models.
    """
    station_metadata: MetadataPostgreSQLBase = Field(..., exclude=True)
    code: str = Field(..., description="The unique station code.")
    geology: Optional[str] = Field("Unknown", description="Description of the local geology.")
    geoval: Optional[int] = Field(0, description="Numeric value associated with geology assessment.")
    vs30: Optional[str] = Field("Unknown", description="Description or value of Vs30 (shear wave velocity at 30 meters depth).")
    vs30val: Optional[int] = Field(0, description="Numeric value associated with Vs30 assessment.")
    photovoltaic: Optional[str] = Field("Unknown", description="Status or details about the photovoltaic (solar power) system.")
    photoval: Optional[int] = Field(0, description="Numeric value associated with photovoltaic assessment.")
    hvsr: Optional[float] = Field(0.0, description="Horizontal-to-Vertical Spectral Ratio (HVSR) value.")
    hvsrval: Optional[int] = Field(0, description="Numeric value associated with HVSR assessment.")
    psd: Optional[float] = Field(0.0, description="Power Spectral Density (PSD) value.")
    psdval: Optional[int] = Field(0, description="Numeric value associated with PSD assessment.")
    score: Optional[float] = Field(0.0, description="Overall site quality score.")
    site_quality: Optional[str] = Field("Unknown", description="General qualitative assessment of the site quality.")

    @computed_field
    @property
    def geometry(self) -> Optional[GeometryBase]:
        """
        Computes the geographic geometry (Point) of the station.

        Returns:
            Optional[GeometryBase]: A GeometryBase object if latitude and longitude
                                    are available in station_metadata, otherwise None.
        """
        if hasattr(self, 'station_metadata') and self.station_metadata:
            if self.station_metadata.latitude is not None and self.station_metadata.longitude is not None:
                return GeometryBase(
                    type="Point",
                    coordinates=[float(self.station_metadata.longitude), float(self.station_metadata.latitude), 1.0] # Assuming 1.0 for altitude if not explicitly provided
                )
        return None

    class Config:
        from_attributes = True