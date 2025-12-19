
import base64
from venv import create

from fastapi import Query
from sqlalchemy.future import select
from sqlalchemy import func, text, join
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Generic, TypeVar, List, Optional

from pydantic import BaseModel

T = TypeVar("T")


class Page(BaseModel, Generic[T]):
    cursor: Optional[str] = None
    next_cursor: Optional[str] = None
    size: int
    count: int
    data: List[T]


# Paginatsiya qabul qiladigan ma'lumotlar
class PageParams:
    def __init__(
            self,
            size: int,
            cursor: Optional[str] = None
    ):
        self.cursor = cursor
        self.size = size


def get_page_params(
        cursor: Optional[str] = Query(
            None,
            description="Oxirgi ma'lumot `id`-si (Agar `0` yuborilsa, barchasi keladi.)"
        ),
        size: int = Query(
            10, ge=1, le=500, description="Har bir so'rovdagi elementlar soni"
        )
) -> PageParams:
    return PageParams(cursor=cursor, size=size)


async def pagination(
        session: AsyncSession,
        query,
        page_params: PageParams,
        scalars: bool = True,
        total_count: Optional[int] = None,
        union: bool = False
):
    cursor = page_params.cursor
    size = page_params.size

    # Jami sonini olish
    if not total_count:
        count_query = select(func.count()).select_from(query.column_descriptions[0]['entity'])
        if query.whereclause is not None:
            count_query = count_query.where(query.whereclause)

        count_result = await session.execute(count_query)
        total_count = count_result.scalar_one()

    if not union:
        query_pagination = query
        if cursor:
            if cursor != "0":
                model_class = query.column_descriptions[0]['entity']
                primary_key_column = next(
                    col for col in model_class.__table__.columns if col.primary_key
                )
                query_pagination = query.where(primary_key_column > cursor)
        else:
            query_pagination = query_pagination.limit(size)

        model_class = query.column_descriptions[0]['entity']
        primary_key_column = next(
            col for col in model_class.__table__.columns if col.primary_key
        )
        query_pagination = query_pagination.order_by(primary_key_column.asc())
    else:
        subquery = query.subquery()
        entity = subquery.c

        query_pagination = select(subquery)
        if cursor:
            if cursor != "0":
                query_pagination = (
                    query_pagination
                    .where(entity.id > cursor)
                    .limit(size)
                )
        else:
            query_pagination = query_pagination.limit(size)

        query_pagination = query_pagination.order_by(entity.id.asc())

    # Ma'lumotlarni olish
    todos_result = await session.execute(query_pagination)
    if not scalars:
        data = todos_result.unique().all()
        model_class = query.column_descriptions[0]['entity']
        primary_key_column = next(
            col for col in model_class.__table__.columns if col.primary_key
        )
        next_cursor = getattr(data[-1], primary_key_column.name) if data else None
    else:
        data = todos_result.unique().scalars().all()
        model_class = query.column_descriptions[0]['entity']
        primary_key_column = next(
            col for col in model_class.__table__.columns if col.primary_key
        )
        next_cursor = getattr(data[-1], primary_key_column.name) if data else None

    # Cursorlarni kodlash
    encoded_cursor = str(cursor) if cursor is not None else None
    encoded_next_cursor = str(next_cursor) if next_cursor is not None else None

    encoded_next_cursor = None if cursor != '0' and len(data) <= 0 else encoded_next_cursor
    encoded_next_cursor = None if cursor == '0' else encoded_next_cursor

    return Page(
        cursor=encoded_cursor,
        size=size,
        count=total_count,
        next_cursor=encoded_next_cursor,
        data=data
    )
