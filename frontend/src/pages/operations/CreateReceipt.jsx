import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../../services/api'
import '../Operations.css'

function CreateReceipt() {
  const navigate = useNavigate()
  const [locations, setLocations] = useState([])
  const [products, setProducts] = useState([])
  const [formData, setFormData] = useState({
    to_location_id: '',
    contact: '',
    schedule_date: '',
    lines: [{ product_id: '', quantity: '', unit_cost: '' }]
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchLocations()
    fetchProducts()
  }, [])

  const fetchLocations = async () => {
    try {
      const response = await api.get('/locations')
      setLocations(response.data)
    } catch (error) {
      console.error('Failed to fetch locations:', error)
    }
  }

  const fetchProducts = async () => {
    try {
      const response = await api.get('/products')
      setProducts(response.data)
    } catch (error) {
      console.error('Failed to fetch products:', error)
    }
  }

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleLineChange = (index, field, value) => {
    const newLines = [...formData.lines]
    newLines[index][field] = value
    
    // Auto-fill unit cost when product is selected
    if (field === 'product_id') {
      const product = products.find(p => p.id === parseInt(value))
      if (product) {
        newLines[index].unit_cost = product.unit_cost
      }
    }
    
    setFormData({ ...formData, lines: newLines })
  }

  const addLine = () => {
    setFormData({
      ...formData,
      lines: [...formData.lines, { product_id: '', quantity: '', unit_cost: '' }]
    })
  }

  const removeLine = (index) => {
    const newLines = formData.lines.filter((_, i) => i !== index)
    setFormData({ ...formData, lines: newLines })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    // Validate
    if (!formData.to_location_id) {
      setError('Please select a location')
      setLoading(false)
      return
    }

    const validLines = formData.lines.filter(
      line => line.product_id && line.quantity && line.unit_cost
    )

    if (validLines.length === 0) {
      setError('Please add at least one product line')
      setLoading(false)
      return
    }

    try {
      const payload = {
        to_location_id: parseInt(formData.to_location_id),
        contact: formData.contact,
        schedule_date: formData.schedule_date || null,
        lines: validLines.map(line => ({
          product_id: parseInt(line.product_id),
          quantity: parseFloat(line.quantity),
          unit_cost: parseFloat(line.unit_cost)
        }))
      }

      const response = await api.post('/operations/receipts', payload)
      navigate(`/operations/receipts/${response.data.id}`)
    } catch (error) {
      setError(error.response?.data?.error || 'Failed to create receipt')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="create-operation">
      <div className="operation-form-header">
        <h2>Create Receipt</h2>
        <button onClick={() => navigate(-1)} className="back-button">
          Back
        </button>
      </div>

      <form onSubmit={handleSubmit} className="operation-form">
        <div className="form-section">
          <div className="form-group">
            <label>To Location *</label>
            <select
              name="to_location_id"
              value={formData.to_location_id}
              onChange={handleChange}
              required
            >
              <option value="">Select Location</option>
              {locations.map((loc) => (
                <option key={loc.id} value={loc.id}>
                  {loc.name} ({loc.warehouse_short_code})
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label>Contact</label>
            <input
              type="text"
              name="contact"
              value={formData.contact}
              onChange={handleChange}
              placeholder="Supplier/Contact name"
            />
          </div>

          <div className="form-group">
            <label>Schedule Date</label>
            <input
              type="date"
              name="schedule_date"
              value={formData.schedule_date}
              onChange={handleChange}
            />
          </div>
        </div>

        <div className="form-section">
          <div className="section-header">
            <h3>Product Lines</h3>
            <button type="button" onClick={addLine} className="add-line-button">
              Add Line
            </button>
          </div>

          {formData.lines.map((line, index) => (
            <div key={index} className="line-item">
              <div className="form-group">
                <label>Product *</label>
                <select
                  value={line.product_id}
                  onChange={(e) => handleLineChange(index, 'product_id', e.target.value)}
                  required
                >
                  <option value="">Select Product</option>
                  {products.map((prod) => (
                    <option key={prod.id} value={prod.id}>
                      {prod.name} ({prod.sku})
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label>Quantity *</label>
                <input
                  type="number"
                  step="0.01"
                  min="0"
                  value={line.quantity}
                  onChange={(e) => handleLineChange(index, 'quantity', e.target.value)}
                  required
                />
              </div>

              <div className="form-group">
                <label>Unit Cost (₹) *</label>
                <input
                  type="number"
                  step="0.01"
                  min="0"
                  value={line.unit_cost}
                  onChange={(e) => handleLineChange(index, 'unit_cost', e.target.value)}
                  required
                />
              </div>

              {formData.lines.length > 1 && (
                <button
                  type="button"
                  onClick={() => removeLine(index)}
                  className="remove-line-button"
                >
                  Remove
                </button>
              )}
            </div>
          ))}
        </div>

        {error && <div className="error-message">{error}</div>}

        <div className="form-actions">
          <button type="button" onClick={() => navigate(-1)} className="cancel-button">
            Cancel
          </button>
          <button type="submit" disabled={loading} className="submit-button">
            {loading ? 'Creating...' : 'Create Receipt'}
          </button>
        </div>
      </form>
    </div>
  )
}

export default CreateReceipt

