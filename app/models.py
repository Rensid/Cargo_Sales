from sqlalchemy import Column, Integer, String, Float, Date, UniqueConstraint
from app.base import main_database


class Tariff(main_database.Base):
    __tablename__ = "tariffs"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    cargo_type = Column(String, nullable=False)
    rate = Column(Float, nullable=False)

    __table_args__ = (UniqueConstraint(
        "date", "cargo_type", name="_date_cargo_uc"),)
