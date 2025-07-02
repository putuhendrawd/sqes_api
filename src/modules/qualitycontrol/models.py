from sqlalchemy import BigInteger, Column, ForeignKey,  String, Date, Float, ForeignKeyConstraint, String, Numeric, Integer
from sqlalchemy.orm import relationship
from src.core.database import Base_mysql, Base_pg


# -- MYSQL Table Model --
class StationsDataQualityPostgreSQL(Base_pg):
    __tablename__ = "stations_data_quality"
    __table_args__ = (
        ForeignKeyConstraint(['code'], ['stations.code']),
        ForeignKeyConstraint(['code'], ['stations_site_quality.code']),
    )

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    date = Column(Date)
    code = Column(String, ForeignKey('stations.code'), nullable=False)
    quality_percentage = Column(Float)
    result = Column(String)
    details = Column(String)

    station_metadata = relationship("MetadataPostgreSQL", 
                                    back_populates="data_quality", 
                                    primaryjoin="StationsDataQualityPostgreSQL.code == MetadataPostgreSQL.code",
                                    overlaps="data_quality")
    station_site_quality = relationship("StationSiteQualityPostgreSQL", 
                                        back_populates="data_quality",
                                          primaryjoin="StationsDataQualityPostgreSQL.code == StationSiteQualityPostgreSQL.code",
                                          overlaps="data_quality,station_metadata")

    def __repr__(self):
        return f"<StationsDataQuality(code={self.code}, quality_percentage={self.quality_percentage}, result='{self.result}')>"
    
class StationsQCDetailsPostgreSQL(Base_pg):
    __tablename__ = 'stations_qc_details'

    # All columns are marked 'Not NULL' in your image.
    # 'id' is also marked 'Primary key'.
    id = Column(String(255), primary_key=True, nullable=False) 
    code = Column(String(50), nullable=False)
    date = Column(Date, nullable=False) 
    channel = Column(String(50), nullable=False)
    rms = Column(Numeric(precision=7, scale=2), nullable=False)
    amplitude_ratio = Column(Numeric(precision=7, scale=2), nullable=False)
    availability = Column(Numeric(precision=5, scale=2), nullable=False)
    num_gap = Column(Integer, nullable=False)
    num_overlap = Column(Integer, nullable=False)
    num_spikes = Column(Integer, nullable=False)
    perc_below_nlnm = Column(Numeric(precision=5, scale=2), nullable=False)
    perc_above_nhnm = Column(Numeric(precision=5, scale=2), nullable=False)
    linear_dead_channel = Column(Numeric(precision=7, scale=2), nullable=False)
    gsn_dead_channel = Column(Numeric(precision=7, scale=2), nullable=False)
    sp_percentage = Column(Numeric(precision=5, scale=2), nullable=False)
    bw_percentage = Column(Numeric(precision=5, scale=2), nullable=False)
    lp_percentage = Column(Numeric(precision=5, scale=2), nullable=False)

    def __repr__(self):
        return (
            f"<StationsQCDetailsPostgreSQL(id='{self.id}', code='{self.code}', "
            f"date='{self.date}', channel='{self.channel}')>"
        )