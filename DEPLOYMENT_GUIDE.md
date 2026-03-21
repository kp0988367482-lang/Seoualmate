# 📦 Playform - 完整部署指南

## 🌍 部署架構

```
┌─────────────────────────────────────────────────────┐
│                  GitHub Actions                      │
│  自動檢測推送 → 測試 → 構建 → 部署                 │
└──────────────┬─────────────────────────────────────┘
               │
       ┌───────┴───────┐
       │               │
   ┌──▼───┐      ┌───▼───┐
   │Firebase   │  Google
   │Hosting    │  Cloud Run
   │+ Firestore│  
   └────────┘      └────────┘
   React 前端      FastAPI 後端
```

## 1️⃣ 前置準備

### 1.1 創建 Firebase 項目

```bash
# 訪問 https://console.firebase.google.com
# 1. 點擊 "新增專案"
# 2. 名稱輸入: playform-prod
# 3. 選擇區域: Asia-East1 (台灣)
# 4. 啟用 Firestore Database
# 5. 啟用 Hosting
```

### 1.2 創建 Google Cloud 項目

```bash
# 訪問 https://console.cloud.google.com/projectcreate
# 1. 項目名稱: playform-api-prod
# 2. 啟用 APIs:
#    - Cloud Run
#    - Container Registry
#    - Cloud SQL (可選)
#    - Firestore
```

### 1.3 本地登入 Firebase

```powershell
# 在 Windows PowerShell 中
npm install -g firebase-tools

# 登入 Firebase
firebase login

# 初始化 Firebase (已完成，配置檔在 firebase.json)
# firebase init hosting firestore functions
```

## 2️⃣ 配置 GitHub Secrets

### 在 GitHub 上配置所需的密鑰

1. **進入倉庫** → Settings → Secrets and variables → Actions
2. **新增以下 Secrets**:

#### Firebase 部署
```
FIREBASE_TOKEN = <firebase login:ci 生成的令牌>
FIREBASE_PROJECT_ID = playform-prod
```

#### Google Cloud
```
GCP_PROJECT_ID = playform-api-prod
GCP_SA_KEY = <服務帳戶金鑰 JSON>
```

#### 應用密鑰
```
DATABASE_URL = postgresql://user:pass@host/db
OPENAI_API_KEY = sk-...
```

### 2.1 生成 Firebase Token

```bash
firebase login:ci

# 輸出:
# ✔ Success! Use this token to login on a CI server:
# <your-firebase-token>

# 複製此 Token 到 GitHub Secrets 中的 FIREBASE_TOKEN
```

### 2.2 生成 Google Cloud 服務帳戶

```bash
# 在 Google Cloud Console (https://console.cloud.google.com)
# 1. 進入 "服務帳戶" 
# 2. 創建新服務帳戶: playform-ci-deploy
# 3. 授予角色:
#    - Cloud Run 管理員
#    - Artifact Registry 寫入者
#    - Service Account User
# 4. 創建金鑰 → JSON
# 5. 下載的 JSON 內容貼到 GitHub Secrets 中的 GCP_SA_KEY
```

## 3️⃣ 部署流程

### 3.1 本地快速部署（開發）

```powershell
# Backend to Firebase Functions (如果有)
cd apps/core/backend
firebase deploy --only functions

# Frontend to Firebase Hosting
cd ../frontend
npm run build
firebase deploy --only hosting

# Backend to Google Cloud Run (使用 gcloud CLI)
gcloud run deploy playform-api \
  --source apps/core/backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### 3.2 自動化 CI/CD 部署

**當你推送至 main 分支時，自動執行**:

```bash
git add .
git commit -m "新功能: 完成用戶認證"
git push origin main

# ✅ GitHub Actions 自動:
# 1. 執行測試 (pytest)
# 2. 構建 Docker 映像
# 3. 部署到 Firebase Hosting
# 4. 部署後端到 Google Cloud Run
# 5. 更新 Firestore 規則和索引
# 6. 發送部署通知
```

## 4️⃣ Firebase Firestore 配置

### 4.1 集合結構

```
firestore/
├── users/
│   └── {userId}/
│       ├── displayName: string
│       ├── email: string
│       ├── createdAt: timestamp
│       └── subscription: map
│
├── games/
│   └── {gameId}/
│       ├── creatorId: string
│       ├── title: string
│       ├── description: string
│       ├── isPublic: boolean
│       └── createdAt: timestamp
│
└── analytics/
    └── {userId}/
        ├── dailyActiveUsers: number
        ├── totalRevenue: number
        └── date: timestamp
```

### 4.2 在後端使用 Firestore

```python
# apps/core/backend/main.py
from firebase_admin import firestore

db = firestore.client()

# 添加文檔
def create_game(user_id: str, game_data: dict):
    db.collection('games').add({
        'creatorId': user_id,
        'createdAt': firestore.SERVER_TIMESTAMP,
        **game_data
    })

# 查詢文檔
def get_user_games(user_id: str):
    games = db.collection('games')\
        .where('creatorId', '==', user_id)\
        .order_by('createdAt', direction=firestore.Query.DESCENDING)\
        .stream()
    
    return [doc.to_dict() for doc in games]

# 更新文檔
def update_game(game_id: str, updates: dict):
    db.collection('games').document(game_id).update(updates)

# 刪除文檔
def delete_game(game_id: str):
    db.collection('games').document(game_id).delete()
```

### 4.3 前端使用 Firestore

```javascript
// apps/core/frontend/src/firebase.js
import { getFirestore, collection, query, where } from 'firebase/firestore'

const db = getFirestore()

// 查詢
import { getDocs } from 'firebase/firestore'

export async function getUserGames(userId) {
  const q = query(
    collection(db, 'games'),
    where('creatorId', '==', userId)
  )
  const snapshot = await getDocs(q)
  return snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }))
}

// 即時訂閱
import { onSnapshot } from 'firebase/firestore'

export function subscribeToUserGames(userId, callback) {
  const q = query(collection(db, 'games'), where('creatorId', '==', userId))
  return onSnapshot(q, snapshot => {
    callback(snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() })))
  })
}
```

## 5️⃣ Docker 部署（Google Cloud Run）

### 5.1 Dockerfile

```dockerfile
# apps/core/backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 複製依賴
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製程式碼
COPY . .

# 暴露端口
EXPOSE 8080

# 運行應用
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

### 5.2 本地構建和測試

```bash
# 構建 Docker 映像
docker build -t playform-api:latest apps/core/backend/

# 本地運行
docker run -p 8080:8080 playform-api:latest

# 訪問 http://localhost:8080/docs
```

## 6️⃣ 監控和日誌

### 6.1 Firebase Console

- Hosting 日誌: https://console.firebase.google.com/hosting/sites
- Firestore 監控: https://console.firebase.google.com/firestore
- 雲端函數日誌: https://console.firebase.google.com/functions

### 6.2 Google Cloud 監控

```bash
# 查看 Cloud Run 日誌
gcloud run logs read playform-api --limit 50

# 即時尾隨日誌
gcloud run logs read playform-api --limit 50 --follow
```

### 6.3 GitHub Actions 監控

1. 進入倉庫 → Actions
2. 查看最新部署工作流
3. 點擊查看詳細日誌

## 7️⃣ 常見問題排除

### 部署失敗: "Firebase Token 無效"

```bash
# 重新生成 Token
firebase login:ci

# 更新 GitHub Secrets
# Settings → Secrets → Update FIREBASE_TOKEN
```

### Cloud Run 部署失敗: "容器未啟動"

```bash
# 檢查本地 Docker 構建
docker build -t playform-api:test apps/core/backend/
docker run -p 8080:8080 playform-api:test

# 檢查端口是否正確
# Dockerfile 需要使用 8080 (Cloud Run 要求)
```

### Firestore 權限錯誤

```bash
# 檢查規則配置
firebase rules:test

# 驗證服務帳戶權限
# GCP Console → IAM & Admin → 檢查服務帳戶角色
```

## 📊 部署檢查清單

- [ ] Firebase 項目已創建 (playform-prod)
- [ ] Google Cloud 項目已創建 (playform-api-prod)
- [ ] GitHub Secrets 已配置:
  - [ ] FIREBASE_TOKEN
  - [ ] GCP_SA_KEY
  - [ ] OPENAI_API_KEY
  - [ ] DATABASE_URL
- [ ] Firestore 規則已部署
- [ ] Firestore 索引已部署
- [ ] Docker 映像在本地測試成功
- [ ] GitHub Actions 工作流已觸發
- [ ] Firebase Hosting 顯示最新前端
- [ ] Cloud Run 服務正常運行
- [ ] 監控和告警已配置

## 🚀 後續優化

```python
# 1. 設置 Firestore 備份
# 2. 啟用 Cloud CDN 加速
# 3. 配置自動擴展
# 4. 設置價格預警
# 5. 配置藍綠部署策略
```

---

**部署完成！🎉** 

你的應用現在:
- ✅ 前端在 Firebase Hosting
- ✅ 後端在 Google Cloud Run
- ✅ 資料庫在 Firestore
- ✅ 自動 CI/CD 流程
