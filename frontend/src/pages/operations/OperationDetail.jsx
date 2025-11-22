import { useState, useEffect } from 'react'
import { useParams, useNavigate, useLocation } from 'react-router-dom'
import api from '../../services/api'
import '../Operations.css'
import './OperationDetail.css'

function OperationDetail() {
  const { id } = useParams()
  const navigate = useNavigate()
  const location = useLocation()
  const [operation, setOperation] = useState(null)
  const [loading, setLoading] = useState(true)

  const operationType = location.pathname.includes('/receipts') ? 'receipts' :
                        location.pathname.includes('/deliveries') ? 'deliveries' : 'adjustments'

  useEffect(() => {
    fetchOperation()
  }, [id])

  const fetchOperation = async () => {
    try {
      const response = await api.get(`/operations/${id}`)
      setOperation(response.data)
    } catch (error) {
      console.error('Failed to fetch operation:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleValidate = async () => {
    if (!window.confirm('Are you sure you want to validate this operation?')) {
      return
    }

    try {
      await api.post(`/operations/${id}/validate`)
      fetchOperation()
      alert('Operation validated successfully')
    } catch (error) {
      alert(error.response?.data?.error || 'Failed to validate operation')
    }
  }

  const handleCancel = async () => {
    if (!window.confirm('Are you sure you want to cancel this operation?')) {
      return
    }

    try {
      await api.post(`/operations/${id}/cancel`)
      fetchOperation()
      alert('Operation cancelled successfully')
    } catch (error) {
      alert(error.response?.data?.error || 'Failed to cancel operation')
    }
  }

  const handlePrint = () => {
    window.print()
  }

  if (loading) {
    return <div className="loading">Loading...</div>
  }

  if (!operation) {
    return <div>Operation not found</div>
  }

  return (
    <div className="operation-detail">
      <div className="operation-header">
        <h2>{operation.reference}</h2>
        <div className="operation-actions">
          {operation.status === 'pending' && (
            <>
              <button onClick={handleValidate} className="action-button validate">
                Validate
              </button>
              <button onClick={handleCancel} className="action-button cancel">
                Cancel
              </button>
            </>
          )}
          <button onClick={handlePrint} className="action-button print">
            Print
          </button>
          <button onClick={() => navigate(-1)} className="action-button back">
            Back
          </button>
        </div>
      </div>

      <div className="operation-info">
        <div className="info-section">
          <h3>Details</h3>
          <p><strong>Type:</strong> {operation.operation_type_name}</p>
          <p><strong>Status:</strong> <span className={`status-badge ${operation.status}`}>{operation.status}</span></p>
          {operation.from_location_name && (
            <p><strong>From:</strong> {operation.from_location_name} ({operation.from_warehouse})</p>
          )}
          {operation.to_location_name && (
            <p><strong>To:</strong> {operation.to_location_name} ({operation.to_warehouse})</p>
          )}
          <p><strong>Contact:</strong> {operation.contact || '-'}</p>
          <p><strong>Schedule Date:</strong> {operation.schedule_date || '-'}</p>
          <p><strong>Created:</strong> {operation.created_at ? new Date(operation.created_at).toLocaleString() : '-'}</p>
          {operation.validated_at && (
            <p><strong>Validated:</strong> {new Date(operation.validated_at).toLocaleString()}</p>
          )}
        </div>

        <div className="info-section">
          <h3>Lines</h3>
          <table className="operations-table">
            <thead>
              <tr>
                <th>Product</th>
                <th>SKU</th>
                <th>Quantity</th>
                <th>Unit Cost</th>
                <th>Total</th>
              </tr>
            </thead>
            <tbody>
              {operation.lines?.map((line) => (
                <tr key={line.id}>
                  <td>{line.product_name}</td>
                  <td>{line.product_sku}</td>
                  <td>{line.quantity}</td>
                  <td>₹{line.unit_cost}</td>
                  <td>₹{(line.quantity * line.unit_cost).toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

export default OperationDetail

