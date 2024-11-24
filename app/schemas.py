from pydantic import BaseModel, RootModel
from datetime import date
from typing import List, Dict


class TariffItem(BaseModel):
    cargo_type: str
    rate: float


class Tariffs(RootModel[Dict[str, List[TariffItem]]]):  # Используй RootModel
    pass


class TariffCreate(BaseModel):
    date: date
    cargo_type: str
    rate: float


class Cargo(BaseModel):
    cargo_type: str
    date: str
    declared_value: int


class Cargos(BaseModel):
    cargo: List[Cargo]
