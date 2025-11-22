import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import './Navbar.css'

function Navbar() {
  const location = useLocation()
  const navigate = useNavigate()
  const { logout } = useAuth()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const navItems = [
    { path: '/', label: 'Dashboard' },
    { path: '/operations', label: 'Operations' },
    { path: '/stock', label: 'Stock' },
    { path: '/move-history', label: 'Move History' },
    { path: '/settings', label: 'Settings' },
    { path: '/profile', label: 'Profile' }
  ]

  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <h2>StockMaster</h2>
      </div>
      <div className="navbar-links">
        {navItems.map(item => (
          <Link
            key={item.path}
            to={item.path}
            className={location.pathname === item.path ? 'active' : ''}
          >
            {item.label}
          </Link>
        ))}
        <button onClick={handleLogout} className="logout-btn">
          Logout
        </button>
      </div>
    </nav>
  )
}

export default Navbar

