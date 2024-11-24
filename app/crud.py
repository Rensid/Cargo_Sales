from sqlalchemy import tuple_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from app.models import Tariff
from app.logger import kafka_logger
from app.exceptions import TariffNotFound, TariffConflict
from app.schemas import TariffCreate


async def create_tariff(session: AsyncSession, tariff: TariffCreate) -> Tariff:
    new_tariff = Tariff(**tariff.dict())
    try:
        session.add(new_tariff)
        await session.commit()
        await session.refresh(new_tariff)
        kafka_logger.log_action(
            action="create_tariff",
            details=f"Response: {201}"
        )
        return new_tariff
    except IntegrityError:
        kafka_logger.log_action(
            action="create_tariff",
            details=f"Error {IntegrityError}"
        )
        await session.rollback()
        raise TariffConflict()


async def get_tariff_by_type_and_date(session, data: list) -> Tariff:
    tariffs_query = await session.execute(
        select(Tariff)
        .where(
            tuple_(Tariff.cargo_type, Tariff.date).in_(data)
        )
    )
    response = {f"{tariff.cargo_type}, {tariff.date}":
                tariff.rate for tariff in tariffs_query.scalars().all()}
    kafka_logger.log_action(
        action="get_tariff_by_type_and_date",
        details=f"Response: {response}"
    )
    return response


async def get_tariff(session: AsyncSession,
                     tariff_data: TariffCreate) -> Tariff:
    result = await session.execute(select(Tariff)
                                   .where(Tariff.date == tariff_data.date,
                                          Tariff.cargo_type == tariff_data.cargo_type))
    tariff = result.scalar_one_or_none()
    if not tariff:
        raise TariffNotFound()
    kafka_logger.log_action(
        action="get_tariff",
        details=f"Response: {tariff}"
    )
    return tariff


async def update_tariff(session: AsyncSession, tariff_data: TariffCreate) -> Tariff:
    tariff = await get_tariff(session, tariff_data)
    for key, value in tariff_data.dict().items():
        setattr(tariff, key, value)
    kafka_logger.log_action(
        action="get_tariff",
        details=f"Response: {tariff}"
    )
    await session.commit()
    await session.refresh(tariff)
    return tariff


async def delete_tariff(session: AsyncSession, tariff_data: TariffCreate) -> None:
    tariff = await get_tariff(session, tariff_data)
    await session.delete(tariff)
    await session.commit()
