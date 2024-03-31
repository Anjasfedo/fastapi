from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from .koneksi import Base

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, nullable=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    is_publish = Column(Boolean, server_default="False")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()"))
