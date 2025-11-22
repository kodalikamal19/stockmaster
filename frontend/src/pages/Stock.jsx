import { useState, useEffect } from 'react'
import api from '../services/api'
import './Stock.css'

function Stock() {
  const [stock, setStock] = useState([])
  const [warehouses, setWarehouses] = useState([])
  const [locations, setLocations] = useState([])
  const [products, setProducts] = useState([])
  const [filters, setFilters] = useState({
    search: '',
    warehouse_id: '',
    location_id: '',
    product_id: ''
  })
  const [sortBy, setSortBy] = useState('product_name')
  const [sortOrder, setSortOrder] = useState('asc')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchWarehouses()
    fetchProducts()
  }, [])

  useEffect(() => {
    fetchStock()
  }, [filters, sortBy, sortOrder])

  useEffect(() => {
    if (filters.warehouse_id) {
      fetchLocations(filters.warehouse_id)
    } else {
      setLocations([])
    }
  }, [filters.warehouse_id])

  const fetchWarehouses = async () => {
    try {
      const response = await api.get('/warehouses')
      setWarehouses(response.data)
    } catch (error) {
      console.error('Failed to fetch warehouses:', error)
    }
  }

  const fetchLocations = async (warehouseId) => {
    try {
      const response = await api.get('/locations', { params: { warehouse_id: warehouseId } })
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

  const fetchStock = async () => {
    setLoading(true)
    try {
      const params = {
        sort_by: sortBy,
        sort_order: sortOrder
      }
      if (filters.search) params.search = filters.search
      if (filters.warehouse_id) params.warehouse_id = filters.warehouse_id
      if (filters.location_id) params.location_id = filters.location_id
      if (filters.product_id) params.product_id = filters.product_id

      const response = await api.get('/stock', { params })
      setStock(response.data)
    } catch (error) {
      console.error('Failed to fetch stock:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleFilterChange = (key, value) => {
    setFilters({ ...filters, [key]: value })
    if (key === 'warehouse_id') {
      setFilters({ ...filters, warehouse_id: value, location_id: '' })
    }
  }

  const handleSort = (column) => {
    if (sortBy === column) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')
    } else {
      setSortBy(column)
      setSortOrder('asc')
    }
  }

  if (loading && stock.length === 0) {
    return <div className="loading">Loading...</div>
  }

  return (
    <div className="stock-page">
      <h1>Stock</h1>

      <div className="stock-filters">
        <input
          type="text"
          placeholder="Search products..."
          value={filters.search}
          onChange={(e) => handleFilterChange('search', e.target.value)}
          className="filter-input"
        />
        <select
          value={filters.warehouse_id}
          onChange={(e) => handleFilterChange('warehouse_id', e.target.value)}
          className="filter-select"
        >
          <option value="">All Warehouses</option>
          {warehouses.map((wh) => (
            <option key={wh.id} value={wh.id}>
              {wh.name}
            </option>
          ))}
        </select>
        <select
          value={filters.location_id}
          onChange={(e) => handleFilterChange('location_id', e.target.value)}
          className="filter-select"
          disabled={!filters.warehouse_id}
        >
          <option value="">All Locations</option>
          {locations.map((loc) => (
            <option key={loc.id} value={loc.id}>
              {loc.name}
            </option>
          ))}
        </select>
        <select
          value={filters.product_id}
          onChange={(e) => handleFilterChange('product_id', e.target.value)}
          className="filter-select"
        >
          <option value="">All Products</option>
          {products.map((prod) => (
            <option key={prod.id} value={prod.id}>
              {prod.name}
            </option>
          ))}
        </select>
      </div>

      <div className="stock-table-container">
        <table className="stock-table">
          <thead>
            <tr>
              <th onClick={() => handleSort('product_name')}>
                Product {sortBy === 'product_name' && (sortOrder === 'asc' ? '↑' : '↓')}
              </th>
              <th onClick={() => handleSort('sku')}>
                SKU {sortBy === 'sku' && (sortOrder === 'asc' ? '↑' : '↓')}
              </th>
              <th>Unit Cost</th>
              <th onClick={() => handleSort('qty_on_hand')}>
                Qty on Hand {sortBy === 'qty_on_hand' && (sortOrder === 'asc' ? '↑' : '↓')}
              </th>
              <th>Free to Use</th>
              <th>Location</th>
              <th>Warehouse</th>
            </tr>
          </thead>
          <tbody>
            {stock.map((item) => (
              <tr key={item.id}>
                <td>{item.product_name}</td>
                <td>{item.product_sku}</td>
                <td>₹{item.unit_cost?.toFixed(2) || '0.00'}</td>
                <td>{item.qty_on_hand}</td>
                <td>{item.free_to_use}</td>
                <td>{item.location_name}</td>
                <td>{item.warehouse_short_code}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default Stock

