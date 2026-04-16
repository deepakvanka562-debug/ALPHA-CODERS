import { useState } from 'react'

export default function InputForm({ onSubmit, loading }) {
  const [formData, setFormData] = useState({
    zone_name: 'Zone A',
    load_percentage: 50,
    temperature: 25,
    weather_condition: 'Clear',
    equipment_health: 'Good',
    maintenance_delay: 'No'
  })

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    onSubmit(formData)
  }

  return (
    <form onSubmit={handleSubmit}>
      <div className="form-group">
        <label>Zone Name</label>
        <input 
          type="text" 
          name="zone_name" 
          value={formData.zone_name} 
          onChange={handleChange} 
          required 
        />
      </div>

      <div className="form-group">
        <label>Load Percentage (0-100%)</label>
        <input 
          type="number" 
          name="load_percentage" 
          min="0" max="100" 
          value={formData.load_percentage} 
          onChange={handleChange} 
          required 
        />
      </div>

      <div className="form-group">
        <label>Temperature (°C)</label>
        <input 
          type="number" 
          name="temperature" 
          value={formData.temperature} 
          onChange={handleChange} 
          required 
        />
      </div>

      <div className="form-group">
        <label>Weather Condition</label>
        <select name="weather_condition" value={formData.weather_condition} onChange={handleChange}>
          <option value="Clear">Clear</option>
          <option value="Rain">Rain</option>
          <option value="Storm">Storm</option>
        </select>
      </div>

      <div className="form-group">
        <label>Equipment Health</label>
        <select name="equipment_health" value={formData.equipment_health} onChange={handleChange}>
          <option value="Good">Good</option>
          <option value="Moderate">Moderate</option>
          <option value="Poor">Poor</option>
        </select>
      </div>

      <div className="form-group">
        <label>Maintenance Delay</label>
        <select name="maintenance_delay" value={formData.maintenance_delay} onChange={handleChange}>
          <option value="No">No</option>
          <option value="Yes">Yes</option>
        </select>
      </div>

      <button type="submit" className="btn-primary" disabled={loading}>
        {loading ? 'Analyzing...' : 'Predict Risk'}
      </button>
    </form>
  )
}
