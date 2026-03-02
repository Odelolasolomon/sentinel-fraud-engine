import pytest
from app.services.fraud_engine import FraudEngine
from app.models.schemas import IdentityData, BehavioralData, DeviceAssessment

@pytest.fixture
def engine():
    return FraudEngine()

def test_synthetic_identity_anomaly(engine):
    # Setup identity with a suspicious history vs age
    identity = IdentityData(
        id="si_test_01",
        full_name="Synthetic Alice",
        email="alice@fake.com",
        phone="+1234567890",
        ssn_last4="9999",
        dob="2010-01-01", # 14 years old
        credit_score=800,
        history_months=120, # 10 years of credit at 14? Major SI signal.
        ip_address="10.0.0.1",
        device_id="dev_01"
    )
    
    behavioral = BehavioralData(
        user_id="si_test_01",
        last_login="2024-01-01T00:00:00",
        session_duration=120,
        location="NY",
        failed_attempts=0,
        velocity_score=0.1
    )
    
    device = DeviceAssessment(
        device_id="dev_01",
        os="iOS",
        is_vpn=False,
        is_proxy=False,
        is_emulator=False,
        trust_score=0.9
    )
    
    assessment = engine.assess_risk(identity, behavioral, device)
    
    assert assessment.threat_level in ["MEDIUM", "HIGH", "CRITICAL"]
    assert any("Identity Discrepancy" in f for f in assessment.factors)

def test_graph_clustering_detect(engine):
    # Common shared element: IP_SHARED
    ip = "192.168.1.50"
    
    def create_id(uid):
        return IdentityData(
            id=uid, full_name="User", email=f"{uid}@test.com", phone="+100", 
            ssn_last4="0000", dob="1990-01-01", credit_score=700, 
            history_months=60, ip_address=ip, device_id="D"
        )

    # Add multiple identities sharing the same IP
    for i in range(5):
        engine.add_identity(create_id(f"user_{i}"))

    # New identity sharing that same IP
    new_id = create_id("new_hijacker")
    score, factors = engine._cluster_analysis(new_id)
    
    assert score > 0.2
    assert any("Network Cluster" in f for f in factors)
