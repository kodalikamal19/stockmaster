import { useState } from 'react'
import { Routes, Route, Link, useLocation } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import api from '../services/api'
import Receipts from '../components/operations/Receipts'
import Deliveries from '../components/operations/Deliveries'
import Adjustments from '../components/operations/Adjustments'

function Operations() {
  const location = useLocation()
  const tabs = [
    { path: '/operations/receipts', label: 'Receipts' },
    { path: '/operations/deliveries', label: 'Deliveries' },
    { path: '/operations/adjustments', label: 'Adjustments' },
  ]

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-3xl font-bold text-gray-800">Operations</h1>
      </div>

      <div className="bg-white rounded-lg shadow-md mb-6">
        <div className="border-b border-gray-200">
          <nav className="flex -mb-px">
            {tabs.map((tab) => {
              const isActive = location.pathname === tab.path
              return (
                <Link
                  key={tab.path}
                  to={tab.path}
                  className={`px-6 py-4 text-sm font-medium border-b-2 ${
                    isActive
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  {tab.label}
                </Link>
              )
            })}
          </nav>
        </div>
      </div>

      <Routes>
        <Route path="receipts" element={<Receipts />} />
        <Route path="deliveries" element={<Deliveries />} />
        <Route path="adjustments" element={<Adjustments />} />
        <Route path="" element={<Receipts />} />
      </Routes>
    </div>
  )
}

export default Operations

