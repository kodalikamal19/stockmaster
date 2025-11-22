import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../../services/api'
import '../Operations.css'

function Receipts() {
  const navigate = useNavigate()
  const [receipts, setReceipts] = useState([])
  const [search, setSearch] = useState('')
  const [view, setView] = useState('list')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchReceipts()
  }, [search])

  const fetchReceipts = async () => {
    try {
      const params = search ? { search } : {}
      const response = await api.get('/operations/receipts', { params })
      setReceipts(response.data)
    } catch (error) {
      console.error('Failed to fetch receipts:', error)
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
        <button className="create-button" onClick={() => navigate('/operations/receipts/new')}>
          Create Receipt
        </button>
      </div>

      {view === 'list' ? (
        <table className="operations-table">
          <thead>
            <tr>
              <th>Reference</th>
              <th>To</th>
              <th>Contact</th>
              <th>Schedule Date</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {receipts.map((receipt) => (
              <tr
                key={receipt.id}
                onClick={() => navigate(`/operations/receipts/${receipt.id}`)}
              >
                <td>
                  <a href={`/operations/receipts/${receipt.id}`}>{receipt.reference}</a>
                </td>
                <td>{receipt.to_location_name || receipt.to_warehouse}</td>
                <td>{receipt.contact || '-'}</td>
                <td>{receipt.schedule_date || '-'}</td>
                <td>
                  <span className={getStatusClass(receipt.status)}>
                    {receipt.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <div className="kanban-view">
          {receipts.map((receipt) => (
            <div
              key={receipt.id}
              className="kanban-card"
              onClick={() => navigate(`/operations/receipts/${receipt.id}`)}
            >
              <h3>{receipt.reference}</h3>
              <p><strong>To:</strong> {receipt.to_location_name || receipt.to_warehouse}</p>
              <p><strong>Contact:</strong> {receipt.contact || '-'}</p>
              <p><strong>Schedule:</strong> {receipt.schedule_date || '-'}</p>
              <p>
                <span className={getStatusClass(receipt.status)}>
                  {receipt.status}
                </span>
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default Receipts

