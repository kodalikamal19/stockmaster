import { Routes, Route, Link, useLocation, useNavigate } from 'react-router-dom'
import Receipts from './operations/Receipts'
import Deliveries from './operations/Deliveries'
import Adjustments from './operations/Adjustments'
import OperationDetail from './operations/OperationDetail'
import CreateReceipt from './operations/CreateReceipt'
import CreateDelivery from './operations/CreateDelivery'
import CreateAdjustment from './operations/CreateAdjustment'
import './Operations.css'

function Operations() {
  const location = useLocation()
  const navigate = useNavigate()

  return (
    <div className="operations">
      <div className="operations-header">
        <h1>Operations</h1>
        <div className="operations-tabs">
          <Link
            to="/operations/receipts"
            className={location.pathname.includes('/receipts') ? 'active' : ''}
          >
            Receipts
          </Link>
          <Link
            to="/operations/deliveries"
            className={location.pathname.includes('/deliveries') ? 'active' : ''}
          >
            Deliveries
          </Link>
          <Link
            to="/operations/adjustments"
            className={location.pathname.includes('/adjustments') ? 'active' : ''}
          >
            Adjustments
          </Link>
        </div>
      </div>

      <Routes>
        <Route path="receipts" element={<Receipts />} />
        <Route path="receipts/new" element={<CreateReceipt />} />
        <Route path="receipts/:id" element={<OperationDetail />} />
        <Route path="deliveries" element={<Deliveries />} />
        <Route path="deliveries/new" element={<CreateDelivery />} />
        <Route path="deliveries/:id" element={<OperationDetail />} />
        <Route path="adjustments" element={<Adjustments />} />
        <Route path="adjustments/new" element={<CreateAdjustment />} />
        <Route path="adjustments/:id" element={<OperationDetail />} />
      </Routes>
    </div>
  )
}

export default Operations

