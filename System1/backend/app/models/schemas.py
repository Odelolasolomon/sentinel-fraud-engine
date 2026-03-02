from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime

class IdentityData(BaseModel):
    id: str
    full_name: str
    email: str
    phone: str
    ssn_last4: str
    dob: str
    credit_score: int
    history_months: int
    ip_address: str
    device_id: str

class DeviceAssessment(BaseModel):
    device_id: str
    os: str
    is_vpn: bool
    is_proxy: bool
    is_emulator: bool
    trust_score: float

class BehavioralData(BaseModel):
    user_id: str
    last_login: datetime
    session_duration: int
    location: str
    failed_attempts: int
    velocity_score: float

class RiskAssessment(BaseModel):
    id: str
    synthetic_risk: float
    ato_risk: float
    factors: List[str]
    threat_level: str  # LOW, MEDIUM, HIGH, CRITICAL
