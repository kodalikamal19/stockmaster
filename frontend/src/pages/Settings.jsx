import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import api from '../services/api'
import { Plus, Edit, Trash2 } from 'lucide-react'

function Settings() {
  const [activeTab, setActiveTab] = useState('warehouses')

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-800 mb-6">Settings</h1>

      <div className="bg-white rounded-lg shadow-md mb-6">
        <div className="border-b border-gray-200">
          <nav className="flex -mb-px">
            <button
              onClick={() => setActiveTab('warehouses')}
              className={`px-6 py-4 text-sm font-medium border-b-2 ${
                activeTab === 'warehouses'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              Warehouses
            </button>
            <button
              onClick={() => setActiveTab('locations')}
              className={`px-6 py-4 text-sm font-medium border-b-2 ${
                activeTab === 'locations'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              Locations
            </button>
          </nav>
        </div>
      </div>

      {activeTab === 'warehouses' && <WarehousesTab />}
      {activeTab === 'locations' && <LocationsTab />}
    </div>
  )
}

function WarehousesTab() {
  const { data, isLoading } = useQuery({
    queryKey: ['warehouses'],
    queryFn: async () => {
      const response = await api.get('/settings/warehouses')
      return response.data
    },
  })

  if (isLoading) return <div>Loading...</div>

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-semibold">Warehouses</h2>
        <button className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 flex items-center space-x-2">
          <Plus className="w-4 h-4" />
          <span>Add Warehouse</span>
        </button>
      </div>

      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Short Code</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Address</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Locations</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {data?.map((warehouse) => (
              <tr key={warehouse.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap">{warehouse.name}</td>
                <td className="px-6 py-4 whitespace-nowrap font-medium">{warehouse.short_code}</td>
                <td className="px-6 py-4">{warehouse.address || '-'}</td>
                <td className="px-6 py-4 whitespace-nowrap">{warehouse.locations_count || 0}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                  <button className="text-blue-600 hover:text-blue-900">
                    <Edit className="w-4 h-4 inline" />
                  </button>
                  <button className="text-red-600 hover:text-red-900">
                    <Trash2 className="w-4 h-4 inline" />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

function LocationsTab() {
  const { data, isLoading } = useQuery({
    queryKey: ['locations'],
    queryFn: async () => {
      const response = await api.get('/settings/locations')
      return response.data
    },
  })

  if (isLoading) return <div>Loading...</div>

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-semibold">Locations</h2>
        <button className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 flex items-center space-x-2">
          <Plus className="w-4 h-4" />
          <span>Add Location</span>
        </button>
      </div>

      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Short Code</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Warehouse</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {data?.map((location) => (
              <tr key={location.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap">{location.name}</td>
                <td className="px-6 py-4 whitespace-nowrap font-medium">{location.short_code}</td>
                <td className="px-6 py-4 whitespace-nowrap">{location.warehouse_short_code || '-'}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                  <button className="text-blue-600 hover:text-blue-900">
                    <Edit className="w-4 h-4 inline" />
                  </button>
                  <button className="text-red-600 hover:text-red-900">
                    <Trash2 className="w-4 h-4 inline" />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default Settings

