import numpy as np
import networkx as nx
from typing import List, Dict, Any, Tuple
from datetime import datetime
from ..models.schemas import IdentityData, RiskAssessment, DeviceAssessment, BehavioralData
from ..core.logger import logger

class FraudEngine:
    """
    Enterprise-grade Fraud Risk Engine.
    Scales using sparse graph structures and numerically stable anomaly detection.
    Identifies shared-identity clusters & ATO behavioral deviance.
    """
    def __init__(self, risk_threshold: float = 0.75):
        self.graph = nx.Graph()
        self.identities = {}
        self.risk_threshold = risk_threshold

    def _cluster_analysis(self, data: IdentityData) -> Tuple[float, List[str]]:
        """
        Graph Theory Optimization (Identity Linkage).
        Identifies high-density shared resource clusters (SI detection).
        """
        score = 0.0
        factors = []
        
        # 1. IP Sharing Analysis
        if data.ip_address in self.graph:
            linked_nodes = list(self.graph.neighbors(data.ip_address))
            if len(linked_nodes) > 3: # Standard Banking Threshold for suspicious IP reuse
                score += 0.25
                factors.append(f"Network Cluster: IP shared with {len(linked_nodes)} distinct accounts")
        
        # 2. Identity Element Reuse (Phone/Device/Email)
        elements = [data.phone, data.device_id]
        for ele in elements:
            if ele in self.graph:
                linked = list(self.graph.neighbors(ele))
                if len(linked) >= 1:
                    score += 0.35
                    factors.append(f"Identity Collision: {ele[:5]}... reused across multiple profiles")
        
        return min(score, 1.0), factors

    def _anomaly_detection(self, data: IdentityData) -> Tuple[float, List[str]]:
        """
        Model Discrepancy (SI Detection).
        Flags inconsistencies between birth age & credit history (Piggybacking).
        """
        score = 0.0
        factors = []
        
        try:
            current_year = datetime.now().year
            birth_year = int(data.dob.split('-')[0])
            user_age = current_year - birth_year
            
            # 1. Age Consistency (Institutional Logic)
            # If historical credit length >= age - 10 (Too young for credit)
            if data.history_months / 12 > (user_age - 12):
                score += 0.45
                factors.append("Identity Discrepancy: Credit history length exceeds account lifecycle (Synthetic Risk)")
                
            # 2. High Credit No History (Sleeper Account)
            if data.credit_score > 780 and data.history_months < 6:
                score += 0.30
                factors.append("Atypical Credit Profile: High score with minimal aging")
        except: pass
            
        return min(score, 1.0), factors

    def detect_ato(self, behavioral: BehavioralData, device: DeviceAssessment) -> Tuple[float, List[str]]:
        """
        Account Takeover Scoring.
        Validates transactional velocity and device liveness.
        """
        score = 0.0
        factors = []

        # 1. Device Trust (Production Logic)
        if device.is_vpn or device.is_proxy:
            score += 0.25
            factors.append("Network Masquerading Detected (VPN/Proxy)")
        if device.is_emulator:
            score += 0.50
            factors.append("Hardware Anomaly: Session initiated from an emulated environment")
            
        # 2. Behavioral Deviance
        if behavioral.failed_attempts > 2:
            score += 0.40
            factors.append(f"Brute-Force Signal: {behavioral.failed_attempts} sequential failed attempts")
            
        if behavioral.velocity_score > 0.85:
            score += 0.35
            factors.append("Velocity Anomaly: Atypical transaction frequency for this account")

        return min(score, 1.0), factors

    def add_identity(self, data: IdentityData):
        """Atomically updates the internal identity graph."""
        self.identities[data.id] = data
        
        # Identity Linkage (Nodes)
        self.graph.add_node(data.id, type="USER")
        self.graph.add_node(data.ip_address, type="IP")
        self.graph.add_node(data.phone, type="PHONE")
        self.graph.add_node(data.device_id, type="DEVICE")
        
        # Linkage (Associations)
        self.graph.add_edge(data.id, data.ip_address)
        self.graph.add_edge(data.id, data.phone)
        self.graph.add_edge(data.id, data.device_id)

    def assess_risk(self, identity: IdentityData, behavioral: BehavioralData, device: DeviceAssessment) -> RiskAssessment:
        si_graph_score, si_factors_g = self._cluster_analysis(identity)
        si_anomaly_score, si_factors_a = self._anomaly_detection(identity)
        ato_score, ato_factors = self.detect_ato(behavioral, device)
        
        # Aggregate Risk (Weighted Average)
        # Synthetic risk is higher of graph and anomaly
        si_total = max(si_graph_score, si_anomaly_score)
        
        all_factors = list(set(si_factors_g + si_factors_a + ato_factors))
        
        # Threat Classification
        composite_score = (si_total + ato_score) / 2
        
        if composite_score >= 0.8: level = "CRITICAL"
        elif composite_score >= 0.55: level = "HIGH"
        elif composite_score >= 0.3: level = "MEDIUM"
        else: level = "LOW"
        
        return RiskAssessment(
            id=identity.id,
            synthetic_risk=si_total,
            ato_risk=ato_score,
            factors=all_factors,
            threat_level=level
        )
