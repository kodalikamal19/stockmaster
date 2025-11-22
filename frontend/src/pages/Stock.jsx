import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import api from '../services/api'
import { Search, Filter } from 'lucide-react'

function Stock() {
  const [search, setSearch] = useState('')
  const [sortBy, setSortBy] = useState('product.name')
  const [sortOrder, setSortOrder] = useState('asc')
  const [lowStockFilter, setLowStockFilter] = useState(false)

  const { data, isLoading } = useQuery({
    queryKey: ['stock', search, sortBy, sortOrder, lowStockFilter],
    queryFn: async () => {
      const params = new URLSearchParams()
      if (search) params.append('search', search)
      params.append('sort_by', sortBy)
      params.append('sort_order', sortOrder)
      if (lowStockFilter) params.append('low_stock', 'true')
      const response = await api.get(`/stock?${params}`)
      return response.data
    },
  })

  if (isLoading) return <div>Loading...</div>

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-3xl font-bold text-gray-800">Stock</h1>
      </div>

      <div className="bg-white rounded-lg shadow-md p-4 mb-6">
        <div className="flex items-center space-x-4">
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Search products..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="pl-10 pr-4 py-2 border border-gray-300 rounded-md w-full focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
          >
            <option value="product.name">Product Name</option>
            <option value="sku">SKU</option>
            <option value="quantity_on_hand">Quantity</option>
            <option value="unit_cost">Unit Cost</option>
          </select>
          <select
            value={sortOrder}
            onChange={(e) => setSortOrder(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
          >
            <option value="asc">Ascending</option>
            <option value="desc">Descending</option>
          </select>
          <label className="flex items-center space-x-2">
            <input
              type="checkbox"
              checked={lowStockFilter}
              onChange={(e) => setLowStockFilter(e.target.checked)}
              className="rounded"
            />
            <span>Low Stock Only</span>
          </label>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Product</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">SKU</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Location</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Unit Cost</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Qty On Hand</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Qty Free</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {data?.items?.map((item) => (
              <tr key={item.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap">{item.product?.name || '-'}</td>
                <td className="px-6 py-4 whitespace-nowrap">{item.product?.sku || '-'}</td>
                <td className="px-6 py-4 whitespace-nowrap">{item.location?.name || '-'}</td>
                <td className="px-6 py-4 whitespace-nowrap">${item.unit_cost?.toFixed(2) || '0.00'}</td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={item.quantity_on_hand < 10 ? 'text-red-600 font-semibold' : ''}>
                    {item.quantity_on_hand}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">{item.quantity_free_to_use}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                  <button className="text-blue-600 hover:text-blue-900">Transfer</button>
                  <button className="text-purple-600 hover:text-purple-900">Adjust</button>
                  <button className="text-green-600 hover:text-green-900">Ledger</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default Stock

