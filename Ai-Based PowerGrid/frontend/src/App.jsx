import { useState } from 'react'
import axios from 'axios'
import InputForm from './components/InputForm'
import Dashboard from './components/Dashboard'

function App() {
  const [prediction, setPrediction] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handlePredict = async (formData) => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await axios.post('http://127.0.0.1:5000/predict', formData)
      setPrediction(response.data)
    } catch (err) {
      console.error(err)
      setError("Prediction failed. Please ensure the backend is running.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-container">
      <header>
        <h1>AI Power Grid Agent</h1>
        <p className="subtitle">Real-time Failure & Delay Prediction System</p>
      </header>

      <main className="dashboard-layout">
        <div className="glass-card">
          <h2 className="card-title">Grid Parameters</h2>
          <InputForm onSubmit={handlePredict} loading={loading} />
          {error && <p style={{color: 'var(--accent-red)', marginTop: '1rem'}}>{error}</p>}
        </div>

        <div className="glass-card">
          <h2 className="card-title">Analysis & Insights</h2>
          <Dashboard data={prediction} loading={loading} />
        </div>
      </main>
    </div>
  )
}

export default App
