import { useCallback, useEffect, useState } from 'react'
import { fetchDashboard, fetchPublicProfiles, fetchUsers, login } from './lib/api'

const EMPTY_CREDENTIALS = { username: '', password: '' }

export default function App() {
  const [token, setToken] = useState(localStorage.getItem('sm_admin_token') || '')
  const [currentUser, setCurrentUser] = useState(localStorage.getItem('sm_admin_user') || '')
  const [credentials, setCredentials] = useState(EMPTY_CREDENTIALS)
  const [profiles, setProfiles] = useState([])
  const [dashboard, setDashboard] = useState(null)
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(false)
  const [loginLoading, setLoginLoading] = useState(false)
  const [publicError, setPublicError] = useState('')
  const [loginError, setLoginError] = useState('')
  const [protectedStatus, setProtectedStatus] = useState('登入後可查看會員清單與私人儀表板。')

  const loadPublicData = useCallback(async () => {
    try {
      const data = await fetchPublicProfiles()
      setProfiles(data)
      setPublicError('')
    } catch (error) {
      setProfiles([])
      setPublicError(error.message)
    }
  }, [])

  const loadProtectedData = useCallback(async (activeToken) => {
    if (!activeToken) {
      setDashboard(null)
      setUsers([])
      setProtectedStatus('目前顯示公開資料；登入後可查看會員清單與私人儀表板。')
      return
    }

    const [dashboardResult, usersResult] = await Promise.allSettled([
      fetchDashboard(activeToken),
      fetchUsers(activeToken),
    ])

    if (dashboardResult.status === 'fulfilled') {
      setDashboard(dashboardResult.value)
    } else {
      setDashboard(null)
    }

    if (usersResult.status === 'fulfilled') {
      setUsers(usersResult.value)
    } else {
      setUsers([])
    }

    if (dashboardResult.status === 'rejected' && usersResult.status === 'rejected') {
      localStorage.removeItem('sm_admin_token')
      localStorage.removeItem('sm_admin_user')
      setToken('')
      setCurrentUser('')
      setProtectedStatus('登入已失效，請重新登入。')
      return
    }

    if (dashboardResult.status === 'fulfilled' && usersResult.status === 'fulfilled') {
      setProtectedStatus('管理員資料同步正常。')
      return
    }

    if (dashboardResult.status === 'fulfilled') {
      setProtectedStatus('已登入，但目前帳號沒有管理員權限，會員清單不可用。')
      return
    }

    setProtectedStatus('目前僅取得部分受保護資料。')
  }, [])

  const refreshAll = useCallback(async () => {
    setLoading(true)
    await loadPublicData()
    await loadProtectedData(token)
    setLoading(false)
  }, [loadProtectedData, loadPublicData, token])

  useEffect(() => {
    refreshAll()
  }, [refreshAll])

  function updateCredential(field) {
    return (event) => {
      setCredentials((current) => ({ ...current, [field]: event.target.value }))
    }
  }

  async function handleLogin(event) {
    event.preventDefault()
    setLoginError('')
    setLoginLoading(true)

    try {
      const response = await login(credentials)
      localStorage.setItem('sm_admin_token', response.access_token)
      localStorage.setItem('sm_admin_user', credentials.username)
      setToken(response.access_token)
      setCurrentUser(credentials.username)
      setCredentials(EMPTY_CREDENTIALS)
      await loadProtectedData(response.access_token)
    } catch (error) {
      setLoginError(error.message)
    } finally {
      setLoginLoading(false)
    }
  }

  function handleLogout() {
    localStorage.removeItem('sm_admin_token')
    localStorage.removeItem('sm_admin_user')
    setToken('')
    setCurrentUser('')
    setDashboard(null)
    setUsers([])
    setProtectedStatus('已登出，僅顯示公開資料。')
  }

  const totalMatches = profiles.reduce((sum, profile) => sum + (profile.matches_count || 0), 0)
  const averageAge = profiles.length
    ? Math.round(profiles.reduce((sum, profile) => sum + Number(profile.age || 0), 0) / profiles.length)
    : 0

  return (
    <div className="admin-layout">
      <aside className="sidebar">
        <h2 className="sidebar-title">SEOULMATE</h2>
        <nav className="sidebar-nav">
          <div className="sidebar-link active">內容總覽</div>
          <div className="sidebar-link">公開檔案</div>
          <div className="sidebar-link">會員資料</div>
          <div className="sidebar-link">API 狀態</div>
        </nav>

        <div className="sidebar-panel">
          <div className="sidebar-label">同步狀態</div>
          <div className={`status-pill ${publicError ? 'error' : 'ok'}`}>
            {publicError ? 'API 異常' : 'API 正常'}
          </div>
          <p className="sidebar-text">
            {publicError || '公開 profiles API 已連線，可直接查看即時內容。'}
          </p>
        </div>
      </aside>

      <main className="main-content">
        <header className="header">
          <div>
            <h1 className="page-title">內容管理後台</h1>
            <p className="page-subtitle">同步公開檔案、會員資料與配對統計，不再顯示假資料。</p>
          </div>
          <button className="refresh-btn" onClick={refreshAll} type="button" disabled={loading}>
            {loading ? '更新中...' : '重新整理'}
          </button>
        </header>

        <section className="login-panel">
          {token ? (
            <div className="login-state">
              <div>
                <div className="panel-title">已登入帳號</div>
                <div className="panel-user">{currentUser}</div>
              </div>
              <button className="ghost-btn" onClick={handleLogout} type="button">
                登出
              </button>
            </div>
          ) : (
            <form className="inline-form" onSubmit={handleLogin}>
              <input
                className="field-input"
                value={credentials.username}
                onChange={updateCredential('username')}
                placeholder="管理員帳號"
                required
              />
              <input
                className="field-input"
                value={credentials.password}
                onChange={updateCredential('password')}
                placeholder="密碼"
                type="password"
                required
              />
              <button className="primary-btn" type="submit" disabled={loginLoading}>
                {loginLoading ? '登入中...' : '登入'}
              </button>
            </form>
          )}
          <p className="panel-note">{loginError || protectedStatus}</p>
        </section>

        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-label">公開檔案數</div>
            <div className="stat-value">{profiles.length}</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">累積配對次數</div>
            <div className="stat-value">{totalMatches}</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">平均年齡</div>
            <div className="stat-value">{averageAge || '--'}</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">會員數</div>
            <div className="stat-value">{users.length || (dashboard ? 1 : '--')}</div>
          </div>
        </div>

        <div className="split-grid">
          <section className="table-card">
            <div className="table-header">
              <h3 style={{ margin: 0 }}>最新公開檔案</h3>
              <span className="table-badge">{profiles.length} 份</span>
            </div>
            <table>
              <thead>
                <tr>
                  <th>名稱</th>
                  <th>年齡</th>
                  <th>自介</th>
                  <th>配對</th>
                </tr>
              </thead>
              <tbody>
                {profiles.length === 0 ? (
                  <tr>
                    <td colSpan="4" className="table-empty">目前沒有可顯示的公開檔案。</td>
                  </tr>
                ) : (
                  profiles.map((profile) => (
                    <tr key={profile.id}>
                      <td>{profile.name}</td>
                      <td>{profile.age}</td>
                      <td>{profile.bio}</td>
                      <td><span className="badge-active">{profile.matches_count || 0} 次</span></td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </section>

          <section className="table-card">
            <div className="table-header">
              <h3 style={{ margin: 0 }}>會員與私人儀表板</h3>
            </div>
            {dashboard ? (
              <div className="panel-stack">
                <div className="mini-card">
                  <div className="mini-label">目前登入</div>
                  <div className="mini-value">{dashboard.user}</div>
                </div>
                <div className="mini-card">
                  <div className="mini-label">儀表板檔案數</div>
                  <div className="mini-value">{dashboard.total_profiles}</div>
                </div>
                <div className="member-list">
                  {users.length > 0 ? (
                    users.map((user) => (
                      <div key={user.id} className="member-item">
                        <span>{user.username}</span>
                        <span className="member-id">#{user.id}</span>
                      </div>
                    ))
                  ) : (
                    <div className="table-empty">目前帳號沒有管理員權限，會員清單不可用。</div>
                  )}
                </div>
              </div>
            ) : (
              <div className="table-empty">登入後可查看受保護的會員與儀表板資料。</div>
            )}
          </section>
        </div>
      </main>
    </div>
  )
}
