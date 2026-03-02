from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .db.base_class import Base

class ProfileModel(Base):
    __tablename__ = "profiles"

    user_id = Column(String, primary_key=True, index=True)
    embedding_vector = Column(JSON)
    last_updated = Column(DateTime, default=datetime.utcnow)

    sessions = relationship("SessionLogModel", back_populates="profile")

class SessionLogModel(Base):
    __tablename__ = "session_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_id = Column(String, index=True)
    user_id = Column(String, ForeignKey("profiles.user_id"))
    similarity_score = Column(Float)
    action = Column(String)
    threat_level = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    profile = relationship("ProfileModel", back_populates="sessions")
