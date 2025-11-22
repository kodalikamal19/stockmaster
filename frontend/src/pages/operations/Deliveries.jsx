import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../../services/api'
import '../Operations.css'

function Deliveries() {
  const navigate = useNavigate()
  const [deliveries, setDeliveries] = useState([])
  const [search, setSearch] = useState('')
  const [view, setView] = useState('list')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDeliveries()
  }, [search])

  const fetchDeliveries = async () => {
    try {
      const params = search ? { search } : {}
      const response = await api.get('/operations/deliveries', { params })
      setDeliveries(response.data)
    } catch (error) {
      console.error('Failed to fetch deliveries:', error)
    } finally {
      setLoading(false)
    }
  }

  const getStatusClass = (status) => {
    return `status-badge ${status}`
  }

  if (loading) {
    return <div className="loading">Loading...</div>
  }

  return (
    <div className="operations-list">
      <div className="operations-controls">
        <input
          type="text"
          placeholder="Search by reference or contact..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="search-input"
        />
        <div className="view-toggle">
          <button
            className={view === 'list' ? 'active' : ''}
            onClick={() => setView('list')}
          >
            List
          </button>
          <button
            className={view === 'kanban' ? 'active' : ''}
            onClick={() => setView('kanban')}
          >
            Kanban
          </button>
        </div>
        <button className="create-button" onClick={() => navigate('/operations/deliveries/new')}>
          Create Delivery
        </button>
      </div>

      {view === 'list' ? (
        <table className="operations-table">
          <thead>
            <tr>
              <th>Reference</th>
              <th>From</th>
              <th>Contact</th>
              <th>Schedule Date</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {deliveries.map((delivery) => (
              <tr
                key={delivery.id}
                onClick={() => navigate(`/operations/deliveries/${delivery.id}`)}
              >
                <td>
                  <a href={`/operations/deliveries/${delivery.id}`}>{delivery.reference}</a>
                </td>
                <td>{delivery.from_location_name || delivery.from_warehouse}</td>
                <td>{delivery.contact || '-'}</td>
                <td>{delivery.schedule_date || '-'}</td>
                <td>
                  <span className={getStatusClass(delivery.status)}>
                    {delivery.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <div className="kanban-view">
          {deliveries.map((delivery) => (
            <div
              key={delivery.id}
              className="kanban-card"
              onClick={() => navigate(`/operations/deliveries/${delivery.id}`)}
            >
              <h3>{delivery.reference}</h3>
              <p><strong>From:</strong> {delivery.from_location_name || delivery.from_warehouse}</p>
              <p><strong>Contact:</strong> {delivery.contact || '-'}</p>
              <p><strong>Schedule:</strong> {delivery.schedule_date || '-'}</p>
              <p>
                <span className={getStatusClass(delivery.status)}>
                  {delivery.status}
                </span>
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default Deliveries

