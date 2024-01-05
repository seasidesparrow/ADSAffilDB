try:
    from adsputils import get_date, UTCDateTime
except ImportError:
    from adsmutils import get_date, UTCDateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Table, Column, Integer, Numeric, String, TIMESTAMP,
                        ForeignKey, Boolean, Float, Text, UniqueConstraint)
from sqlalchemy.dialects.postgresql import ENUM

Base = declarative_base()

class AffilData(Base):
    """
    affil_data holds the mapping of published string and affiliation ID
    """
    __tablename__ = "affil_data"

    data_key = Column(Integer, primary_key=True, unique=True)
    data_id = Column(String(6), nullable=False)
    data_pubstring = Column(Text, nullable=False)
    data_created = Column(UTCDateTime, default=get_date)
    data_updated = Column(UTCDateTime, onupdate=get_date)


class AffilInst(Base):
    __tablename__ = "affil_inst"

    inst_key = Column(Integer, primary_key=True, unique=True)
    inst_id = Column(String(6), unique=True, nullable=False)
    inst_parents = Column(String, nullable=True)
    inst_canonical = Column(String, nullable=False)
    inst_abbreviated = Column(String, nullable=False)
    # in place of location, we could consider using GeoAlchemy2 here
    # especially if we can get lat-lon from ROR
    inst_location = Column(String, nullable=True)
    inst_country = Column(String, nullable=True)
    inst_rorid = Column(String, nullable=True)
    inst_created = Column(UTCDateTime, default=get_date)


class AffilNorm(Base):
    __tablename__ = "affil_norm"

    norm_key = Column(Integer, primary_key=True, unique=True)
    norm_id = Column(String(6), unique=False, nullable=False)
    norm_string = Column(Text, unique=True, nullable=False)


class AffilCuration(Base):
    __tablename__ = "affil_curation"

    curation_count = Column(Integer, nullable=True)
    curation_id = Column(String(6), unique=False, nullable=True)
    curation_string = Column(Text, unique=True, nullable=False)
