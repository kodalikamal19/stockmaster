import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import api from '../services/api'
import './Auth.css'

function Signup() {
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    login_id: '',
    email: '',
    password: '',
    confirm_password: ''
  })
  const [errors, setErrors] = useState({})
  const [loading, setLoading] = useState(false)

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
    setErrors({ ...errors, [e.target.name]: '' })
  }

  const validate = () => {
    const newErrors = {}

    if (formData.login_id.length < 6 || formData.login_id.length > 12) {
      newErrors.login_id = 'Login ID must be between 6 and 12 characters'
    }

    if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email is invalid'
    }

    if (formData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters'
    } else {
      if (!/[A-Z]/.test(formData.password)) {
        newErrors.password = 'Password must contain an uppercase letter'
      } else if (!/[a-z]/.test(formData.password)) {
        newErrors.password = 'Password must contain a lowercase letter'
      } else if (!/\d/.test(formData.password)) {
        newErrors.password = 'Password must contain a digit'
      } else if (!/[!@#$%^&*(),.?":{}|<>]/.test(formData.password)) {
        newErrors.password = 'Password must contain a special character'
      }
    }

    if (formData.password !== formData.confirm_password) {
      newErrors.confirm_password = 'Passwords do not match'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!validate()) {
      return
    }

    setLoading(true)
    try {
      await api.post('/auth/signup', formData)
      navigate('/login')
    } catch (error) {
      setErrors({ submit: error.response?.data?.error || 'Signup failed' })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-logo">
          <h1>StockMaster</h1>
        </div>
        <h2>Sign Up</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Login ID</label>
            <input
              type="text"
              name="login_id"
              value={formData.login_id}
              onChange={handleChange}
              required
            />
            {errors.login_id && <span className="error">{errors.login_id}</span>}
          </div>

          <div className="form-group">
            <label>Email</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
            />
            {errors.email && <span className="error">{errors.email}</span>}
          </div>

          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
            />
            {errors.password && <span className="error">{errors.password}</span>}
          </div>

          <div className="form-group">
            <label>Confirm Password</label>
            <input
              type="password"
              name="confirm_password"
              value={formData.confirm_password}
              onChange={handleChange}
              required
            />
            {errors.confirm_password && <span className="error">{errors.confirm_password}</span>}
          </div>

          {errors.submit && <div className="error-message">{errors.submit}</div>}

          <button type="submit" disabled={loading} className="auth-button">
            {loading ? 'Signing up...' : 'Sign Up'}
          </button>

          <p className="auth-link">
            Already have an account? <Link to="/login">Login</Link>
          </p>
        </form>
      </div>
    </div>
  )
}

export default Signup

