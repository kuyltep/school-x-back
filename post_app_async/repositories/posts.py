from typing import List

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from models import Post


class PostRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def create(self, post_text: str, owner_id: int, img_url: str | None = None) -> Post:
        db_post = Post(post_text=post_text, owner_id=owner_id, img_url=img_url)
        self.db.add(db_post)
        await self.db.commit()
        await self.db.refresh(db_post)
        return db_post

    async def get_by_id(self, post_id: int) -> Post:
        return await self.db.query(Post).filter(Post.id == post_id).first()

    async def get_all(self) -> List[Post]:
        return await self.db.query(Post).all()

    async def delete(self, post: Post) -> None:
        self.db.delete(post)
        await self.db.commit()
