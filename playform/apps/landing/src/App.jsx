import React from 'react'

function App() {
  return (
    <div className="landing-container">
      <div className="bg-glow"></div>

      <nav className="nav">
        <div className="logo">PLAYFORM</div>
        <div className="nav-links">
          <a href="#features" className="nav-link">功能特色</a>
          <a href="#about" className="nav-link">關於我們</a>
          <a href="#" className="nav-link">開發文檔</a>
        </div>
        <a href="http://localhost:5173" className="btn-cta-nav">進入平台</a>
      </nav>

      <main>
        <section className="hero">
          <span className="badge animate">Explore the Gaming Universe</span>
          <h1 className="hero-title animate delay-1">打造您的<br />數位遊戲生態</h1>
          <p className="hero-subtitle animate delay-2">
            Playform 是下一代的遊戲平台解決方案。整合即時通知、強大的管理後台與絕佳的用戶體驗。
          </p>
          <div className="hero-btns animate delay-3">
            <button className="btn-primary">立即開始 — 免費</button>
            <button className="btn-secondary">觀看演示</button>
          </div>
        </section>

        <section id="features" className="features">
          <div className="feature-card animate">
            <div className="feature-icon">🎮</div>
            <h3 className="feature-h">核心平台</h3>
            <p className="feature-p">具備強大後端的遊戲管理系統，支援多語系與即時回應。</p>
          </div>
          <div className="feature-card animate delay-1">
            <div className="feature-icon">⚡</div>
            <h3 className="feature-h">自動化工作流</h3>
            <p className="feature-p">整合 n8n 工作流，讓您的遊戲事件自動觸發 Discord、電子郵件與數據追蹤。</p>
          </div>
          <div className="feature-card animate delay-2">
            <div className="feature-icon">📊</div>
            <h3 className="feature-h">專業後台</h3>
            <p className="feature-p">專為管理員設計的數據看板，掌握每一場遊戲與用戶的動態。</p>
          </div>
        </section>
      </main>

      <footer style={{ padding: '60px 5%', textAlign: 'center', borderTop: '1px solid var(--glass-border)', color: 'var(--text-secondary)', fontSize: '0.8rem' }}>
        &copy; 2026 PLAYFORM ECOSYSTEM. ALL RIGHTS RESERVED.
      </footer>
    </div>
  )
}

export default App
