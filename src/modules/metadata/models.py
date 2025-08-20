from sqlalchemy import BigInteger, Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.core.database import Base_mysql, Base_pg


# -- MYSQL Table Model --
class MetadataMySQL(Base_mysql):
    __tablename__ = 'tb_slmon'

    no_urut = Column(Integer, primary_key=True)
    kode_sensor = Column(String(30))
    lokasi_sensor = Column(String(300))
    lat_sensor = Column(String(30))
    lon_sensor = Column(String(30))
    sistem_sensor = Column(String(60))
    pj_sensor = Column(String(30))
    balai = Column(String(30))
    ket_sensor = Column(String(60))
    status_sensor = Column(String(30))
    last_data = Column(String(60))
    pic = Column(String(30))
    sta_mag = Column(String(15))
    geo = Column(String(300))
    vs30 = Column(String(300))
    photo = Column(String(300))
    hvsr = Column(String(300))
    psd = Column(String(300))
    nilai = Column(String(10))
    keterangan2 = Column(String(100))
    gval = Column(Integer)
    vval = Column(Integer)
    pval = Column(Integer)
    hval = Column(Integer)
    psdval = Column(Integer)
    sensormerk = Column(String(50))
    digitizermerk = Column(String(50))

    def __repr__(self):
        return f"<MetadataSQES(no_urut={self.no_urut}, kode_sensor='{self.kode_sensor}')>"
    

## -- POSTGRESQL Table Model --
class MetadataPostgreSQL(Base_pg):
    __tablename__ = 'stations'

    code = Column(String(10), primary_key=True, nullable=False, comment="Station Unique identifier code")
    network = Column(String(10), nullable=False, comment="Network identifier")
    latitude = Column(Numeric(precision=9, scale=7), nullable=False, comment="Geographic latitude")
    longitude = Column(Numeric(precision=8, scale=5), nullable=False, comment="Geographic longitude")
    province = Column(String(50), nullable=True, comment="Province name")
    location = Column(String(100), nullable=True, comment="Location description")
    year = Column(Integer, nullable=True, comment="Year of station installation")
    upt = Column(String(100), nullable=True, comment="UPT (Unit Pelaksana Teknis) identifier")
    balai = Column(Integer, nullable=True, comment="Balai identifier")
    digitizer_type = Column(String(100), nullable=True, comment="Type of digitizer used")
    communication_type = Column("communication_type", String(100), nullable=True, comment="Type of communication used")
    network_group = Column(String(100), nullable=True, comment="Network group identifier")

    data_quality = relationship("StationsDataQualityPostgreSQL", back_populates="station_metadata")
    site_quality = relationship("StationSiteQualityPostgreSQL", back_populates="station_metadata", uselist=False)

    def __repr__(self):
        return f"<PostgreSQLTable(code='{self.code}', network='{self.network}')>"

class StationSensorPostgreSQL(Base_pg):
    __tablename__ = 'stations_sensor'
    # id = Column(Integer, primary_key=True, nullable=False)
    code = Column(String, nullable=True, primary_key = True)
    location = Column(String, nullable=True, primary_key = True)
    channel = Column(String, nullable=True, primary_key = True)
    sensor = Column(String, nullable=True)

    def __repr__(self):
        return f"<StationSensor(id={self.id}, code='{self.code}', location='{self.location}', channel='{self.channel}', sensor='{self.sensor}')>"

class StationSensorLatencyPostgreSQL(Base_pg):
    __tablename__ = "stations_sensor_latency"

    id = Column(Integer, primary_key=True, nullable=False)
    net = Column(String(50), nullable=True)
    sta = Column(String(50), nullable=True)
    datetime = Column(DateTime, nullable=True)
    channel = Column(String(50), nullable=True)
    last_time_channel = Column(DateTime, nullable=True)
    latency = Column(Integer, nullable=True)
    color_code = Column(String(20), nullable=True)

    def __repr__(self):
        return (
            f"<StationSensorLatency(id={self.id}, net='{self.net}', "
            f"sta='{self.sta}', channel='{self.channel}, latency='{self.latency}')>"
        )

class StationVisitPostgreSQL(Base_pg):
    __tablename__ = "stations_visit"

    code = Column(String, primary_key=True, nullable=False) 
    visit_year = Column(String, nullable=True)
    visit_count = Column(BigInteger, nullable=True) 

    def __repr__(self):
        return (
            f"<StationVisit(code='{self.code}', visit_year='{self.visit_year}', visit_count='{self.visit_count}')>"
        )

class StationDominantDataQualityPostgreSQL(Base_pg):
    __tablename__ = "stations_dominant_data_quality"

    code = Column(String, primary_key=True, nullable=False) 
    dominant_data_quality = Column(String, nullable=True)

    def __repr__(self):
        return (
            f"<StationDominantDataQuality(code='{self.code}', dominant_data_quality='{self.dominant_data_quality}')>"
        )
    
class StationSiteQualityPostgreSQL(Base_pg):
    __tablename__ = "stations_site_quality"

    code = Column(String(50), ForeignKey('stations.code'), primary_key=True, nullable=False)
    geology = Column(String(255), nullable=True)
    geoval = Column(Integer, nullable=True)
    vs30 = Column(String(255), nullable=True)
    vs30val = Column(Integer, nullable=True)
    photovoltaic = Column(String(255), nullable=True)
    photoval = Column(Integer, nullable=True)
    hvsr = Column(Numeric(precision=5, scale=2), nullable=True) 
    hvsrval = Column(Integer, nullable=True)
    psd = Column(Numeric(precision=5, scale=2), nullable=True)   
    psdval = Column(Integer, nullable=True)
    score = Column(Numeric(precision=5, scale=2), nullable=True)  
    site_quality = Column(String(255), nullable=True)

    data_quality = relationship("StationsDataQualityPostgreSQL", 
                                back_populates="station_site_quality",
                                overlaps="station_metadata,data_quality")   
    station_metadata = relationship("MetadataPostgreSQL", 
                                    back_populates="site_quality", 
                                    )

    def __repr__(self):
        return (
            f"<StationSiteQualityPostgreSQL(code='{self.code}', "
            f"site_quality='{self.site_quality}')>"
        )