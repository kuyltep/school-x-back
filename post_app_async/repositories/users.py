from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr


from core.database import get_db
from core.security import hash_password
from schemas import UserRegistrationSchema
from models import User


class UserRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def create(self, new_user: UserRegistrationSchema):
        user_dict = new_user.model_dump()
        user_dict["hashed_password"] = hash_password(new_user.password)
        user_dict.pop("password")
        db_user = User(**user_dict)

        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)

        return db_user

    async def get_by_email(self, email: str | EmailStr):
        return await self.db.query(User).filter(User.email == email).first()


    async def get_by_username(self, username: str):
        return await self.db.query(User).filter(User.username == username).first()