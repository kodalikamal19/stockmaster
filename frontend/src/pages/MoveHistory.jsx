import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import api from '../services/api'
import { Search, Calendar } from 'lucide-react'

function MoveHistory() {
  const [search, setSearch] = useState('')
  const [startDate, setStartDate] = useState('')
  const [endDate, setEndDate] = useState('')
  const [ledgerType, setLedgerType] = useState('')

  const { data, isLoading } = useQuery({
    queryKey: ['history', search, startDate, endDate, ledgerType],
    queryFn: async () => {
      const params = new URLSearchParams()
      if (search) params.append('search', search)
      if (startDate) params.append('start_date', startDate)
      if (endDate) params.append('end_date', endDate)
      if (ledgerType) params.append('ledger_type', ledgerType)
      const response = await api.get(`/history?${params}`)
      return response.data
    },
  })

  const getTypeColor = (type) => {
    if (type === 'inbound') return 'text-green-600'
    if (type === 'outbound') return 'text-red-600'
    return 'text-gray-600'
  }

  if (isLoading) return <div>Loading...</div>

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-3xl font-bold text-gray-800">Move History</h1>
      </div>

      <div className="bg-white rounded-lg shadow-md p-4 mb-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Search..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="pl-10 pr-4 py-2 border border-gray-300 rounded-md w-full focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
            placeholder="Start Date"
          />
          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
            placeholder="End Date"
          />
          <select
            value={ledgerType}
            onChange={(e) => setLedgerType(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All Types</option>
            <option value="inbound">Inbound</option>
            <option value="outbound">Outbound</option>
            <option value="adjustment">Adjustment</option>
            <option value="transfer">Transfer</option>
          </select>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Reference</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Type</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Product</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Location</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Quantity</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Contact</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {data?.items?.map((entry) => (
              <tr key={entry.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap font-medium">{entry.reference}</td>
                <td className="px-6 py-4 whitespace-nowrap">{entry.created_at?.split('T')[0] || '-'}</td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`font-medium ${getTypeColor(entry.ledger_type)}`}>
                    {entry.ledger_type}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">{entry.product?.name || '-'}</td>
                <td className="px-6 py-4 whitespace-nowrap">{entry.location?.name || '-'}</td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={entry.quantity > 0 ? 'text-green-600' : 'text-red-600'}>
                    {entry.quantity > 0 ? '+' : ''}{entry.quantity}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">{entry.contact_name || '-'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default MoveHistory

