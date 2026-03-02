from sqlalchemy.orm import Session
from ..models.database import IdentityModel, RiskAssessmentModel
from ..models.schemas import RiskAssessment, IdentityData

def get_identity(db: Session, id: str):
    return db.query(IdentityModel).filter(IdentityModel.id == id).first()

def create_identity(db: Session, identity: IdentityData):
    db_identity = IdentityModel(**identity.dict())
    db.add(db_identity)
    db.commit()
    db.refresh(db_identity)
    return db_identity

def create_risk_assessment(db: Session, assessment: RiskAssessment, identity_id: str):
    db_assessment = RiskAssessmentModel(
        identity_id=identity_id,
        synthetic_risk=assessment.synthetic_risk,
        ato_risk=assessment.ato_risk,
        factors=assessment.factors,
        threat_level=assessment.threat_level
    )
    db.add(db_assessment)
    db.commit()
    db.refresh(db_assessment)
    return db_assessment

def get_recent_assessments(db: Session, limit: int = 10):
    return db.query(RiskAssessmentModel).order_by(RiskAssessmentModel.created_at.desc()).limit(limit).all()
