from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.dao.base_dao import BaseDao
from sqlalchemy.sql.expression import ColumnExpressionArgument

from typing import TypeVar, Generic, Sequence, Optional

T = TypeVar("T", bound=BaseDao)


class GenericRepository(Generic[T]):
    def __init__(self, entity, engine):
        self._dao: T = entity
        self._engine = engine
        self._session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async def get_all(self) -> Sequence[T]:
        async with self._session() as session:
            result = await session.execute(select(self._dao))
            return result.scalars().all()

    async def get_by_id(self, entity_id: int) -> T or None:
        async with self._session() as session:
            result = await session.execute(select(self._dao).filter(self._dao.id == entity_id))
            return result.scalar_one_or_none()

    async def get_by_column(self, column: ColumnExpressionArgument, value) -> Sequence[T]:
        async with self._session() as session:
            result = await session.execute(select(self._dao).filter(column == value))
            return result.scalars().all()

    async def get_first_by_column(self, column: ColumnExpressionArgument, value) -> T or None:
        async with self._session() as session:
            result = await session.execute(select(self._dao).filter(column == value))
            return result.scalar_one_or_none()

    async def get_all_by_whereclause(self, whereclause, page: Optional[int] = None,
                                     page_size: Optional[int] = None) -> Sequence[T]:
        offset, limit = None, None

        if page is not None and page_size is not None:
            if page_size <= 0 or page < 0:
                raise ValueError("Incorrect page or page_size")
            offset = page * page_size
            limit = page_size

        async with self._session() as session:
            query = select(self._dao).where(whereclause)
            if limit is not None and offset is not None:
                query = query.limit(limit).offset(offset)
            result = await session.execute(query)
            return result.scalars().all()

    async def count_by_whereclause(self, whereclause) -> int:
        async with self._session() as session:
            result = await session.execute(select(self._dao).where(whereclause))
            return len(result.scalars().all())

    async def get_one_by_whereclause(self, whereclause) -> T or None:
        async with self._session() as session:
            result = await session.execute(select(self._dao).where(whereclause))
            return result.scalar_one_or_none()

    async def add(self, entity: T) -> None:
        async with self._session() as session:
            session.add(entity)
            await session.commit()

    async def update(self, entity: T) -> None:
        async with self._session() as session:
            await session.merge(entity)
            await session.commit()

    async def delete(self, entity: T) -> None:
        async with self._session() as session:
            await session.delete(entity)
            await session.commit()
