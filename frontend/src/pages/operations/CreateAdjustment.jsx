import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../../services/api'
import '../Operations.css'

function CreateAdjustment() {
  const navigate = useNavigate()
  const [locations, setLocations] = useState([])
  const [products, setProducts] = useState([])
  const [formData, setFormData] = useState({
    location_id: '',
    product_id: '',
    counted_quantity: '',
    contact: ''
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

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    if (!formData.location_id || !formData.product_id || !formData.counted_quantity) {
      setError('Please fill all required fields')
      setLoading(false)
      return
    }

    try {
      const payload = {
        location_id: parseInt(formData.location_id),
        product_id: parseInt(formData.product_id),
        counted_quantity: parseFloat(formData.counted_quantity),
        contact: formData.contact || 'Inventory Count'
      }

      const response = await api.post('/operations/adjustments', payload)
      navigate(`/operations/adjustments/${response.data.id}`)
    } catch (error) {
      setError(error.response?.data?.error || 'Failed to create adjustment')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="create-operation">
      <div className="operation-form-header">
        <h2>Create Adjustment</h2>
        <button onClick={() => navigate(-1)} className="back-button">
          Back
        </button>
      </div>

      <form onSubmit={handleSubmit} className="operation-form">
        <div className="form-section">
          <div className="form-group">
            <label>Location *</label>
            <select
              name="location_id"
              value={formData.location_id}
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
            <label>Product *</label>
            <select
              name="product_id"
              value={formData.product_id}
              onChange={handleChange}
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
            <label>Counted Quantity *</label>
            <input
              type="number"
              step="0.01"
              min="0"
              name="counted_quantity"
              value={formData.counted_quantity}
              onChange={handleChange}
              required
              placeholder="Enter the actual counted quantity"
            />
          </div>

          <div className="form-group">
            <label>Contact</label>
            <input
              type="text"
              name="contact"
              value={formData.contact}
              onChange={handleChange}
              placeholder="Inventory Count"
            />
          </div>
        </div>

        {error && <div className="error-message">{error}</div>}

        <div className="form-actions">
          <button type="button" onClick={() => navigate(-1)} className="cancel-button">
            Cancel
          </button>
          <button type="submit" disabled={loading} className="submit-button">
            {loading ? 'Creating...' : 'Create Adjustment'}
          </button>
        </div>
      </form>
    </div>
  )
}

export default CreateAdjustment

