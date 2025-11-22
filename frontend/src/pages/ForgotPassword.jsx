import { useState } from 'react'
import { Link } from 'react-router-dom'
import api from '../services/api'
import './Auth.css'

function ForgotPassword() {
  const [step, setStep] = useState(1) // 1: email, 2: OTP, 3: reset
  const [formData, setFormData] = useState({
    email: '',
    otp: '',
    new_password: '',
    confirm_password: ''
  })
  const [error, setError] = useState('')
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
    setError('')
    setMessage('')
  }

  const handleSendOTP = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      await api.post('/auth/forgot-password', { email: formData.email })
      setMessage('OTP sent to your email')
      setStep(2)
    } catch (error) {
      setError(error.response?.data?.error || 'Failed to send OTP')
    } finally {
      setLoading(false)
    }
  }

  const handleVerifyOTP = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      await api.post('/auth/verify-otp', {
        email: formData.email,
        otp: formData.otp
      })
      setMessage('OTP verified')
      setStep(3)
    } catch (error) {
      setError(error.response?.data?.error || 'Invalid OTP')
    } finally {
      setLoading(false)
    }
  }

  const handleResetPassword = async (e) => {
    e.preventDefault()
    setError('')

    if (formData.new_password !== formData.confirm_password) {
      setError('Passwords do not match')
      return
    }

    setLoading(true)
    try {
      await api.post('/auth/reset-password', {
        email: formData.email,
        otp: formData.otp,
        new_password: formData.new_password
      })
      setMessage('Password reset successfully')
      setTimeout(() => {
        window.location.href = '/login'
      }, 2000)
    } catch (error) {
      setError(error.response?.data?.error || 'Failed to reset password')
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
        <h2>Reset Password</h2>

        {step === 1 && (
          <form onSubmit={handleSendOTP}>
            <div className="form-group">
              <label>Email</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
              />
            </div>

            {error && <div className="error-message">{error}</div>}
            {message && <div className="success-message">{message}</div>}

            <button type="submit" disabled={loading} className="auth-button">
              {loading ? 'Sending...' : 'Send OTP'}
            </button>

            <p className="auth-link">
              <Link to="/login">Back to Login</Link>
            </p>
          </form>
        )}

        {step === 2 && (
          <form onSubmit={handleVerifyOTP}>
            <div className="form-group">
              <label>OTP</label>
              <input
                type="text"
                name="otp"
                value={formData.otp}
                onChange={handleChange}
                maxLength="6"
                required
              />
            </div>

            {error && <div className="error-message">{error}</div>}
            {message && <div className="success-message">{message}</div>}

            <button type="submit" disabled={loading} className="auth-button">
              {loading ? 'Verifying...' : 'Verify OTP'}
            </button>
          </form>
        )}

        {step === 3 && (
          <form onSubmit={handleResetPassword}>
            <div className="form-group">
              <label>New Password</label>
              <input
                type="password"
                name="new_password"
                value={formData.new_password}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-group">
              <label>Confirm New Password</label>
              <input
                type="password"
                name="confirm_password"
                value={formData.confirm_password}
                onChange={handleChange}
                required
              />
            </div>

            {error && <div className="error-message">{error}</div>}
            {message && <div className="success-message">{message}</div>}

            <button type="submit" disabled={loading} className="auth-button">
              {loading ? 'Resetting...' : 'Reset Password'}
            </button>
          </form>
        )}
      </div>
    </div>
  )
}

export default ForgotPassword

