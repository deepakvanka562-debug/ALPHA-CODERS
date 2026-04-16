import { CircularProgressbar, buildStyles } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';

export default function Dashboard({ data, loading }) {
  if (loading) {
    return (
      <div className="empty-state">
        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
        <h3>AI Engine Processing...</h3>
        <p>Analyzing historical data and running simulations.</p>
      </div>
    )
  }

  if (!data) {
    return (
      <div className="empty-state">
        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>
        <h3>Waiting for Input</h3>
        <p>Enter parameters on the left to predict grid risk.</p>
      </div>
    )
  }

  // Determine colors based on risk
  let riskColor = '#10b981' // Green
  let riskGlow = 'rgba(16, 185, 129, 0.4)'
  if (data.risk_level === 'MEDIUM') {
    riskColor = '#f59e0b' // Yellow
    riskGlow = 'rgba(245, 158, 11, 0.4)'
  } else if (data.risk_level === 'HIGH') {
    riskColor = '#ef4444' // Red
    riskGlow = 'rgba(239, 68, 68, 0.4)'
  }

  return (
    <div className="dashboard-content animate-in">
      
      <div className="results-grid">
        <div className="metric-card" style={{ boxShadow: `0 0 20px ${riskGlow}` }}>
          <div className="metric-label">Failure Probability</div>
          <div style={{ width: '120px', margin: '1rem auto' }}>
            <CircularProgressbar 
              value={data.failure_probability} 
              text={`${data.failure_probability}%`}
              styles={buildStyles({
                pathColor: riskColor,
                textColor: '#fff',
                trailColor: 'rgba(255,255,255,0.1)'
              })}
            />
          </div>
          <h3 className={`risk-${data.risk_level}`}>{data.risk_level} RISK</h3>
        </div>

        <div className="metric-card">
          <div className="metric-label">Est. Restoration Delay</div>
          <div className="metric-value">
            {data.expected_delay_hours} <span style={{fontSize: '1rem', color: 'var(--text-muted)'}}>hrs</span>
          </div>
          <div style={{ marginTop: '2rem' }}>
            <div className="metric-label">Zone</div>
            <h3 style={{marginTop: '0.5rem'}}>{data.zone_name}</h3>
          </div>
        </div>
      </div>

      <div className="recommendations-box">
        <h3 style={{marginBottom: '1rem'}}>AI Recommendations</h3>
        <ul className="recommendations-list">
          {data.recommendations && data.recommendations.map((rec, idx) => (
            <li key={idx}>{rec}</li>
          ))}
        </ul>
      </div>

    </div>
  )
}
