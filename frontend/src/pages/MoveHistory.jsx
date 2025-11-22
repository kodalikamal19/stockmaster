import { useState, useEffect } from 'react'
import api from '../services/api'
import './MoveHistory.css'

function MoveHistory() {
  const [history, setHistory] = useState([])
  const [warehouses, setWarehouses] = useState([])
  const [products, setProducts] = useState([])
  const [filters, setFilters] = useState({
    search: '',
    warehouse_id: '',
    product_id: '',
    date_from: '',
    date_to: '',
    operation_type: ''
  })
  const [sortBy, setSortBy] = useState('date')
  const [sortOrder, setSortOrder] = useState('desc')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchWarehouses()
    fetchProducts()
  }, [])

  useEffect(() => {
    fetchHistory()
  }, [filters, sortBy, sortOrder])

  const fetchWarehouses = async () => {
    try {
      const response = await api.get('/warehouses')
      setWarehouses(response.data)
    } catch (error) {
      console.error('Failed to fetch warehouses:', error)
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

  const fetchHistory = async () => {
    setLoading(true)
    try {
      const params = {
        sort_by: sortBy,
        sort_order: sortOrder
      }
      if (filters.search) params.search = filters.search
      if (filters.warehouse_id) params.warehouse_id = filters.warehouse_id
      if (filters.product_id) params.product_id = filters.product_id
      if (filters.date_from) params.date_from = filters.date_from
      if (filters.date_to) params.date_to = filters.date_to
      if (filters.operation_type) params.operation_type = filters.operation_type

      const response = await api.get('/move-history', { params })
      setHistory(response.data)
    } catch (error) {
      console.error('Failed to fetch history:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleFilterChange = (key, value) => {
    setFilters({ ...filters, [key]: value })
  }

  const handleSort = (column) => {
    if (sortBy === column) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')
    } else {
      setSortBy(column)
      setSortOrder('asc')
    }
  }

  const getRowClass = (entry) => {
    if (entry.operation_type === 'IN') {
      return 'inbound-row'
    } else if (entry.operation_type === 'OUT') {
      return 'outbound-row'
    }
    return ''
  }

  if (loading && history.length === 0) {
    return <div className="loading">Loading...</div>
  }

  return (
    <div className="move-history-page">
      <h1>Move History</h1>

      <div className="history-filters">
        <input
          type="text"
          placeholder="Search by reference or contact..."
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
        <select
          value={filters.operation_type}
          onChange={(e) => handleFilterChange('operation_type', e.target.value)}
          className="filter-select"
        >
          <option value="">All Types</option>
          <option value="IN">Receipt</option>
          <option value="OUT">Delivery</option>
          <option value="ADJ">Adjustment</option>
        </select>
        <input
          type="date"
          value={filters.date_from}
          onChange={(e) => handleFilterChange('date_from', e.target.value)}
          className="filter-input"
          placeholder="From Date"
        />
        <input
          type="date"
          value={filters.date_to}
          onChange={(e) => handleFilterChange('date_to', e.target.value)}
          className="filter-input"
          placeholder="To Date"
        />
      </div>

      <div className="history-table-container">
        <table className="history-table">
          <thead>
            <tr>
              <th onClick={() => handleSort('reference')}>
                Reference {sortBy === 'reference' && (sortOrder === 'asc' ? '↑' : '↓')}
              </th>
              <th onClick={() => handleSort('date')}>
                Date {sortBy === 'date' && (sortOrder === 'asc' ? '↑' : '↓')}
              </th>
              <th>Contact</th>
              <th>From</th>
              <th>To</th>
              <th>Product</th>
              <th>Quantity</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {history.map((entry) => (
              <tr key={entry.id} className={getRowClass(entry)}>
                <td>{entry.reference}</td>
                <td>{entry.date ? new Date(entry.date).toLocaleString() : '-'}</td>
                <td>{entry.contact || '-'}</td>
                <td>{entry.from_location_name || entry.from_warehouse || '-'}</td>
                <td>{entry.to_location_name || entry.to_warehouse || '-'}</td>
                <td>{entry.product_name} ({entry.product_sku})</td>
                <td>{entry.quantity}</td>
                <td>
                  <span className={`status-badge ${entry.status}`}>
                    {entry.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default MoveHistory

