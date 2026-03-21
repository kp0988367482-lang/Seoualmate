import React, { useEffect, useRef, useState } from 'react'
import { fetchPublicProfiles } from './lib/api'
import './index.css'

const HOW_CARDS = [
  {
    num: '01',
    title: '一對一真人陪跑',
    desc: '每位顧問只服務少量會員，不只是轉交檔案，而是根據你的狀態調整聊天、見面與節奏安排。',
  },
  {
    num: '02',
    title: '資料化精準配對',
    desc: '根據累積媒合紀錄、興趣標籤與互動反饋，優先推薦真正有機會發展關係的對象。',
  },
  {
    num: '03',
    title: '從配對到見面都跟進',
    desc: '不是只把人丟給你。從初聊、約見到見後回饋，整段流程都有真人協助推進。',
  },
]

const TESTIMONIALS = [
  { name: '37 歲軟體工程師', days: '68 天開始交往', text: '平常工作圈太封閉，過去總是聊到一半就冷掉。顧問幫我抓出問題之後，兩個月內就和現在的女友穩定交往。' },
  { name: '32 歲自營工作者', days: '30 天開始交往', text: '以前完全不會聊天，連訊息節奏都抓不到。這裡不只給名單，還會把每一步都陪你練過。' },
  { name: '40 歲藥師', days: '85 天開始交往', text: '用了兩年交友軟體還是沒結果，換到這裡後只收到真正適合我的人，對話自然很多。' },
  { name: '35 歲公職', days: '40 天開始交往', text: '原本半信半疑，但顧問真的很會抓我的狀態，幫我重新建立約會節奏，最後順利脫單。' },
  { name: '30 歲研究生', days: '44 天開始交往', text: '我常常曖昧到一半就消失，後來才知道自己在關鍵時刻太保守。調整之後，整個進展快很多。' },
  { name: '38 歲公務員', days: '39 天開始交往', text: '我原本覺得自己條件普通，但顧問把我的優勢重新整理出來，很快就遇到願意深聊的人。' },
]

const FEED_ITEMS = [
  { name: '35 歲林先生', result: '68 天開始交往', date: '06.16' },
  { name: '31 歲陳先生', result: '30 天開始交往', date: '06.16' },
  { name: '33 歲黃小姐', result: '95 天開始交往', date: '06.15' },
  { name: '24 歲張小姐', result: '13 天成功配對', date: '06.15' },
  { name: '38 歲王先生', result: '64 天開始交往', date: '06.14' },
  { name: '38 歲李小姐', result: '111 天開始交往', date: '06.14' },
  { name: '36 歲吳先生', result: '成功安排首次見面', date: '06.13' },
]

function useCountdown(targetDate) {
  const [time, setTime] = useState({ d: 0, h: 0, m: 0, s: 0 })

  useEffect(() => {
    const tick = () => {
      const diff = new Date(targetDate) - new Date()
      if (diff <= 0) {
        setTime({ d: 0, h: 0, m: 0, s: 0 })
        return
      }

      setTime({
        d: Math.floor(diff / 86400000),
        h: Math.floor((diff % 86400000) / 3600000),
        m: Math.floor((diff % 3600000) / 60000),
        s: Math.floor((diff % 60000) / 1000),
      })
    }

    tick()
    const id = setInterval(tick, 1000)
    return () => clearInterval(id)
  }, [targetDate])

  return time
}

function useReveal() {
  useEffect(() => {
    const elements = document.querySelectorAll('.reveal')
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible')
          observer.unobserve(entry.target)
        }
      })
    }, { threshold: 0.15 })

    elements.forEach((element) => observer.observe(element))
    return () => observer.disconnect()
  }, [])
}

export default function App() {
  const [profileCount, setProfileCount] = useState(null)
  const countdown = useCountdown('2026-06-30T23:59:59')
  useReveal()

  useEffect(() => {
    let active = true

    async function loadProfiles() {
      try {
        const profiles = await fetchPublicProfiles()
        if (active) {
          setProfileCount(profiles.length)
        }
      } catch {
        if (active) {
          setProfileCount(null)
        }
      }
    }

    loadProfiles()
    return () => {
      active = false
    }
  }, [])

  const stats = [
    { num: '20,000+', label: '累積媒合次數' },
    { num: '8,500+', label: '累積會員數' },
    { num: '91.3%', label: '服務滿意度' },
    { num: profileCount === null ? '--' : `${profileCount}+`, label: '目前公開檔案' },
  ]

  const pad = (value) => String(value).padStart(2, '0')
  const allTestimonials = [...TESTIMONIALS, ...TESTIMONIALS]
  const initials = (name) => name.slice(0, 1)

  return (
    <>
      <section className="hero" id="top">
        <div className="hero-bg" />

        <div className="badge-top">
          <span className="badge-dot" />
          2026 年 6 月限量開放，額滿即止
        </div>

        <h1 className="hero-title">
          誰都能幫你配對<br />
          <span className="highlight">真正開始交往</span>才算數
        </h1>

        <p className="hero-subtitle">
          SEOULMATE 顧問以一對一方式陪你走完整個配對流程。
          多數會員會在 3 個月內完成第一次高品質見面。
        </p>

        <div className="stats-row">
          {stats.map((stat, index) => (
            <React.Fragment key={stat.label}>
              <div className="stat-item">
                <div className="stat-num">{stat.num}</div>
                <div className="stat-label">{stat.label}</div>
              </div>
              {index < stats.length - 1 && <div className="stat-divider" />}
            </React.Fragment>
          ))}
        </div>

        <div className="hero-cta">
          <a href="#apply" className="btn-primary" id="hero-cta-btn">
            立即預約免費諮詢 →
          </a>
          <a href="#how" className="btn-ghost" id="hero-how-btn">
            了解服務方式
          </a>
        </div>
      </section>

      <div className="countdown-bar">
        <div className="countdown-inner">
          <span className="countdown-label">🔥 截止倒數</span>
          <div className="countdown-timer">
            <div className="cd-block">
              <div className="cd-num">{pad(countdown.d)}</div>
              <div className="cd-unit">日</div>
            </div>
            <span className="cd-sep">:</span>
            <div className="cd-block">
              <div className="cd-num">{pad(countdown.h)}</div>
              <div className="cd-unit">時</div>
            </div>
            <span className="cd-sep">:</span>
            <div className="cd-block">
              <div className="cd-num">{pad(countdown.m)}</div>
              <div className="cd-unit">分</div>
            </div>
            <span className="cd-sep">:</span>
            <div className="cd-block">
              <div className="cd-num">{pad(countdown.s)}</div>
              <div className="cd-unit">秒</div>
            </div>
          </div>
          <span className="countdown-label">本期名額滿額後將提前關閉</span>
        </div>
      </div>

      <div id="how">
        <div className="section">
          <h2 className="section-title reveal">跟交友軟體或婚介所<br />到底差在哪？</h2>
          <p className="section-subtitle reveal">不是只給名單，而是一路陪你把關係推進到真正見面。</p>
          <div className="how-grid">
            {HOW_CARDS.map((card) => (
              <div key={card.num} className="how-card reveal">
                <div className="how-num">{card.num}</div>
                <div className="how-title">{card.title}</div>
                <p className="how-desc">{card.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="testimonials-wrapper">
        <div className="testimonials-header">
          <h2 className="section-title">🔥 十位申請者中，九位成功進入穩定互動</h2>
          <p className="section-subtitle" style={{ marginBottom: 0 }}>
            以完成正式見面並持續聯繫的會員案例為基準
          </p>
        </div>
        <div className="scroll-track">
          {allTestimonials.map((item, index) => (
            <div key={`${item.name}-${index}`} className="testi-card">
              <div className="testi-header">
                <div className="testi-avatar">{initials(item.name)}</div>
                <div>
                  <div className="testi-name">{item.name}</div>
                  <div className="testi-meta">真實會員回饋</div>
                </div>
                <div className="testi-badge">✓ {item.days}</div>
              </div>
              <p className="testi-text">{item.text}</p>
            </div>
          ))}
        </div>
      </div>

      <div className="live-feed">
        <h2 className="feed-title reveal">今天也持續更新的<br />戀愛進展通知</h2>
        <p className="feed-sub reveal">如果你一直停在原地，感情也不會自己往前走。</p>
        <div className="feed-list">
          {FEED_ITEMS.map((item, index) => (
            <div key={`${item.name}-${item.date}`} className="feed-item reveal" style={{ animationDelay: `${index * 0.1}s` }}>
              <span className="feed-new">NEW</span>
              <div className="feed-content">
                <div className="feed-name">{item.name}</div>
                <div className="feed-result">{item.result} 🎉</div>
              </div>
              <span className="feed-date">{item.date}</span>
            </div>
          ))}
        </div>
      </div>

      <section className="final-cta" id="apply">
        <h2 className="reveal">把一直拖著的感情課題<br />這次好好解決</h2>
        <p className="reveal">3 個月內沒有明顯進展，我們會延長陪跑期，讓你無壓力開始。</p>
        <div className="hero-cta reveal">
          <a href="#top" className="btn-primary" id="final-cta-btn" style={{ padding: '20px 56px', fontSize: '1.15rem' }}>
            預約免費諮詢 →
          </a>
        </div>
      </section>
    </>
  )
}
