import uuid

from fastapi import Depends, HTTPException, UploadFile

from adapters.storage.base import StorageAdapter
from core.adapters import get_storage
from models import Post
from repositories import PostRepository


class PostService:
    def __init__(
            self,
            repository: PostRepository = Depends(PostRepository),
            storage: StorageAdapter = Depends(get_storage)
    ):
        self.repository = repository
        self.storage = storage


    async def create_post(self, post_text: str, owner_id: int, image: UploadFile | None = None) -> Post:
        if image is not None:
            content = image.file.read()
            ext = image.filename.split('.')[-1] if image.filename else "bin"
            if ext not in ("jpeg", "jpg", "png"):
                raise HTTPException(400, "Invalid image format")

            key = f"posts/{uuid.uuid4()}.{ext}"
            img_url = await self.storage.upload(content, key, image.content_type or "application/octet-stream")
        return await self.repository.create(post_text, owner_id, img_url)

    async def get_post(self, post_id: int) -> Post:
        post = await self.repository.get_by_id(post_id)
        if post is None:
            raise HTTPException(status_code=404, detail="Post not found")
        return post

    async def get_all_posts(self) -> list[Post]:
        return await self.repository.get_all()

    async def delete_post(self, post_id: int, current_user_id: int) -> Post:
        post = await self.repository.get_by_id(post_id)
        if post is None:
            raise HTTPException(status_code=404, detail="Post not found")
        if post.owner_id != current_user_id:
            raise HTTPException(status_code=403, detail="You are not the owner of the post")
        await self.repository.delete(post)