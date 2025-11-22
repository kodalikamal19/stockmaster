import { useState, useEffect } from 'react'
import api from '../services/api'
import './Settings.css'

function Settings() {
  const [activeTab, setActiveTab] = useState('warehouses')
  const [warehouses, setWarehouses] = useState([])
  const [locations, setLocations] = useState([])
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const [editingItem, setEditingItem] = useState(null)
  const [formData, setFormData] = useState({
    name: '',
    short_code: '',
    address: '',
    warehouse_id: ''
  })

  useEffect(() => {
    fetchData()
  }, [activeTab])

  const fetchData = async () => {
    setLoading(true)
    try {
      if (activeTab === 'warehouses') {
        const response = await api.get('/settings/warehouses')
        setWarehouses(response.data)
      } else {
        const response = await api.get('/settings/locations')
        setLocations(response.data)
        const whResponse = await api.get('/settings/warehouses')
        setWarehouses(whResponse.data)
      }
    } catch (error) {
      console.error('Failed to fetch data:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleOpenModal = (item = null) => {
    setEditingItem(item)
    if (item) {
      if (activeTab === 'warehouses') {
        setFormData({
          name: item.name,
          short_code: item.short_code,
          address: item.address || ''
        })
      } else {
        setFormData({
          name: item.name,
          short_code: item.short_code,
          warehouse_id: item.warehouse_id.toString()
        })
      }
    } else {
      setFormData({
        name: '',
        short_code: '',
        address: '',
        warehouse_id: ''
      })
    }
    setShowModal(true)
  }

  const handleCloseModal = () => {
    setShowModal(false)
    setEditingItem(null)
    setFormData({ name: '', short_code: '', address: '', warehouse_id: '' })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      if (activeTab === 'warehouses') {
        if (editingItem) {
          await api.put(`/settings/warehouses/${editingItem.id}`, formData)
        } else {
          await api.post('/settings/warehouses', formData)
        }
      } else {
        if (editingItem) {
          await api.put(`/settings/locations/${editingItem.id}`, formData)
        } else {
          await api.post('/settings/locations', formData)
        }
      }
      handleCloseModal()
      fetchData()
    } catch (error) {
      alert(error.response?.data?.error || 'Operation failed')
    }
  }

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this item?')) {
      return
    }

    try {
      if (activeTab === 'warehouses') {
        await api.delete(`/settings/warehouses/${id}`)
      } else {
        await api.delete(`/settings/locations/${id}`)
      }
      fetchData()
    } catch (error) {
      alert(error.response?.data?.error || 'Delete failed')
    }
  }

  if (loading) {
    return <div className="loading">Loading...</div>
  }

  return (
    <div className="settings-page">
      <h1>Settings</h1>

      <div className="settings-tabs">
        <button
          className={activeTab === 'warehouses' ? 'active' : ''}
          onClick={() => setActiveTab('warehouses')}
        >
          Warehouses
        </button>
        <button
          className={activeTab === 'locations' ? 'active' : ''}
          onClick={() => setActiveTab('locations')}
        >
          Locations
        </button>
      </div>

      <div className="settings-content">
        <div className="settings-header">
          <h2>{activeTab === 'warehouses' ? 'Warehouses' : 'Locations'}</h2>
          <button className="create-button" onClick={() => handleOpenModal()}>
            Create {activeTab === 'warehouses' ? 'Warehouse' : 'Location'}
          </button>
        </div>

        {activeTab === 'warehouses' ? (
          <table className="settings-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Short Code</th>
                <th>Address</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {warehouses.map((wh) => (
                <tr key={wh.id}>
                  <td>{wh.name}</td>
                  <td>{wh.short_code}</td>
                  <td>{wh.address || '-'}</td>
                  <td>
                    <button onClick={() => handleOpenModal(wh)} className="edit-btn">
                      Edit
                    </button>
                    <button onClick={() => handleDelete(wh.id)} className="delete-btn">
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <table className="settings-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Short Code</th>
                <th>Warehouse</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {locations.map((loc) => (
                <tr key={loc.id}>
                  <td>{loc.name}</td>
                  <td>{loc.short_code}</td>
                  <td>{loc.warehouse_short_code}</td>
                  <td>
                    <button onClick={() => handleOpenModal(loc)} className="edit-btn">
                      Edit
                    </button>
                    <button onClick={() => handleDelete(loc.id)} className="delete-btn">
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {showModal && (
        <div className="modal-overlay" onClick={handleCloseModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h3>
              {editingItem ? 'Edit' : 'Create'}{' '}
              {activeTab === 'warehouses' ? 'Warehouse' : 'Location'}
            </h3>
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label>Name</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  required
                />
              </div>
              <div className="form-group">
                <label>Short Code</label>
                <input
                  type="text"
                  value={formData.short_code}
                  onChange={(e) => setFormData({ ...formData, short_code: e.target.value.toUpperCase() })}
                  required
                />
              </div>
              {activeTab === 'warehouses' ? (
                <div className="form-group">
                  <label>Address</label>
                  <textarea
                    value={formData.address}
                    onChange={(e) => setFormData({ ...formData, address: e.target.value })}
                  />
                </div>
              ) : (
                <div className="form-group">
                  <label>Warehouse</label>
                  <select
                    value={formData.warehouse_id}
                    onChange={(e) => setFormData({ ...formData, warehouse_id: e.target.value })}
                    required
                  >
                    <option value="">Select Warehouse</option>
                    {warehouses.map((wh) => (
                      <option key={wh.id} value={wh.id}>
                        {wh.name}
                      </option>
                    ))}
                  </select>
                </div>
              )}
              <div className="modal-actions">
                <button type="button" onClick={handleCloseModal} className="cancel-btn">
                  Cancel
                </button>
                <button type="submit" className="submit-btn">
                  {editingItem ? 'Update' : 'Create'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}

export default Settings

