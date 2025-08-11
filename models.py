from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    telegram_user_id = Column(Integer, unique=True, nullable=False)
    stars = Column(Integer, default=0, nullable=False)

class UserAIKey(Base):
    __tablename__ = "user_keys"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    provider_name = Column(String, nullable=False)
    encrypted_api_key = Column(String, nullable=False)
    selected_model = Column(String, nullable=False)
    __table_args__ = (UniqueConstraint('user_id', 'provider_name', name='_user_provider_uc'),)
