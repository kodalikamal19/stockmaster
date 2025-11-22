import { Outlet, useNavigate, useLocation } from 'react-router-dom'
import Navbar from './Navbar'
import { useAuth } from '../contexts/AuthContext'

function Layout() {
  const navigate = useNavigate()
  const location = useLocation()
  const { user, logout } = useAuth()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar user={user} onLogout={handleLogout} currentPath={location.pathname} />
      <main className="container mx-auto px-4 py-8">
        <Outlet />
      </main>
    </div>
  )
}

export default Layout

