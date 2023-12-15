import datetime

from typing import List, Optional
from sqlalchemy.types import Integer, String, Text, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class Base(DeclarativeBase):
    type_annotation_map = {
        datetime.datetime: TIMESTAMP(timezone=True),
    }

class AffilData(Base):
    """
    affil_data holds the mapping of published string and affiliation ID
    """
    __tablename__ = "affil_data"

    affil_data_key: Mapped[int] = mapped_column(primary_key=True)
    affil_data_string: Mapped[str] = mapped_column(Text)
    affil_data_id: Mapped[str] = mapped_column(String(6))


class AffilDataHistory(Base):
    __tablename__ = "affil_data_history"

    affil_data_hist_key: Mapped[int] = mapped_column(primary_key=True)
    affil_data_modified_time: Mapped[datetime.datetime]
    affil_data_key: Mapped[int] = mapped_column(Integer)
    affil_data_string: Mapped[str] = mapped_column(Text)
    affil_data_id: Mapped[str] = mapped_column(String(6))


class AffilInst(Base):
    __tablename__ = "affil_inst"

    affil_inst_key: Mapped[int] = mapped_column(Integer)
    affil_inst_id: Mapped[str] = mapped_column(String(6))
    affil_inst_canonical: Mapped[str] = mapped_column(Text)
    affil_inst_abbreviated: Mapped[str] = mapped_column(Text)
    affil_inst_country: Mapped[str] = mapped_column(Text)


class AffilInstHistory(Base):
    __tablename__ = "affil_inst_history"

    affil_inst_hist_key: Mapped[int] = mapped_column(primary_key=True)
    affil_inst_modified_time: Mapped[datetime.datetime]
    affil_inst_key: Mapped[int] = mapped_column(primary_key=True)
    affil_string: Mapped[str] = mapped_column(Text)
    affil_id: Mapped[str] = mapped_column(String(6))


class AffilNorm(Base):
    __tablename__ = "affil_norm"

    affil_norm_key: Mapped[int] = mapped_column(primary_key=True)
    affil_norm_string: Mapped[str] = mapped_column(Text)
    affil_id: Mapped[str] = mapped_column(String(6))

