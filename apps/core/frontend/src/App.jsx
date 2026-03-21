import React, { useCallback, useEffect, useState } from 'react'
import './index.css'

const API_BASE = 'http://127.0.0.1:8000'
const EMPTY_PROFILE = { name: '', age: '', bio: '' }

function Particles() {
  return (
    <div className="particles">
      {Array.from({ length: 20 }).map((_, index) => (
        <span
          key={index}
          className="particle"
          style={{
            left: `${Math.random() * 100}%`,
            animationDelay: `${Math.random() * 8}s`,
            animationDuration: `${6 + Math.random() * 6}s`,
            width: `${4 + Math.random() * 6}px`,
            height: `${4 + Math.random() * 6}px`,
          }}
        />
      ))}
    </div>
  )
}

function Toast({ message, type, onClose }) {
  useEffect(() => {
    const timer = setTimeout(onClose, 3000)
    return () => clearTimeout(timer)
  }, [onClose])

  return (
    <div className={`toast toast-${type}`}>
      <span>{type === 'success' ? '✅' : '❌'}</span>
      <span>{message}</span>
    </div>
  )
}

function AuthPanel({ onToken }) {
  const [mode, setMode] = useState('login')
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function submit(event) {
    event.preventDefault()
    setError(null)
    setLoading(true)

    const endpoint = mode === 'login' ? '/auth/login' : '/auth/signup'

    try {
      const response = await fetch(`${API_BASE}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      })
      const data = await response.json()
      if (!response.ok) {
        throw new Error(data.detail || 'Authentication failed')
      }
      onToken(data.access_token, username)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-panel glass">
      <div className="auth-logo">💘</div>
      <h2 className="auth-title">SEOULMATE</h2>
      <p className="auth-subtitle">首爾感配對資料庫</p>

      <div className="tab-switcher">
        <button
          className={`tab-btn ${mode === 'login' ? 'active' : ''}`}
          onClick={() => { setMode('login'); setError(null) }}
          type="button"
        >
          登入
        </button>
        <button
          className={`tab-btn ${mode === 'signup' ? 'active' : ''}`}
          onClick={() => { setMode('signup'); setError(null) }}
          type="button"
        >
          註冊
        </button>
      </div>

      <form onSubmit={submit} className="auth-form">
        {error && <div className="error-msg">⚠️ {error}</div>}
        <div className="input-group">
          <span className="input-icon">👤</span>
          <input
            className="auth-input"
            value={username}
            onChange={(event) => setUsername(event.target.value)}
            placeholder="使用者名稱"
            required
          />
        </div>
        <div className="input-group">
          <span className="input-icon">🔒</span>
          <input
            className="auth-input"
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            placeholder="密碼"
            required
          />
        </div>
        <button className="btn-primary" type="submit" disabled={loading}>
          {loading ? <span className="spinner" /> : (mode === 'login' ? '進入後台' : '建立帳號')}
        </button>
      </form>
    </div>
  )
}

const PROFILE_EMOJIS = ['💘', '🌆', '☕', '🎧', '🍷', '📚', '✨', '🌙', '🎬', '🫶']

function ProfileCard({ profile, index, onDelete, canDelete }) {
  const emoji = PROFILE_EMOJIS[index % PROFILE_EMOJIS.length]
  const [deleting, setDeleting] = useState(false)

  async function handleDelete() {
    if (!window.confirm(`確定要刪除「${profile.name}」的檔案嗎？`)) {
      return
    }

    setDeleting(true)
    await onDelete(profile.id)
    setDeleting(false)
  }

  return (
    <div className="game-card glass" style={{ animationDelay: `${index * 0.05}s` }}>
      <div className="game-emoji">{emoji}</div>
      <div className="game-info">
        <h3 className="game-name">{profile.name}</h3>
        <div className="profile-meta">
          <span>#{profile.id}</span>
          <span>{profile.age} 歲</span>
          <span>{profile.matches_count || 0} 次配對</span>
        </div>
        <p className="profile-bio">{profile.bio}</p>
      </div>
      {canDelete && (
        <button
          className="btn-delete"
          onClick={handleDelete}
          disabled={deleting}
          title="刪除檔案"
          type="button"
        >
          {deleting ? '⏳' : '🗑️'}
        </button>
      )}
    </div>
  )
}

function StatCard({ emoji, label, value }) {
  return (
    <div className="stat-card glass">
      <div className="stat-emoji">{emoji}</div>
      <div className="stat-value">{value}</div>
      <div className="stat-label">{label}</div>
    </div>
  )
}

export default function App() {
  const [token, setToken] = useState(localStorage.getItem('pf_token') || null)
  const [currentUser, setCurrentUser] = useState(localStorage.getItem('pf_user') || null)
  const [profiles, setProfiles] = useState([])
  const [loading, setLoading] = useState(false)
  const [dashData, setDashData] = useState(null)
  const [profileForm, setProfileForm] = useState(EMPTY_PROFILE)
  const [creating, setCreating] = useState(false)
  const [toast, setToast] = useState(null)
  const [view, setView] = useState('profiles')

  const showToast = useCallback((message, type = 'success') => {
    setToast({ message, type })
  }, [])

  const fetchProfiles = useCallback(async () => {
    setLoading(true)
    try {
      const response = await fetch(`${API_BASE}/api/profiles`)
      if (!response.ok) {
        throw new Error('載入檔案失敗')
      }
      const data = await response.json()
      setProfiles(data)
    } catch (err) {
      showToast(err.message, 'error')
    } finally {
      setLoading(false)
    }
  }, [showToast])

  const fetchDashboard = useCallback(async () => {
    if (!token) {
      return
    }

    try {
      const response = await fetch(`${API_BASE}/api/dashboard`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      if (!response.ok) {
        throw new Error('載入儀表板失敗')
      }
      const data = await response.json()
      setDashData(data)
    } catch (err) {
      showToast(err.message, 'error')
    }
  }, [showToast, token])

  useEffect(() => {
    fetchProfiles()
  }, [fetchProfiles])

  useEffect(() => {
    if (token) {
      fetchDashboard()
    }
  }, [fetchDashboard, token])

  function handleToken(nextToken, username) {
    localStorage.setItem('pf_token', nextToken)
    localStorage.setItem('pf_user', username)
    setToken(nextToken)
    setCurrentUser(username)
    showToast(`歡迎回來，${username}。`)
  }

  function logout() {
    localStorage.removeItem('pf_token')
    localStorage.removeItem('pf_user')
    setToken(null)
    setCurrentUser(null)
    setDashData(null)
    showToast('已登出')
  }

  function updateProfileForm(field) {
    return (event) => {
      setProfileForm((current) => ({ ...current, [field]: event.target.value }))
    }
  }

  async function createProfile(event) {
    event.preventDefault()
    if (!profileForm.name.trim() || !profileForm.bio.trim() || !profileForm.age) {
      return
    }

    setCreating(true)
    try {
      const headers = { 'Content-Type': 'application/json' }
      if (token) {
        headers.Authorization = `Bearer ${token}`
      }

      const response = await fetch(`${API_BASE}/api/profiles`, {
        method: 'POST',
        headers,
        body: JSON.stringify({
          name: profileForm.name.trim(),
          age: Number(profileForm.age),
          bio: profileForm.bio.trim(),
        }),
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || '建立檔案失敗')
      }

      setProfileForm(EMPTY_PROFILE)
      await fetchProfiles()
      if (token) {
        await fetchDashboard()
      }
      showToast('配對檔案已建立')
    } catch (err) {
      showToast(err.message, 'error')
    } finally {
      setCreating(false)
    }
  }

  async function deleteProfile(id) {
    try {
      const response = await fetch(`${API_BASE}/api/profiles/${id}`, {
        method: 'DELETE',
      })
      if (!response.ok) {
        throw new Error('刪除檔案失敗')
      }
      await fetchProfiles()
      if (token) {
        await fetchDashboard()
      }
      showToast('檔案已刪除')
    } catch (err) {
      showToast(err.message, 'error')
    }
  }

  const dashboardProfiles = dashData?.profiles || []
  const totalMatches = dashboardProfiles.reduce(
    (sum, profile) => sum + (profile.matches_count || 0),
    0,
  )

  if (!token) {
    return (
      <div className="app-bg">
        <Particles />
        <div className="center-screen">
          <AuthPanel onToken={handleToken} />
        </div>
        {toast && <Toast {...toast} onClose={() => setToast(null)} />}
      </div>
    )
  }

  return (
    <div className="app-bg">
      <Particles />

      <header className="app-header glass">
        <div className="header-brand">
          <span className="brand-logo">💘</span>
          <span className="brand-name">SEOULMATE</span>
        </div>
        <nav className="header-nav">
          <button
            className={`nav-btn ${view === 'profiles' ? 'active' : ''}`}
            onClick={() => setView('profiles')}
            type="button"
          >
            配對檔案
          </button>
          <button
            className={`nav-btn ${view === 'dashboard' ? 'active' : ''}`}
            onClick={() => setView('dashboard')}
            type="button"
          >
            儀表板
          </button>
        </nav>
        <div className="header-user">
          <span className="user-badge">👤 {currentUser}</span>
          <button className="btn-logout" onClick={logout} type="button">
            登出
          </button>
        </div>
      </header>

      <main className="app-main">
        {view === 'profiles' && (
          <>
            <section className="add-game-section">
              <div className="section-header">
                <h2 className="section-title">建立新的配對檔案</h2>
              </div>
              <form onSubmit={createProfile} className="add-game-form glass">
                <div className="form-grid">
                  <input
                    className="game-input"
                    value={profileForm.name}
                    onChange={updateProfileForm('name')}
                    placeholder="暱稱或姓名"
                    maxLength={30}
                    required
                  />
                  <input
                    className="game-input"
                    value={profileForm.age}
                    onChange={updateProfileForm('age')}
                    type="number"
                    min="18"
                    max="50"
                    placeholder="年齡"
                    required
                  />
                  <textarea
                    className="game-input bio-input"
                    value={profileForm.bio}
                    onChange={updateProfileForm('bio')}
                    placeholder="自我介紹、興趣或想認識的對象"
                    maxLength={160}
                    required
                  />
                </div>
                <button className="btn-primary btn-add" type="submit" disabled={creating}>
                  {creating ? <span className="spinner" /> : '建立檔案'}
                </button>
              </form>
            </section>

            <section className="games-section">
              <div className="section-header">
                <h2 className="section-title">公開配對檔案</h2>
                <span className="badge">{profiles.length} 份</span>
              </div>
              {loading ? (
                <div className="loading-grid">
                  {[1, 2, 3].map((item) => <div key={item} className="skeleton-card" />)}
                </div>
              ) : profiles.length === 0 ? (
                <div className="empty-state glass">
                  <div style={{ fontSize: 64 }}>💌</div>
                  <p>目前還沒有檔案，先建立第一份吧。</p>
                </div>
              ) : (
                <div className="games-grid">
                  {profiles.map((profile, index) => (
                    <ProfileCard
                      key={profile.id}
                      profile={profile}
                      index={index}
                      onDelete={deleteProfile}
                      canDelete={Boolean(token)}
                    />
                  ))}
                </div>
              )}
            </section>
          </>
        )}

        {view === 'dashboard' && (
          <section className="dashboard-section">
            <div className="section-header">
              <h2 className="section-title">會員儀表板</h2>
            </div>
            {dashData ? (
              <>
                <div className="stats-grid">
                  <StatCard emoji="💘" label="檔案總數" value={dashData.total_profiles} />
                  <StatCard emoji="👤" label="目前登入" value={dashData.user} />
                  <StatCard emoji="✨" label="累積配對次數" value={totalMatches} />
                </div>
                <div className="dashboard-games glass">
                  <h3 style={{ marginBottom: 16, color: 'var(--text-secondary)' }}>最近檔案</h3>
                  {dashboardProfiles.length === 0 ? (
                    <p style={{ color: 'var(--text-muted)' }}>尚無檔案資料</p>
                  ) : (
                    <table className="data-table">
                      <thead>
                        <tr>
                          <th>ID</th>
                          <th>名稱</th>
                          <th>年齡</th>
                          <th>簡介</th>
                          <th>配對</th>
                        </tr>
                      </thead>
                      <tbody>
                        {dashboardProfiles.map((profile) => (
                          <tr key={profile.id}>
                            <td>#{profile.id}</td>
                            <td>{profile.name}</td>
                            <td>{profile.age}</td>
                            <td>{profile.bio}</td>
                            <td>{profile.matches_count || 0}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  )}
                </div>
              </>
            ) : (
              <div className="loading-grid">
                {[1, 2, 3].map((item) => <div key={item} className="skeleton-card" />)}
              </div>
            )}
          </section>
        )}
      </main>

      {toast && <Toast {...toast} onClose={() => setToast(null)} />}
    </div>
  )
}
