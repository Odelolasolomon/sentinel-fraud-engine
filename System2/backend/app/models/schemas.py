from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime

class BiometricTelemetry(BaseModel):
    user_id: str
    session_id: str
    timestamp: datetime = Field(default_factory=datetime.now)
    # Mobile Telemetry
    orientation_pitch: float  # device tilt
    orientation_roll: float
    finger_pressure_avg: float
    swipe_velocity_avg: float
    typing_cadence_ms: List[int]  # Timing between key presses

class BehaviouralProfile(BaseModel):
    user_id: str
    embedding_vector: List[float] # Trained centroid of behavioral data
    last_updated: datetime

class AuthenticationResponse(BaseModel):
    session_id: str
    similarity_score: float
    is_authenticated: bool
    action: str  # ALLOW, CHALLENGE, TERMINATE
    threat_level: str

class DeviationAlert(BaseModel):
    session_id: str
    deviation: float
    reason: str
