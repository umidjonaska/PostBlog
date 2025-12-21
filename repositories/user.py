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
        
    async def get_one_user(self, user_id: int):
        """
            Id bo'yicha user olish
        """
        query = select(User).where(User.id==user_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def create_user(self, payload: UserCreate, flush: bool = False, commit: bool = False) -> int|bool:
        """
            Yangi user yaratish
        """
        query = insert(User).values(payload)
        exc = await self.session.execute(query)

        if flush:
            await self.session.flush()
            pk = exc.inserted_primary_key
            return pk[0] if pk else False
        elif commit:
            await self.session.commit()
            return True
        
        return False
    
    async def update_user(self, user_id: int, payload: UserCreate):
        """
            Userni yangilash
        """
        query = update(User).where(User.id==user_id).values(payload)
        await self.session.execute(query)
        await self.session.commit()