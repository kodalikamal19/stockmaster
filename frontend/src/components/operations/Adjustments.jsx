import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import api from '../../services/api'
import { Plus } from 'lucide-react'

function Adjustments() {
  const { data, isLoading } = useQuery({
    queryKey: ['adjustments'],
    queryFn: async () => {
      const response = await api.get('/operations/adjustments')
      return response.data
    },
  })

  if (isLoading) return <div>Loading...</div>

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-semibold">Stock Adjustments</h2>
        <button className="px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700 flex items-center space-x-2">
          <Plus className="w-4 h-4" />
          <span>New Adjustment</span>
        </button>
      </div>

      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Reference</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Location</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Product</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Quantity</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {data?.items?.map((adjustment) => (
              <tr key={adjustment.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap font-medium">{adjustment.reference}</td>
                <td className="px-6 py-4 whitespace-nowrap">{adjustment.to_location?.name || '-'}</td>
                <td className="px-6 py-4 whitespace-nowrap">
                  {adjustment.lines?.[0]?.product?.name || '-'}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  {adjustment.lines?.[0]?.quantity || 0}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">{adjustment.created_at?.split('T')[0] || '-'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default Adjustments

