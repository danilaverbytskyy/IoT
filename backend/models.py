from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Integer,
    SmallInteger,
    Float,
)
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


class SensorData(Base):
    __tablename__ = "sensors_data"

    __table_args__ = (
        CheckConstraint(
            "mote_id BETWEEN 1 AND 55",
            name="ck_sensors_data_mote_id",
        ),
        CheckConstraint(
            "temperature BETWEEN -60 AND 60",
            name="ck_sensors_data_temperature",
        ),
        CheckConstraint(
            "humidity BETWEEN 0 AND 100",
            name="ck_sensors_data_humidity",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    datetime: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=False),
        nullable=True,
    )

    epoch: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    mote_id: Mapped[int | None] = mapped_column(
        SmallInteger,
        nullable=True,
    )

    temperature: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    humidity: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    light: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    voltage: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )
