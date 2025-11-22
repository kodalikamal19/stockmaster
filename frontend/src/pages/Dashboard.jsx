import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'
import './Dashboard.css'

function Dashboard() {
  const navigate = useNavigate()
  const [stats, setStats] = useState({
    receipts: { pending: 0, scheduled: 0, late: 0, waiting_for_stock: 0 },
    deliveries: { pending: 0, scheduled: 0, late: 0, waiting_for_stock: 0 }
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    try {
      const response = await api.get('/dashboard/stats')
      setStats(response.data)
    } catch (error) {
      console.error('Failed to fetch stats:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="loading">Loading...</div>
  }

  return (
    <div className="dashboard">
      <h1>Dashboard</h1>
      <div className="dashboard-grid">
        <div className="dashboard-card receipts-card" onClick={() => navigate('/operations/receipts')}>
          <h2>Receipts</h2>
          <div className="stats-grid">
            <div className="stat-item">
              <span className="stat-label">Pending</span>
              <span className="stat-value">{stats.receipts.pending}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Scheduled</span>
              <span className="stat-value">{stats.receipts.scheduled}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Late</span>
              <span className="stat-value">{stats.receipts.late}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Waiting for Stock</span>
              <span className="stat-value">{stats.receipts.waiting_for_stock}</span>
            </div>
          </div>
        </div>

        <div className="dashboard-card deliveries-card" onClick={() => navigate('/operations/deliveries')}>
          <h2>Deliveries</h2>
          <div className="stats-grid">
            <div className="stat-item">
              <span className="stat-label">Pending</span>
              <span className="stat-value">{stats.deliveries.pending}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Scheduled</span>
              <span className="stat-value">{stats.deliveries.scheduled}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Late</span>
              <span className="stat-value">{stats.deliveries.late}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Waiting for Stock</span>
              <span className="stat-value">{stats.deliveries.waiting_for_stock}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard

