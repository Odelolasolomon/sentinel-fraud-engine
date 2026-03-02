# 🛡️ Sentinel Fraud Engine: Enterprise Prevention Suite

An institutional-grade, AI-driven fraud prevention platform featuring specialized models for **Synthetic Identity Detection** and **Continuous Behavioural Biometrics**. 

This repository contains two distinct, production-ready systems architected for high-security financial environments.

---

## 🏗️ Project Overview

### 🛰️ System 1: Synthetic Identity & Account Takeover (ATO)
Identifies "sleeper" accounts and credit piggybacking using Graph-based cluster analysis.
*   **Graph Linking**: Detects shared IPs, Phones, and Device IDs across account boundaries using `NetworkX`.
*   **Anomaly Modeling**: Flags discrepancies between identity history (credit length) and user lifecycle (age).
-   **Dashboard**: High-end React interface with real-time threat maps and trend analytics.

### 🧬 System 2: Continuous Auth & Behavioural Biometrics
Passive session monitoring to prevent high-velocity takeover and hijacking. 
*   **Passive Telemetry**: Recording of finger pressure, swipe velocity, typing cadence, and device orientation.
*   **User Embeddings**: Calculation of 5D behavioral profiles with **Cosine Similarity** comparison against "Golden" baselines.
*   **Dynamic Friction**: Scoring engine that automatically triggers Step-up Authentication (MFA) on behavioral mismatch.

---

## 🛠️ Global Architecture (Institutional Standard)

Both systems follow an **Enterprise Factory Pattern**:
-   **Backend**: FastAPI, SQLAlchemy (Persistence), Loguru (Audit), Pydantic Settings.
-   **Security**: Header-based `X-API-TOKEN` protection.
-   **Middlewares**: Performance tracking and global exception handling.
-   **Frontend**: React (TS), Recharts Data Viz, Framer Motion animations.
-   **Testing**: Pytest suites for analytical accuracy validation.

---

## 🚀 Getting Started

Launch both platforms using **Docker Compose**:

### Monitoring System 1 (Port 3000)
```bash
cd System1
docker-compose up --build
```

### Monitoring System 2 (Port 4000)
```bash
cd System2
docker-compose up --build
```

---

## 📁 Repository Structure
```text
sentinel-fraud-engine/
├── System1/ (SI & ATO Detection)
│   ├── backend/ (Python/FastAPI)
│   ├── frontend/ (React/TS)
│   └── docker-compose.yml
├── System2/ (Biometrics & Session Auth)
│   ├── backend/ (Python/FastAPI)
│   ├── frontend/ (React/TS)
│   └── docker-compose.yml
└── README.md
```

**Designed for robustness, observability, and security.**
