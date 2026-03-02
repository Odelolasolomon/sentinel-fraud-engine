from fastapi import APIRouter, HTTPException, Depends, Security
from fastapi.security import APIKeyHeader
from typing import List
from ..models.schemas import IdentityData, RiskAssessment, DeviceAssessment, BehavioralData
from ..services.fraud_engine import FraudEngine
from ..core.config import settings

from sqlalchemy.orm import Session
from ..core.security import get_api_key
from ..db.session import get_db
from ..crud import risk as crud
from ..core.logger import logger

router = APIRouter()
fraud_engine = FraudEngine()

@router.post("/assess", response_model=RiskAssessment, dependencies=[Depends(get_api_key)])
async def assess_risk(
    identity: IdentityData, 
    behavioral: BehavioralData, 
    device: DeviceAssessment,
    db: Session = Depends(get_db)
):
    """
    Main Risk-Assessment Logic. Validates identity clusters and ATO signals.
    Persists all assessments for forensic auditing.
    """
    try:
        # Check for existing identity context
        existing_id = crud.get_identity(db=db, id=identity.id)
        if not existing_id:
            logger.info(f"New identity detected. Registering: {identity.id}")
            crud.create_identity(db=db, identity=identity)
        
        # Calculate Current Risk Score
        assessment = fraud_engine.assess_risk(identity, behavioral, device)
        
        # Persist Assessment for audit
        crud.create_risk_assessment(db=db, assessment=assessment, identity_id=identity.id)
        
        # Internal state update (Graph)
        fraud_engine.add_identity(identity)
        
        return assessment
    except Exception as e:
        logger.error(f"Risk Engineering Fail: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Analytical Error")

@router.get("/threats", response_model=List[RiskAssessment])
async def list_threats(db: Session = Depends(get_db)):
    """Retrieves the most recent threat assessments for dashboard visualization."""
    return crud.get_recent_assessments(db=db)
