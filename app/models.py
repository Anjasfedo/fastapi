from sqlalchemy import Column, String, Integer, Boolean
from .koneksi import Base

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    is_publish = Column(Boolean, default=False)
