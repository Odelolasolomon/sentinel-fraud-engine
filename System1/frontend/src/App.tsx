import { useState, useEffect } from 'react';
import axios from 'axios';
import {
  ShieldAlert,
  UserX,
  Activity,
  Users,
  AlertCircle,
  Lock,
  Search,
  RefreshCw
} from 'lucide-react';
import {
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  AreaChart,
  Area
} from 'recharts';
import { motion, AnimatePresence } from 'framer-motion';

// --- MOCK DATA FOR DEMO IF API NOT READY ---
const mockStats = {
  active_monitors: 1250,
  critical_threats: 14,
  synthetic_blocks: 156,
  ato_prevention_rate: "98.7%",
  daily_trends: [
    { name: 'Mon', value: 30 },
    { name: 'Tue', value: 45 },
    { name: 'Wed', value: 28 },
    { name: 'Thu', value: 55 },
    { name: 'Fri', value: 85 },
    { name: 'Sat', value: 42 },
    { name: 'Sun', value: 64 },
  ]
};

const mockThreats = [
  { id: 'TXN-904', user: 'Synthetic-ID Cluster', risk: 'CRITICAL', signal: 'IP/SSN Reuse' },
  { id: 'TXN-821', user: 'Account-421', risk: 'HIGH', signal: 'ATO - Device Deviance' },
  { id: 'TXN-763', user: 'New-User-X', risk: 'LOW', signal: 'Normal' },
];

function App() {
  const [stats, setStats] = useState<any>(mockStats);
  const [threats] = useState<any[]>(mockThreats);

  useEffect(() => {
    // Attempt real API call if backend is running (localhost:8000)
    // For this assessment demo, we use fallback mock logic if it fails or CORS issues arise
    const fetchData = async () => {
      try {
        const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
        const res = await axios.get(`${apiUrl}/api/v1/threats`);
        setStats({
          ...mockStats,
          ...res.data,
          daily_trends: res.data.daily_trends.map((v: number, i: number) => ({
            name: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][i],
            value: v
          }))
        });
      } catch (err) {
        console.warn("API Offline, using simulated data for demo visualization");
      }
    };
    fetchData();
  }, []);

  return (
    <div className="dashboard-container">
      {/* Header Support */}
      <header className="nav-header">
        <div className="logo-container">
          <ShieldAlert size={32} strokeWidth={2.5} style={{ color: '#3b82f6' }} />
          <span>CYBERGUARD <span style={{ fontWeight: 300, fontSize: '1rem', color: '#94a3b8' }}>AI ENGINE</span></span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem' }}>
          <div className="glass-card" style={{ padding: '0.5rem 1rem', display: 'flex', alignItems: 'center', gap: '0.75rem', borderRadius: '1rem' }}>
            <Search size={18} color="#94a3b8" />
            <span style={{ fontSize: '0.875rem', color: '#64748b' }}>Search Identity...</span>
          </div>
          <button className="btn-primary" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <RefreshCw size={18} /> Run Manual Scan
          </button>
        </div>
      </header>

      {/* Hero Stats */}
      <section className="stats-grid">
        <StatCard title="Active Monitors" value={stats.active_monitors.toLocaleString()} icon={<Activity color="#60a5fa" />} />
        <StatCard title="Critical Threats" value={stats.critical_threats} icon={<AlertCircle color="#ef4444" />} trend="+12% vs LW" />
        <StatCard title="Synthetic Blocks" value={stats.synthetic_blocks} icon={<UserX color="#facc15" />} />
        <StatCard title="ATO Prevention" value={stats.ato_prevention_rate} icon={<Lock color="#4ade80" />} />
      </section>

      {/* Main Grid */}
      <main className="main-content">

        {/* Synthetic Identity Analytics */}
        <div className="glass-card" style={{ gridColumn: 'span 1' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1.5rem' }}>
            <h3>Threat Vector Trends</h3>
            <span className="badge badge-low">Live Matrix</span>
          </div>
          <div style={{ height: '300px', width: '100%' }}>
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={stats.daily_trends}>
                <defs>
                  <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="name" stroke="#64748b" fontSize={12} offset={5} />
                <YAxis stroke="#64748b" fontSize={12} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '0.5rem' }}
                  itemStyle={{ color: '#fff' }}
                />
                <Area type="monotone" dataKey="value" stroke="#3b82f6" fillOpacity={1} fill="url(#colorValue)" strokeWidth={3} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
          <p style={{ marginTop: '1rem', color: '#94a3b8', fontSize: '0.875rem' }}>
            Anomaly detection models detecting "Sleeper" account activations across 5 shared IP clusters.
          </p>
        </div>

        {/* Real-time Threat Feed */}
        <div className="glass-card">
          <h3 style={{ marginBottom: '1.5rem' }}>Real-time Attack Feed</h3>
          <div className="threat-list">
            <AnimatePresence>
              {threats.map((t, i) => (
                <motion.div
                  key={t.id}
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: i * 0.1 }}
                  className="glass-card"
                  style={{
                    padding: '1rem',
                    borderRadius: '1rem',
                    background: 'rgba(51, 65, 85, 0.4)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between'
                  }}
                >
                  <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
                    <div style={{
                      width: '40px', height: '40px', borderRadius: '10px',
                      background: t.risk === 'CRITICAL' ? 'rgba(239, 68, 68, 0.2)' : 'rgba(59, 130, 246, 0.2)',
                      display: 'flex', alignItems: 'center', justifyContent: 'center'
                    }}>
                      <Users size={20} color={t.risk === 'CRITICAL' ? '#ef4444' : '#60a5fa'} />
                    </div>
                    <div>
                      <div style={{ fontWeight: 600, fontSize: '0.9rem' }}>{t.user}</div>
                      <div style={{ fontSize: '0.75rem', color: '#64748b' }}>{t.signal}</div>
                    </div>
                  </div>
                  <span className={`badge badge-${t.risk.toLowerCase()}`}>{t.risk}</span>
                </motion.div>
              ))}
            </AnimatePresence>
          </div>
          <button className="btn-primary" style={{ width: '100%', marginTop: '1.5rem', background: 'transparent', border: '1px solid rgba(255,255,255,0.1)' }}>
            View Forensic Log
          </button>
        </div>

      </main>

      {/* Tech Overview Footer-ish */}
      <footer style={{ marginTop: '3rem', borderTop: '1px solid rgba(255,255,255,0.05)', paddingTop: '2rem', display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '2rem' }}>
        <TechInfo title="Graph Theory" desc="shared IP clusters, identity reuse, device fingerprinting." />
        <TechInfo title="Behavioral Models" desc="transactional deviance scores, liveness detection." />
        <TechInfo title="Response" desc="Automated bust-out prevention & ATO friction flows." />
      </footer>
    </div>
  );
}

function StatCard({ title, value, icon, trend }: any) {
  return (
    <div className="glass-card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        {icon}
        {trend && <span style={{ color: '#4ade80', fontSize: '0.75rem', fontWeight: 600 }}>{trend}</span>}
      </div>
      <div className="stat-value">{value}</div>
      <div className="stat-label">{title}</div>
    </div>
  );
}

function TechInfo({ title, desc }: any) {
  return (
    <div>
      <h4 style={{ color: '#3b82f6', marginBottom: '0.5rem' }}>{title}</h4>
      <p style={{ color: '#64748b', fontSize: '0.875rem', lineHeight: 1.5 }}>{desc}</p>
    </div>
  );
}

export default App;
