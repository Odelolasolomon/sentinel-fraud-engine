from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .db.base_class import Base

class IdentityModel(Base):
    __tablename__ = "identities"

    id = Column(String, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String, index=True)
    phone = Column(String, index=True)
    ssn_last4 = Column(String)
    dob = Column(String)
    credit_score = Column(Integer)
    history_months = Column(Integer)
    ip_address = Column(String, index=True)
    device_id = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    assessments = relationship("RiskAssessmentModel", back_populates="identity")

class RiskAssessmentModel(Base):
    __tablename__ = "risk_assessments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    identity_id = Column(String, ForeignKey("identities.id"))
    synthetic_risk = Column(Float)
    ato_risk = Column(Float)
    factors = Column(JSON)
    threat_level = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    identity = relationship("IdentityModel", back_populates="assessments")
