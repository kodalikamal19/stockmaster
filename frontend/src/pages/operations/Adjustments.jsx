import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../../services/api'
import '../Operations.css'

function Adjustments() {
  const navigate = useNavigate()
  const [adjustments, setAdjustments] = useState([])
  const [search, setSearch] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchAdjustments()
  }, [search])

  const fetchAdjustments = async () => {
    try {
      const params = search ? { search } : {}
      const response = await api.get('/operations/adjustments', { params })
      setAdjustments(response.data)
    } catch (error) {
      console.error('Failed to fetch adjustments:', error)
    } finally {
      setLoading(false)
    }
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
        <button className="create-button" onClick={() => navigate('/operations/adjustments/new')}>
          Create Adjustment
        </button>
      </div>

      <table className="operations-table">
        <thead>
          <tr>
            <th>Reference</th>
            <th>Location</th>
            <th>Contact</th>
            <th>Status</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          {adjustments.map((adjustment) => (
            <tr
              key={adjustment.id}
              onClick={() => navigate(`/operations/adjustments/${adjustment.id}`)}
            >
              <td>
                <a href={`/operations/adjustments/${adjustment.id}`}>{adjustment.reference}</a>
              </td>
              <td>{adjustment.to_location_name || adjustment.to_warehouse}</td>
              <td>{adjustment.contact || '-'}</td>
              <td>
                <span className={`status-badge ${adjustment.status}`}>
                  {adjustment.status}
                </span>
              </td>
              <td>{adjustment.created_at ? new Date(adjustment.created_at).toLocaleDateString() : '-'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default Adjustments

