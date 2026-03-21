

function App() {
  return (
    <div className="admin-layout">
      <aside className="sidebar">
        <h2 style={{ marginBottom: 40, letterSpacing: -1 }}>Admin Panel</h2>
        <nav style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          <div style={{ color: '#fff', fontWeight: 600 }}>📊 總覽</div>
          <div style={{ color: '#94a3b8' }}>🕹️ 遊戲管理</div>
          <div style={{ color: '#94a3b8' }}>👥 用戶設定</div>
          <div style={{ color: '#94a3b8' }}>🔗 n8n 狀態</div>
        </nav>
      </aside>

      <main className="main-content">
        <header className="header">
          <h1 style={{ fontSize: '1.8rem', fontWeight: 700 }}>數據總覽</h1>
          <p style={{ color: '#64748b' }}>歡迎回來，管理員。這是您今天的專案動態。</p>
        </header>

        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-label">總訪問量</div>
            <div className="stat-value">12,840</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">新註冊用戶</div>
            <div className="stat-value">+156</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">n8n 觸發次數</div>
            <div className="stat-value">892</div>
          </div>
        </div>

        <div className="table-card">
          <div className="table-header">
            <h3 style={{ margin: 0 }}>近期遊戲動態</h3>
          </div>
          <table>
            <thead>
              <tr>
                <th>遊戲名稱</th>
                <th>建立者</th>
                <th>狀態</th>
                <th>時間</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>賽博龐克冒險</td>
                <td>admin</td>
                <td><span className="badge-active">已連動 n8n</span></td>
                <td>2 分鐘前</td>
              </tr>
              <tr>
                <td>星際大戰</td>
                <td>User01</td>
                <td><span className="badge-active">已連動 n8n</span></td>
                <td>15 分鐘前</td>
              </tr>
            </tbody>
          </table>
        </div>
      </main>
    </div>
  )
}

export default App
