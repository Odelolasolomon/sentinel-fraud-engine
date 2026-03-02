from sqlalchemy.orm import Session
from datetime import datetime
from ..models.database import ProfileModel, SessionLogModel
from ..models.schemas import AuthenticationResponse, BehaviouralProfile

def get_profile(db: Session, user_id: str):
    return db.query(ProfileModel).filter(ProfileModel.user_id == user_id).first()

def create_or_update_profile(db: Session, user_id: str, embedding: list):
    db_profile = get_profile(db, user_id)
    if db_profile:
        db_profile.embedding_vector = embedding
        db_profile.last_updated = datetime.now()
    else:
        db_profile = ProfileModel(user_id=user_id, embedding_vector=embedding)
        db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

def get_profile_count(db: Session):
    return db.query(ProfileModel).count()

def log_session_verification(db: Session, response: AuthenticationResponse, user_id: str):
    log = SessionLogModel(
        session_id=response.session_id,
        user_id=user_id,
        similarity_score=response.similarity_score,
        action=response.action,
        threat_level=response.threat_level
    )
    db.add(log)
    db.commit()
    return log
