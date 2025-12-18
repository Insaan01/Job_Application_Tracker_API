from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    company = Column(String(255))
    role = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

    statuses = relationship("ApplicationStatusHistory", back_populates="application")


class ApplicationStatusHistory(Base):
    __tablename__ = "application_status_history"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"))
    status = Column(String(50))
    note = Column(String(255), nullable=True)
    changed_at = Column(DateTime, default=datetime.utcnow)

    application = relationship("Application", back_populates="statuses")
