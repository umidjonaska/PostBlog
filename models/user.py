from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import relationship, declarative_base, Mapped, mapped_column
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[str] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    password : Mapped[str]= mapped_column(String)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow)
    
    
    # Relationships
    posts: Mapped[str] = relationship("Post", back_populates="author")
    comments: Mapped[str] = relationship("Comment", back_populates="user")