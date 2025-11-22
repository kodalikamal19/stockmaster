import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import api from '../../services/api'
import { Search, Plus, Eye, Check, X } from 'lucide-react'

function Receipts() {
  const [search, setSearch] = useState('')
  const [statusFilter, setStatusFilter] = useState('')
  const [viewMode, setViewMode] = useState('table') // 'table' or 'kanban'

  const { data, isLoading } = useQuery({
    queryKey: ['receipts', search, statusFilter],
    queryFn: async () => {
      const params = new URLSearchParams()
      if (search) params.append('search', search)
      if (statusFilter) params.append('status', statusFilter)
      const response = await api.get(`/operations/receipts?${params}`)
      return response.data
    },
  })

  const queryClient = useQueryClient()

  const validateMutation = useMutation({
    mutationFn: async (id) => {
      const response = await api.post(`/operations/${id}/validate`)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['receipts'])
    },
  })

  const cancelMutation = useMutation({
    mutationFn: async (id) => {
      const response = await api.post(`/operations/${id}/cancel`)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['receipts'])
    },
  })

  const getStatusColor = (status) => {
    const colors = {
      pending: 'bg-yellow-100 text-yellow-800',
      scheduled: 'bg-blue-100 text-blue-800',
      validated: 'bg-green-100 text-green-800',
      cancelled: 'bg-red-100 text-red-800',
      late: 'bg-red-100 text-red-800',
      waiting_for_stock: 'bg-orange-100 text-orange-800',
    }
    return colors[status] || 'bg-gray-100 text-gray-800'
  }

  if (isLoading) return <div>Loading...</div>

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-4 flex-1">
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Search by reference or contact..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="pl-10 pr-4 py-2 border border-gray-300 rounded-md w-full focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All Status</option>
            <option value="pending">Pending</option>
            <option value="scheduled">Scheduled</option>
            <option value="validated">Validated</option>
            <option value="cancelled">Cancelled</option>
            <option value="late">Late</option>
          </select>
          <button
            onClick={() => setViewMode(viewMode === 'table' ? 'kanban' : 'table')}
            className="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300"
          >
            {viewMode === 'table' ? 'Kanban View' : 'Table View'}
          </button>
        </div>
        <button className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 flex items-center space-x-2">
          <Plus className="w-4 h-4" />
          <span>New Receipt</span>
        </button>
      </div>

      {viewMode === 'table' ? (
        <div className="bg-white rounded-lg shadow-md overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Reference</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">To</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Contact</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Schedule Date</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {data?.items?.map((receipt) => (
                <tr key={receipt.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap font-medium">{receipt.reference}</td>
                  <td className="px-6 py-4 whitespace-nowrap">{receipt.to_location?.name || '-'}</td>
                  <td className="px-6 py-4 whitespace-nowrap">{receipt.contact_name || '-'}</td>
                  <td className="px-6 py-4 whitespace-nowrap">{receipt.schedule_date || '-'}</td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(receipt.status)}`}>
                      {receipt.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                    <button className="text-blue-600 hover:text-blue-900">
                      <Eye className="w-4 h-4 inline" />
                    </button>
                    {receipt.status !== 'validated' && receipt.status !== 'cancelled' && (
                      <>
                        <button
                          onClick={() => validateMutation.mutate(receipt.id)}
                          className="text-green-600 hover:text-green-900"
                        >
                          <Check className="w-4 h-4 inline" />
                        </button>
                        <button
                          onClick={() => cancelMutation.mutate(receipt.id)}
                          className="text-red-600 hover:text-red-900"
                        >
                          <X className="w-4 h-4 inline" />
                        </button>
                      </>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {['pending', 'scheduled', 'validated', 'cancelled'].map((status) => {
            const items = data?.items?.filter((r) => r.status === status) || []
            return (
              <div key={status} className="bg-gray-100 rounded-lg p-4">
                <h3 className="font-semibold mb-4 capitalize">{status}</h3>
                <div className="space-y-2">
                  {items.map((receipt) => (
                    <div key={receipt.id} className="bg-white p-3 rounded shadow">
                      <p className="font-medium text-sm">{receipt.reference}</p>
                      <p className="text-xs text-gray-600">{receipt.contact_name || 'No contact'}</p>
                    </div>
                  ))}
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}

export default Receipts

