import React, { useEffect, useState, useCallback } from 'react'
import './index.css'

const API_BASE = 'http://127.0.0.1:8000'

// ─── Particle Background ────────────────────────────────────────────────────
function Particles() {
  return (
    <div className="particles">
      {Array.from({ length: 20 }).map((_, i) => (
        <span key={i} className="particle" style={{
          left: `${Math.random() * 100}%`,
          animationDelay: `${Math.random() * 8}s`,
          animationDuration: `${6 + Math.random() * 6}s`,
          width: `${4 + Math.random() * 6}px`,
          height: `${4 + Math.random() * 6}px`,
        }} />
      ))}
    </div>
  )
}

// ─── Toast Notification ─────────────────────────────────────────────────────
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

// ─── Auth Forms ─────────────────────────────────────────────────────────────
function AuthPanel({ onToken }) {
  const [mode, setMode] = useState('login')
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function submit(e) {
    e.preventDefault()
    setError(null)
    setLoading(true)
    const endpoint = mode === 'login' ? '/auth/login' : '/auth/signup'
    try {
      const res = await fetch(`${API_BASE}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.detail || 'Authentication failed')
      onToken(data.access_token, username)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-panel glass">
      <div className="auth-logo">🎮</div>
      <h2 className="auth-title">PLAYFORM</h2>
      <p className="auth-subtitle">Your Gaming Universe</p>

      <div className="tab-switcher">
        <button
          className={`tab-btn ${mode === 'login' ? 'active' : ''}`}
          onClick={() => { setMode('login'); setError(null) }}
        >登入</button>
        <button
          className={`tab-btn ${mode === 'signup' ? 'active' : ''}`}
          onClick={() => { setMode('signup'); setError(null) }}
        >註冊</button>
      </div>

      <form onSubmit={submit} className="auth-form">
        {error && <div className="error-msg">⚠️ {error}</div>}
        <div className="input-group">
          <span className="input-icon">👤</span>
          <input
            className="auth-input"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
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
            onChange={(e) => setPassword(e.target.value)}
            placeholder="密碼"
            required
          />
        </div>
        <button className="btn-primary" type="submit" disabled={loading}>
          {loading ? <span className="spinner" /> : (mode === 'login' ? '🚀 登入' : '✨ 建立帳號')}
        </button>
      </form>
    </div>
  )
}

// ─── Game Card ───────────────────────────────────────────────────────────────
const GAME_EMOJIS = ['🎯', '🏆', '⚔️', '🎲', '🕹️', '🎪', '🌟', '🔥', '💎', '🚀']

function GameCard({ game, index, onDelete, isAdmin }) {
  const emoji = GAME_EMOJIS[index % GAME_EMOJIS.length]
  const [deleting, setDeleting] = useState(false)

  async function handleDelete() {
    if (!window.confirm(`確定要刪除「${game.name}」嗎？`)) return
    setDeleting(true)
    await onDelete(game.id)
    setDeleting(false)
  }

  return (
    <div className="game-card glass" style={{ animationDelay: `${index * 0.05}s` }}>
      <div className="game-emoji">{emoji}</div>
      <div className="game-info">
        <h3 className="game-name">{game.name}</h3>
        <span className="game-id">ID: #{game.id}</span>
      </div>
      {isAdmin && (
        <button
          className="btn-delete"
          onClick={handleDelete}
          disabled={deleting}
          title="刪除遊戲"
        >
          {deleting ? '⏳' : '🗑️'}
        </button>
      )}
    </div>
  )
}

// ─── Dashboard Stats ─────────────────────────────────────────────────────────
function StatCard({ emoji, label, value }) {
  return (
    <div className="stat-card glass">
      <div className="stat-emoji">{emoji}</div>
      <div className="stat-value">{value}</div>
      <div className="stat-label">{label}</div>
    </div>
  )
}

// ─── Main App ─────────────────────────────────────────────────────────────────
export default function App() {
  const [token, setToken] = useState(localStorage.getItem('pf_token') || null)
  const [currentUser, setCurrentUser] = useState(localStorage.getItem('pf_user') || null)
  const [games, setGames] = useState([])
  const [loading, setLoading] = useState(false)
  const [dashData, setDashData] = useState(null)
  const [newGameName, setNewGameName] = useState('')
  const [creating, setCreating] = useState(false)
  const [toast, setToast] = useState(null)
  const [view, setView] = useState('games') // 'games' | 'dashboard'

  const showToast = (message, type = 'success') => {
    setToast({ message, type })
  }

  const fetchGames = useCallback(async () => {
    setLoading(true)
    try {
      const res = await fetch(`${API_BASE}/api/games`)
      if (!res.ok) throw new Error('Failed to load games')
      const data = await res.json()
      setGames(data)
    } catch (e) {
      showToast(e.message, 'error')
    } finally {
      setLoading(false)
    }
  }, [])

  const fetchDashboard = useCallback(async () => {
    if (!token) return
    try {
      const res = await fetch(`${API_BASE}/api/dashboard`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      if (!res.ok) throw new Error('Failed to load dashboard')
      const data = await res.json()
      setDashData(data)
    } catch (e) {
      showToast(e.message, 'error')
    }
  }, [token])

  useEffect(() => { fetchGames() }, [fetchGames])
  useEffect(() => { if (token) fetchDashboard() }, [token, fetchDashboard])

  function handleToken(t, username) {
    localStorage.setItem('pf_token', t)
    localStorage.setItem('pf_user', username)
    setToken(t)
    setCurrentUser(username)
    showToast(`歡迎回來，${username}！`)
  }

  function logout() {
    localStorage.removeItem('pf_token')
    localStorage.removeItem('pf_user')
    setToken(null)
    setCurrentUser(null)
    setDashData(null)
    showToast('已登出')
  }

  async function createGame(e) {
    e.preventDefault()
    if (!newGameName.trim()) return
    setCreating(true)
    try {
      const headers = { 'Content-Type': 'application/json' }
      if (token) headers.Authorization = `Bearer ${token}`
      const res = await fetch(`${API_BASE}/api/games`, {
        method: 'POST',
        headers,
        body: JSON.stringify({ name: newGameName.trim() }),
      })
      if (!res.ok) {
        const err = await res.json()
        throw new Error(err.detail || 'Create failed')
      }
      setNewGameName('')
      await fetchGames()
      if (token) await fetchDashboard()
      showToast('遊戲已新增！')
    } catch (e) {
      showToast(e.message, 'error')
    } finally {
      setCreating(false)
    }
  }

  async function deleteGame(id) {
    try {
      const res = await fetch(`${API_BASE}/api/games/${id}`, {
        method: 'DELETE',
      })
      if (!res.ok) throw new Error('Delete failed')
      await fetchGames()
      if (token) await fetchDashboard()
      showToast('遊戲已刪除')
    } catch (e) {
      showToast(e.message, 'error')
    }
  }

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

      {/* Header */}
      <header className="app-header glass">
        <div className="header-brand">
          <span className="brand-logo">🎮</span>
          <span className="brand-name">PLAYFORM</span>
        </div>
        <nav className="header-nav">
          <button
            className={`nav-btn ${view === 'games' ? 'active' : ''}`}
            onClick={() => setView('games')}
          >🕹️ 遊戲</button>
          <button
            className={`nav-btn ${view === 'dashboard' ? 'active' : ''}`}
            onClick={() => setView('dashboard')}
          >📊 儀表板</button>
        </nav>
        <div className="header-user">
          <span className="user-badge">👤 {currentUser}</span>
          <button className="btn-logout" onClick={logout}>登出</button>
        </div>
      </header>

      <main className="app-main">
        {view === 'games' && (
          <>
            {/* Add Game */}
            <section className="add-game-section">
              <div className="section-header">
                <h2 className="section-title">✨ 新增遊戲</h2>
              </div>
              <form onSubmit={createGame} className="add-game-form glass">
                <input
                  className="game-input"
                  value={newGameName}
                  onChange={(e) => setNewGameName(e.target.value)}
                  placeholder="輸入遊戲名稱..."
                  maxLength={50}
                />
                <button className="btn-primary btn-add" type="submit" disabled={creating}>
                  {creating ? <span className="spinner" /> : '+ 新增'}
                </button>
              </form>
            </section>

            {/* Games Grid */}
            <section className="games-section">
              <div className="section-header">
                <h2 className="section-title">🎯 所有遊戲</h2>
                <span className="badge">{games.length} 個</span>
              </div>
              {loading ? (
                <div className="loading-grid">
                  {[1, 2, 3].map(i => <div key={i} className="skeleton-card" />)}
                </div>
              ) : games.length === 0 ? (
                <div className="empty-state glass">
                  <div style={{ fontSize: 64 }}>🎲</div>
                  <p>目前沒有遊戲，快來新增第一個！</p>
                </div>
              ) : (
                <div className="games-grid">
                  {games.map((g, i) => (
                    <GameCard
                      key={g.id}
                      game={g}
                      index={i}
                      onDelete={deleteGame}
                      isAdmin={!!token}
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
              <h2 className="section-title">📊 儀表板</h2>
            </div>
            {dashData ? (
              <>
                <div className="stats-grid">
                  <StatCard emoji="🎮" label="遊戲總數" value={dashData.total_games} />
                  <StatCard emoji="👤" label="目前用戶" value={dashData.user} />
                  <StatCard emoji="⭐" label="活躍度" value="HIGH" />
                </div>
                <div className="dashboard-games glass">
                  <h3 style={{ marginBottom: 16, color: 'var(--text-secondary)' }}>遊戲清單</h3>
                  {dashData.games.length === 0 ? (
                    <p style={{ color: 'var(--text-muted)' }}>尚無遊戲資料</p>
                  ) : (
                    <table className="data-table">
                      <thead>
                        <tr>
                          <th>ID</th>
                          <th>名稱</th>
                          <th>操作</th>
                        </tr>
                      </thead>
                      <tbody>
                        {dashData.games.map((g) => (
                          <tr key={g.id}>
                            <td>#{g.id}</td>
                            <td>{g.name}</td>
                            <td>
                              <button
                                className="btn-delete-sm"
                                onClick={() => deleteGame(g.id)}
                              >刪除</button>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  )}
                </div>
              </>
            ) : (
              <div className="loading-grid">
                {[1, 2, 3].map(i => <div key={i} className="skeleton-card" />)}
              </div>
            )}
          </section>
        )}
      </main>

      {toast && <Toast {...toast} onClose={() => setToast(null)} />}
    </div>
  )
}
