import { useState, useEffect } from 'react';
import axios from 'axios';
import {
  Fingerprint,
  Smartphone,
  Wifi,
  ShieldCheck,
  AlertTriangle,
  Activity,
  Cpu,
  ArrowUpRight,
  TrendingUp,
  RotateCcw
} from 'lucide-react';
import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip
} from 'recharts';
import { motion, AnimatePresence } from 'framer-motion';

// --- MOCK DATA FOR BIOMETRICS ---
const mockProfile = [
  { subject: 'Pitch', A: 120, B: 110, fullMark: 150 },
  { subject: 'Roll', A: 98, B: 130, fullMark: 150 },
  { subject: 'Pressure', A: 86, B: 130, fullMark: 150 },
  { subject: 'Velocity', A: 99, B: 100, fullMark: 150 },
  { subject: 'Cadence', A: 85, B: 90, fullMark: 150 },
];

function App() {
  const [similarity, setSimilarity] = useState(0.92);
  const [status, setStatus] = useState<'SECURE' | 'CAUTION' | 'HIJACK'>('SECURE');
  const [telemetry, setTelemetry] = useState({
    pitch: 0.45,
    roll: 0.12,
    pressure: 0.61,
    velocity: 1.22
  });

  const [stats, setStats] = useState<any>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8001';
        const [statsRes, vectorRes] = await Promise.all([
          axios.get(`${apiUrl}/api/v1/stats`),
          axios.get(`${apiUrl}/api/v1/vector-state`)
        ]);
        setStats(statsRes.data);
      } catch (err) {
        console.warn("Biometric API Offline - Using fallback sim");
      }
    };
    fetchData();
    const interval = setInterval(fetchData, 5000); // Live refresh
    return () => clearInterval(interval);
  }, []);

  // Periodic session verification simulation (In a real mobile app, this would be pushed by the SDK)
  useEffect(() => {
    const runVerification = async () => {
      try {
        const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8001';
        const res = await axios.post(`${apiUrl}/api/v1/verify-session`, {
          user_id: "user_premium_01",
          session_id: "demo_456",
          orientation_pitch: 0.45 + (Math.random() * 0.1 - 0.05),
          orientation_roll: 0.12,
          finger_pressure_avg: 0.6,
          swipe_velocity_avg: 1.2,
          typing_cadence_ms: [120, 115, 122]
        });
        setSimilarity(res.data.similarity_score);
        setStatus(res.data.threat_level === 'SECURE' ? 'SECURE' : 'CAUTION');
      } catch (err) {
        console.error("Session Verification Failed");
      }
    };
    const interval = setInterval(runVerification, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="biometric-dashboard">
      {/* Header Panel */}
      <header style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '3rem' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.5rem' }}>
            <Fingerprint size={36} color="#22d3ee" strokeWidth={2.5} />
            <h1 style={{ fontSize: '1.75rem', fontWeight: 800, letterSpacing: '-0.02em' }}>
              CONTINUOUS <span style={{ color: '#22d3ee' }}>BIOSCAN</span>
            </h1>
          </div>
          <p style={{ color: '#94a3b8', fontSize: '0.875rem' }}>Passive Behavioral Telemetry • Session ID: 48A-921X</p>
        </div>

        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          <div className="auth-card" style={{ padding: '0.5rem 1.25rem', borderRadius: '1rem', display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <div style={{ width: '8px', height: '8px', background: '#22c55e', borderRadius: '50%', boxShadow: '0 0 10px #22c55e' }}></div>
            <span style={{ fontSize: '0.875rem', fontWeight: 600 }}>SDK STREAM: ACTIVE</span>
          </div>
          <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} className="auth-card" style={{ padding: '0.5rem', borderRadius: '50%', cursor: 'pointer' }}>
            <RotateCcw size={20} />
          </motion.div>
        </div>
      </header>

      {/* Main Grid Layout */}
      <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 0.8fr', gap: '2rem' }}>

        {/* Left Col: Radar & Embedding visualization */}
        <section>
          <div className="auth-card" style={{ marginBottom: '2rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
              <h3>Behavioral Embedding Match</h3>
              <div className={`badge badge-${status.toLowerCase()}`}>{status === 'SECURE' ? 'Identity Verified' : status}</div>
            </div>

            <div className="radar-container">
              <ResponsiveContainer width="100%" height="100%">
                <RadarChart cx="50%" cy="50%" outerRadius="80%" data={mockProfile}>
                  <PolarGrid stroke="rgba(255,255,255,0.1)" />
                  <PolarAngleAxis dataKey="subject" tick={{ fill: '#94a3b8', fontSize: 12 }} />
                  <PolarRadiusAxis angle={30} domain={[0, 150]} tick={false} axisLine={false} />
                  <Radar
                    name="Baseline (Master)"
                    dataKey="B"
                    stroke="#8b5cf6"
                    fill="#8b5cf6"
                    fillOpacity={0.2}
                  />
                  <Radar
                    name="Live Session"
                    dataKey="A"
                    stroke="#22d3ee"
                    fill="#22d3ee"
                    fillOpacity={0.5}
                  />
                </RadarChart>
              </ResponsiveContainer>
            </div>

            <div style={{ display: 'flex', justifyContent: 'center', gap: '2rem', marginTop: '1rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <div style={{ width: '12px', height: '12px', background: '#8b5cf6', borderRadius: '3px' }}></div>
                <span style={{ fontSize: '0.75rem', color: '#94a3b8' }}>Stored Embedding</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <div style={{ width: '12px', height: '12px', background: '#22d3ee', borderRadius: '3px' }}></div>
                <span style={{ fontSize: '0.75rem', color: '#94a3b8' }}>Current Telemetry</span>
              </div>
            </div>
          </div>

          <div className="telemetry-grid">
            <Metric title="Typing Cadence" value="112ms" trend="avg" icon={<Cpu size={18} />} />
            <Metric title="Swipe Velocity" value="1.2 px/ms" trend="norm" icon={<Smartphone size={18} />} />
            <Metric title="Device Angle" value="14.2°" trend="stable" icon={<Activity size={18} />} />
          </div>
        </section>

        {/* Right Col: Similarity Gauge & Actions */}
        <section>
          <div className="auth-card" style={{ textAlign: 'center', padding: '3rem 2rem' }}>
            <h3 style={{ marginBottom: '2rem' }}>Similarity Score</h3>

            <div className="similarity-gauge">
              <span style={{ fontSize: '3rem', fontWeight: 800, color: status === 'HIJACK' ? '#ef4444' : '#fff' }}>
                {(similarity * 100).toFixed(1)}%
              </span>
              <span style={{ color: '#94a3b8', fontSize: '0.75rem', textTransform: 'uppercase' }}>Identity Confidence</span>
            </div>

            <div style={{ marginTop: '2.5rem' }}>
              <AnimatePresence mode="wait">
                {status === 'SECURE' ? (
                  <motion.div key="secure" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="badge badge-secure" style={{ padding: '1rem 2rem', fontSize: '1rem' }}>
                    <ShieldCheck size={18} style={{ marginRight: '0.5rem', marginBottom: '-3px' }} /> Frictionless Access
                  </motion.div>
                ) : (
                  <motion.div key="caution" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="badge badge-hijack" style={{ padding: '1rem 2rem', fontSize: '1rem' }}>
                    <AlertTriangle size={18} style={{ marginRight: '0.5rem', marginBottom: '-3px' }} /> Step-up Required
                  </motion.div>
                )}
              </AnimatePresence>
            </div>

            <p style={{ marginTop: '1.5rem', fontSize: '0.875rem', color: '#64748b', lineHeight: 1.5 }}>
              Continuous verification active. {status === 'SECURE' ? 'Passive signals match authorized profile.' : 'Deviation detected in typing pattern & swipe velocity.'}
            </p>
          </div>

          <div className="auth-card" style={{ marginTop: '2rem' }}>
            <h4 style={{ marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <TrendingUp size={18} color="#22d3ee" /> Probability Matrix
            </h4>
            <div style={{ height: '120px' }}>
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={[{ v: 90 }, { v: 92 }, { v: 88 }, { v: 95 }, { v: 91 }, { v: 89 }]}>
                  <Line type="monotone" dataKey="v" stroke="#22d3ee" strokeWidth={3} dot={false} />
                  <Tooltip labelStyle={{ display: 'none' }} contentStyle={{ background: '#0f172a', border: 'none', borderRadius: '4px' }} />
                </LineChart>
              </ResponsiveContainer>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '1rem', fontSize: '0.75rem', color: '#64748b' }}>
              <span>T-15min</span>
              <span>LIVE</span>
            </div>
          </div>
        </section>

      </div>

      <footer style={{ marginTop: '4rem', display: 'flex', gap: '3rem', opacity: 0.5, fontSize: '0.875rem' }}>
        <span>v2.4.0 Engine</span>
        <span>MFA-Bypass Prevention: ACTIVE</span>
        <span>Latency: 24ms</span>
      </footer>
    </div>
  );
}

function Metric({ title, value, trend, icon }: any) {
  return (
    <div className="metric-card">
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
        <div style={{ color: '#22d3ee', background: 'rgba(34, 211, 238, 0.1)', padding: '0.5rem', borderRadius: '8px' }}>
          {icon}
        </div>
        <span style={{ fontSize: '0.75rem', color: '#4ade80', fontWeight: 700 }}>{trend}</span>
      </div>
      <div style={{ fontSize: '1.25rem', fontWeight: 700 }}>{value}</div>
      <div style={{ fontSize: '0.75rem', color: '#64748b', marginTop: '0.25rem' }}>{title}</div>
    </div>
  );
}

export default App;
