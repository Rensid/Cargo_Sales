from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.base import main_database
from app.schemas import Cargos, TariffCreate, Tariffs
from app.crud import create_tariff, get_tariff, get_tariff_by_type_and_date, update_tariff, delete_tariff
from app.logger import kafka_logger
from app.exceptions import TariffNotFound, TariffConflict
app = FastAPI()


async def lifespan(app: FastAPI):
    await main_database.init_models()
    yield


@app.post("/tariffs/", status_code=status.HTTP_201_CREATED)
async def add_tariffs(
    data: Tariffs,
    session: AsyncSession = Depends(main_database.get_async_session)
):
    try:
        created_tariffs = []
        for date, rates in data.root.items():
            for rate in rates:
                tariff = TariffCreate(
                    date=date,
                    cargo_type=rate.cargo_type,
                    rate=rate.rate
                )
                new_tariff = await create_tariff(session, tariff)
                created_tariffs.append(new_tariff)
                kafka_logger.log_action(
                    action="create_tariff",
                    details=tariff.dict(),
                )
        return {"created_tariffs": created_tariffs}
    except TariffConflict as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(e)
        )


@app.post('/calculate-insuarence/')
async def calculate_insurance(
    data: Cargos,
    session: AsyncSession = Depends(main_database.get_async_session)
):
    try:
        cargo_types_and_dates = {(cargo.cargo_type, datetime.strptime(cargo.date, '%Y-%m-%d')): cargo.declared_value
                                 for cargo in data.cargo}
        result = await get_tariff_by_type_and_date(session,
                                                   cargo_types_and_dates)
        response = {}
        for (material, date), value in cargo_types_and_dates.items():
            key = f"{material}, {date.strftime('%Y-%m-%d')}"
            if key in result:
                response[key] = value * result[key]
        kafka_logger.log_action(
            action="calculate_insurance",
            details=f"Entering data: {data}. \n Output data: {response}.",
        )
        return response
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@ app.put("/tariffs/")
async def update_tariff_handler(
    data: Tariffs, session: AsyncSession = Depends(main_database.get_async_session)
):
    try:
        updated_tariffs = []
        for date, rates in data.root.items():
            for rate in rates:
                tariff = TariffCreate(
                    date=date,
                    cargo_type=rate.cargo_type,
                    rate=rate.rate
                )
                new_tariff = await update_tariff(session, tariff)
                updated_tariffs.append(new_tariff)
                kafka_logger.log_action(
                    action="create_tariff",
                    details=tariff.dict()
                )
        return {"updated_tariffs": updated_tariffs}
    except TariffConflict as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(e)
        )


@ app.delete("/tariffs/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tariff_handler(data: Tariffs, session: AsyncSession = Depends(main_database.get_async_session)):
    try:
        for date, rates in data.root.items():
            for rate in rates:
                tariff = TariffCreate(
                    date=date,
                    cargo_type=rate.cargo_type,
                    rate=rate.rate
                )
                await delete_tariff(session, tariff)
            kafka_logger.log_action(
                action="delete_tariff_handler",
                details=tariff.dict(),
            )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
