import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Warehouse, LogOut, User } from 'lucide-react'

function Navbar({ user, onLogout, currentPath }) {
  const navItems = [
    { path: '/', label: 'Dashboard', icon: Warehouse },
    { path: '/operations', label: 'Operations', icon: Warehouse },
    { path: '/stock', label: 'Stock', icon: Warehouse },
    { path: '/history', label: 'Move History', icon: Warehouse },
    { path: '/settings', label: 'Settings', icon: Warehouse },
  ]

  return (
    <nav className="bg-white shadow-md">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-8">
            <Link to="/" className="flex items-center space-x-2">
              <Warehouse className="w-8 h-8 text-blue-600" />
              <span className="text-xl font-bold text-gray-800">StockMaster</span>
            </Link>
            
            <div className="flex space-x-4">
              {navItems.map((item) => {
                const Icon = item.icon
                const isActive = currentPath === item.path || 
                  (item.path !== '/' && currentPath.startsWith(item.path))
                
                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    className={`flex items-center space-x-1 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                      isActive
                        ? 'bg-blue-100 text-blue-700'
                        : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
                    }`}
                  >
                    <Icon className="w-4 h-4" />
                    <span>{item.label}</span>
                  </Link>
                )
              })}
            </div>
          </div>

          <div className="flex items-center space-x-4">
            <Link
              to="/profile"
              className="flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium text-gray-600 hover:bg-gray-100"
            >
              <User className="w-4 h-4" />
              <span>{user?.login_id || 'Profile'}</span>
            </Link>
            <button
              onClick={onLogout}
              className="flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium text-gray-600 hover:bg-gray-100"
            >
              <LogOut className="w-4 h-4" />
              <span>Logout</span>
            </button>
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navbar

