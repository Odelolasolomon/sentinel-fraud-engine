import pytest
import numpy as np
from app.services.biometric_engine import BiometricEngine
from app.models.schemas import BiometricTelemetry

@pytest.fixture
def engine():
    return BiometricEngine()

def test_biometric_profile_learning(engine):
    user_id = "test_user_01"
    
    # 5 identical telemetry events to establish 'perfect' baseline
    telemetry = [
        BiometricTelemetry(
            user_id=user_id, session_id="s1", orientation_pitch=0.5,
            orientation_roll=0.1, finger_pressure_avg=0.5,
            swipe_velocity_avg=1.0, typing_cadence_ms=[100, 110, 105]
        ) for _ in range(5)
    ]
    
    engine.update_profile(user_id, telemetry)
    
    # Current vector should be normalized [0.5, 0.1, 0.5, 1.0, 105]
    # L2 norm ~= sqrt(0.25+0.01+0.25+1.0+11025) which is huge, normalized it's near [0, 0, 0, 0, 1]
    
    res = engine.assess_session(telemetry[0])
    # Perfectly match should have high similarity
    assert res.similarity_score > 0.99
    assert res.threat_level == "SECURE"

def test_biometric_deviance_detection(engine):
    user_id = "target_user"
    
    # Golden Baseline: High pressure, fast swipe
    baseline = [
        BiometricTelemetry(
            user_id=user_id, session_id="base", orientation_pitch=0.1,
            orientation_roll=0.1, finger_pressure_avg=0.9,
            swipe_velocity_avg=2.0, typing_cadence_ms=[80, 85, 82]
        ) for _ in range(5)
    ]
    engine.update_profile(user_id, baseline)
    
    # Deviant Telemetry: Light pressure, slow swipe, slow typing
    hijacker = BiometricTelemetry(
        user_id=user_id, session_id="hijack_s1", orientation_pitch=0.8,
        orientation_roll=0.5, finger_pressure_avg=0.1,
        swipe_velocity_avg=0.2, typing_cadence_ms=[500, 480, 520]
    )
    
    res = engine.assess_session(hijacker)
    
    # Should trigger step-up or termination
    assert res.similarity_score < 0.75
    assert res.threat_level in ["MEDIUM/RISK", "CRITICAL/HIJACK"]
    assert res.action in ["CHALLENGE (STEP-UP)", "TERMINATE_SESSION"]
