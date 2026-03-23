from sqlalchemy import Column, Integer, Text, String, ForeignKey
from sqlalchemy.orm import relationship

from core.database import Base

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    post_text = Column(String, nullable=False)
    img_url = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)


    owner = relationship("User", back_populates="posts")