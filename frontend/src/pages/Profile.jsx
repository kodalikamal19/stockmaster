import { useState, useEffect } from 'react'
import { useAuth } from '../contexts/AuthContext'
import api from '../services/api'
import './Profile.css'

function Profile() {
  const { user, logout } = useAuth()
  const [profile, setProfile] = useState(null)
  const [loading, setLoading] = useState(true)
  const [editing, setEditing] = useState(false)
  const [formData, setFormData] = useState({
    email: ''
  })

  useEffect(() => {
    fetchProfile()
  }, [])

  const fetchProfile = async () => {
    try {
      const response = await api.get('/profile')
      setProfile(response.data)
      setFormData({ email: response.data.email })
    } catch (error) {
      console.error('Failed to fetch profile:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      await api.put('/profile', formData)
      setEditing(false)
      fetchProfile()
      alert('Profile updated successfully')
    } catch (error) {
      alert(error.response?.data?.error || 'Failed to update profile')
    }
  }

  const handleLogout = () => {
    logout()
  }

  if (loading) {
    return <div className="loading">Loading...</div>
  }

  if (!profile) {
    return <div>Profile not found</div>
  }

  return (
    <div className="profile-page">
      <h1>Profile</h1>

      <div className="profile-card">
        {!editing ? (
          <>
            <div className="profile-info">
              <div className="info-item">
                <label>Login ID</label>
                <p>{profile.login_id}</p>
              </div>
              <div className="info-item">
                <label>Email</label>
                <p>{profile.email}</p>
              </div>
              <div className="info-item">
                <label>Member Since</label>
                <p>{profile.created_at ? new Date(profile.created_at).toLocaleDateString() : '-'}</p>
              </div>
            </div>
            <div className="profile-actions">
              <button onClick={() => setEditing(true)} className="edit-button">
                Edit Profile
              </button>
              <button onClick={handleLogout} className="logout-button">
                Logout
              </button>
            </div>
          </>
        ) : (
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Login ID</label>
              <input type="text" value={profile.login_id} disabled />
            </div>
            <div className="form-group">
              <label>Email</label>
              <input
                type="email"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                required
              />
            </div>
            <div className="form-actions">
              <button type="button" onClick={() => setEditing(false)} className="cancel-button">
                Cancel
              </button>
              <button type="submit" className="save-button">
                Save
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  )
}

export default Profile

