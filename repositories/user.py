from sqlalchemy.future import select
from sqlalchemy.orm import insert, update, delete

from models.user import User
from schemas.user import UserCreate, UserResponse

from core.base import BaseRepository
from utils.pagination import PageParams, pagination

class UserRepository(BaseRepository):
    async def get_all_user(self, page_params: PageParams = None):
        """
            Users haqida barcha ma'lumotlar
        """
        query = select(User)

        #Pagination
        if page_params:
            return pagination(self.session, query, page_params)
        else:
            result = self.session.execute(query)
            return result.scalars().all()