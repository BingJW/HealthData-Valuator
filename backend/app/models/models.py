"""Canonical schema shared by the API and database initialization."""
from sqlalchemy import Column, Integer, String, Float, DateTime
from app.core.database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    password = Column(String(255))
    hospital = Column(String(200))
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)

class Evaluation(Base):
    __tablename__ = 'evaluations'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200))
    description = Column(String(500), nullable=True)
    total_value = Column(Float, default=0.0)
    indicators = Column(String(5000))
    created_at = Column(String(50))
    status = Column(String(50), default='completed')
    username = Column(String(50), nullable=True, index=True)

class LoginSession(Base):
    __tablename__ = 'login_sessions'
    token_hash = Column(String(64), primary_key=True)
    username = Column(String(50), nullable=False, index=True)
    expires_at = Column(DateTime, nullable=False, index=True)

class WeightSetting(Base):
    __tablename__ = 'weight_settings'
    category = Column(Integer, primary_key=True)
    value = Column(Float, nullable=False)
