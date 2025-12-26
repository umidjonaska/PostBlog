from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import relationship, declarative_base, Mapped, mapped_column
from database.database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[str] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password : Mapped[str]= mapped_column(String(255))
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow)
    
    
    # Relationships
    posts: Mapped[str] = relationship("Post", back_populates="author")
    comments: Mapped[str] = relationship("Comment", back_populates="user")