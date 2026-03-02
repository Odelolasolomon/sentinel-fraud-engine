# Continuous Authentication & Behavioural Biometrics (System2)

Enterprise-grade continuous verification platform for financial institutions.

## 🧠 Key Features

### 1. Passive Behavioral Telemetry
- **SDK Data Capture**: Collects finger pressure, swipe velocity, typing cadence (inter-key delay), and device orientation (pitch/roll).
- **Behavioral Embedding Vectors**: Transforms raw telemetry into deep-learning inspired embeddings for long-term user fingerprinting.

### 2. Continuous Session Monitoring
- **Similarity Scoring**: Real-time evaluation of the current behavioral profile against the stored "Golden" profile using **Cosine Similarity**.
- **Dynamic Friction**: Automatically triggers Step-up Authentication (Biometrics/MFA) or session termination upon behavioral mismatch.
- **Frictionless Access**: Reduces static login prompts for trusted users by maintaining high identity confidence scores passively.

## ⚙️ Tech Stack

- **Backend**: FastAPI, SciPy (Spatial distance calculation), NumPy (Matrix math).
- **Frontend**: React 18 (TS), Recharts (Radar/RadarChart visualizer), Framer Motion (State-based animations).
- **Production**: Docker Compose & Netlify/Serverless ready.

## 🚀 Deployment

1.  **Backend**: `cd backend && pip install -r requirements.txt && python -m app.main`
2.  **Frontend**: `cd frontend && npm install && npm run dev`

---
**Designed for institutional-level session security.**
