from api.auth import router as auth_router
from api.posts import router as posts_router

__all__ = (
    auth_router,
    posts_router
)