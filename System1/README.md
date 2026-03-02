# Synthetic Identity & ATO Detection Engine (System1)

A production-grade fraud detection platform demonstrating complex identity clustering and behavioral risk assessment.

## 🚀 Key Features

### 1. Synthetic Identity (SI) Detection
- **Graph-Cluster Analytics**: Re-identifies shared IP/Phone/SSN reuse across "sleeper" accounts.
- **Anomaly Modeling**: Identifies discrepancies between identity history (credit history length) and lifecycle data (age).
- **Liveness Indicators**: Detects "bust-out" risks early via piggybacked credit relationship scoring.

### 2. Account Takeover (ATO) Prevention
- **Behavioral Deviance**: High-velocity transactional monitoring.
- **Device Trust**: Fingerprinting for VPNs, Proxies, and Emulators.
- **Friction Triggering**: Dynamic scoring determines when to challenge login vs allow through.

## 🛠 Tech Stack

- **Backend**: FastAPI (Python), NetworkX (Graph Analytics), NumPy/Pandas (Anomaly detection).
- **Frontend**: React (TS), Vite, Recharts (Visualizations), Framer Motion (Glassmorphism UI).
- **Deployment**: Docker Compose ready.

## 📦 Getting Started

1.  **Backend Startup**:
    ```bash
    cd backend
    pip install -r requirements.txt
    python -m app.main
    ```

2.  **Frontend Startup**:
    ```bash
    cd frontend
    npm install
    npm run dev
    ```

3.  **Docker (Production Build)**:
    ```bash
    docker-compose up --build
    ```

## 🏗 Directory structure
```
System1/
├── backend/
│   ├── app/ (Core logic, models, services)
│   └── Dockerfile
├── frontend/ (Modern React Dashboard)
│   └── src/ (TS Components & Glassmorphism styles)
├── docker-compose.yml
└── README.md
```

**Designed for production scalability and high-fidelity fraud alerting.**
