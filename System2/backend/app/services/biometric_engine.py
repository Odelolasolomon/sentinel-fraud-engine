import numpy as np
from scipy.spatial.distance import cosine
from typing import List, Dict, Optional
from datetime import datetime
from pydantic import ValidationError
from ..models.schemas import BiometricTelemetry, BehaviouralProfile, AuthenticationResponse
from ..core.logger import logger

class BiometricEngine:
    """
    Enterprise Biometric Analytics Engine.
    Handles high-concurrency behavioral embedding calculation and distance-based
    threat evaluation (Continuous Auth).
    """
    def __init__(self, high_confidence: float = 0.90, medium_confidence: float = 0.75):
        self.profiles: Dict[str, BehaviouralProfile] = {}
        self.high_confidence = high_confidence
        self.medium_confidence = medium_confidence

    def _generate_embedding_vector(self, telemetry: BiometricTelemetry) -> np.ndarray:
        """
        Calculates a 5-dimensional behavioral fingerprint.
        Standardization: Vectors are normalized to unit length.
        """
        try:
            # Prevent DivisionByZero & Handle Cold Start
            cadence_vals = telemetry.typing_cadence_ms if telemetry.typing_cadence_ms else [0]
            cadence_avg = sum(cadence_vals) / len(cadence_vals)
            
            # Vector: [pitch, roll, pressure, swipe, avg_cadence]
            vector = np.array([
                telemetry.orientation_pitch,
                telemetry.orientation_roll,
                telemetry.finger_pressure_avg,
                telemetry.swipe_velocity_avg,
                cadence_avg
            ])
            
            norm = np.linalg.norm(vector)
            return vector / (norm + 1e-10) # Numerically stable
        except Exception as e:
            logger.error(f"Embedding failure: {str(e)}")
            return np.zeros(5)

    def update_profile(self, user_id: str, historical_telemetry: List[BiometricTelemetry]):
        """
        Learning Step: Computes the 'Master' behavioral centroid.
        In financial institutions, this typically aggregates over 100+ session events.
        """
        vectors = [self._generate_embedding_vector(t) for t in historical_telemetry]
        if vectors:
            centroid = np.mean(vectors, axis=0)
            self.profiles[user_id] = BehaviouralProfile(
                user_id=user_id,
                embedding_vector=centroid.tolist(),
                last_updated=datetime.now()
            )
            logger.info(f"Learned baseline embedding for user: {user_id}")

    def assess_session(self, telemetry: BiometricTelemetry) -> AuthenticationResponse:
        """
        Main Risk Detection Algorithm (Continuous Verification).
        Compares live vectors against master centroids.
        """
        user_id = telemetry.user_id
        session_id = telemetry.session_id
        
        # Profile check (Auth fallback)
        if user_id not in self.profiles:
            logger.warning(f"No profile for {user_id}. Returning learning mode.")
            return AuthenticationResponse(
                session_id=session_id,
                similarity_score=1.0,
                is_authenticated=True,
                action="ALLOW (LEARNING)",
                threat_level="LEARNING"
            )

        current_vector = self._generate_embedding_vector(telemetry)
        profile_vector = np.array(self.profiles[user_id].embedding_vector)

        # Distance Calculation: Cosine Similarity
        try:
            # 1.0 - distance = similarity (1.0 = match, 0.0 = orthogonal)
            dist = cosine(current_vector, profile_vector)
            similarity = 1.0 - dist
        except Exception as e:
            logger.error(f"Similarity Calculation Error: {str(e)}")
            similarity = 0.5 # Suspicious default

        # State-Machine Detection logic (Production Thresholds)
        if similarity >= self.high_confidence:
            # Low friction flow (Trusted user session)
            action, level = "ALLOW", "SECURE"
            is_auth = True
        elif similarity >= self.medium_confidence:
            # Anomaly detected: Trigger Biometric Step-up (MFA)
            action, level = "CHALLENGE (STEP-UP)", "MEDIUM/RISK"
            is_auth = False
        else:
            # Critical Deviance: Immediate Session Invalidation (ATO Prevent)
            action, level = "TERMINATE_SESSION", "CRITICAL/HIJACK"
            is_auth = False
            logger.critical(f"Potential Session Hijack: {user_id} | Similarity: {similarity:.2f}")

        return AuthenticationResponse(
            session_id=session_id,
            similarity_score=float(round(similarity, 4)),
            is_authenticated=is_auth,
            action=action,
            threat_level=level
        )
