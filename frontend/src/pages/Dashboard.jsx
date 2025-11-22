import { useQuery } from '@tanstack/react-query'
import api from '../services/api'
import { motion } from 'framer-motion'
import { Package, Truck, Boxes, AlertTriangle, Activity } from 'lucide-react'

function KPICard({ title, value, icon: Icon, color, onClick }) {
  return (
    <motion.div
      whileHover={{ scale: 1.05 }}
      onClick={onClick}
      className={`bg-white rounded-lg shadow-md p-6 cursor-pointer border-l-4 ${color}`}
    >
      <div className="flex items-center justify-between">
        <div>
          <p className="text-gray-600 text-sm font-medium">{title}</p>
          <p className="text-3xl font-bold text-gray-800 mt-2">{value}</p>
        </div>
        <Icon className="w-12 h-12 text-gray-400" />
      </div>
    </motion.div>
  )
}

function Dashboard() {
  const { data: stats, isLoading } = useQuery({
    queryKey: ['dashboard-stats'],
    queryFn: async () => {
      const response = await api.get('/operations/dashboard/stats')
      return response.data
    },
  })

  if (isLoading) {
    return <div className="text-center py-12">Loading...</div>
  }

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-800 mb-8">Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-6 mb-8">
        <KPICard
          title="Receipts Pending"
          value={stats?.receipts?.pending || 0}
          icon={Package}
          color="border-blue-500"
        />
        <KPICard
          title="Receipts Scheduled"
          value={stats?.receipts?.scheduled || 0}
          icon={Package}
          color="border-green-500"
        />
        <KPICard
          title="Receipts Late"
          value={stats?.receipts?.late || 0}
          icon={Package}
          color="border-red-500"
        />
        <KPICard
          title="Deliveries Pending"
          value={stats?.deliveries?.pending || 0}
          icon={Truck}
          color="border-blue-500"
        />
        <KPICard
          title="Deliveries Scheduled"
          value={stats?.deliveries?.scheduled || 0}
          icon={Truck}
          color="border-green-500"
        />
        <KPICard
          title="Deliveries Late"
          value={stats?.deliveries?.late || 0}
          icon={Truck}
          color="border-red-500"
        />
        <KPICard
          title="Waiting for Stock"
          value={stats?.receipts?.waiting_for_stock || 0}
          icon={Boxes}
          color="border-yellow-500"
        />
        <KPICard
          title="Total Stock Items"
          value={stats?.total_stock_items || 0}
          icon={Boxes}
          color="border-indigo-500"
        />
        <KPICard
          title="Low Stock"
          value={stats?.low_stock || 0}
          icon={AlertTriangle}
          color="border-red-500"
        />
        <KPICard
          title="Operations Left"
          value={stats?.operations_left || 0}
          icon={Activity}
          color="border-purple-500"
        />
      </div>

      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold text-gray-800 mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <button className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">
            Create Receipt
          </button>
          <button className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700">
            Create Delivery
          </button>
          <button className="px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700">
            Stock Adjustment
          </button>
        </div>
      </div>
    </div>
  )
}

export default Dashboard

