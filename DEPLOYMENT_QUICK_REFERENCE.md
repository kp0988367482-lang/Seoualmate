# 🌍 部署快速參考 - Playform

## 一鍵部署命令

### 1️⃣ 本地測試（開發環境）

```powershell
# 啟動後端
cd apps/core/backend
.\\.venv\Scripts\activate
uvicorn main:app --reload --port 8000

# 新終端 - 啟動前端
cd apps/core/frontend
npm run dev

# 訪問
# Frontend: http://localhost:5173
# Backend:  http://localhost:8000/docs
```

### 2️⃣ Docker 本地測試

```bash
# 構建
docker build -t playform-api:test apps/core/backend/

# 運行
docker run -p 8080:8080 \
  -e DATABASE_URL=postgresql://... \
  -e OPENAI_API_KEY=sk-... \
  playform-api:test

# 測試
curl http://localhost:8080/docs
```

### 3️⃣ Firebase 部署（前端）

```bash
# 登入
firebase login

# 部署前端
cd apps/core/frontend
npm run build
firebase deploy --only hosting --project playform-prod

# 查看
firebase open hosting --project playform-prod
```

### 4️⃣ Google Cloud Run 部署（後端）

```bash
# 配置
gcloud config set project playform-api-prod

# 部署
gcloud run deploy playform-api \
  --source apps/core/backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1

# 查看日誌
gcloud run logs read playform-api --limit 50 --follow
```

### 5️⃣ GitHub Actions 自動部署

```bash
# 只需推送到 main！
git add .
git commit -m "特性: 新功能"
git push origin main

# ✅ 自動執行:
# - 測試 (pytest)
# - 構建 Docker
# - 部署 Firebase
# - 部署 Cloud Run
# - 安全掃描
```

---

## 🔑 必需的 GitHub Secrets

| Secret | 來源 | 命令 |
|--------|------|------|
| `FIREBASE_TOKEN` | Firebase CLI | `firebase login:ci` |
| `FIREBASE_PROJECT_ID` | 手動輸入 | `playform-prod` |
| `GCP_PROJECT_ID` | Google Cloud | `playform-api-prod` |
| `GCP_SA_KEY` | GCP 服務帳戶 | 下載 JSON 金鑰 |
| `OPENAI_API_KEY` | OpenAI | `sk-...` |
| `DATABASE_URL` | 自設 | `postgresql://...` |

**配置位置**: GitHub 倉庫 → Settings → Secrets and variables → Actions

---

## 📊 部署後驗證

```bash
# 前端
open https://playform-prod.web.app

# 後端 API
curl https://playform-api-xxxxx.run.app/docs

# 資料庫
open https://console.firebase.google.com/firestore

# 監控
open https://console.cloud.google.com/run

# GitHub Actions
open https://github.com/your-org/playform/actions
```

---

## ❌ 常見錯誤和修復

```bash
# 錯誤: Firebase token 無效
$ firebase login:ci
$ 更新 FIREBASE_TOKEN secret

# 錯誤: GCP 認證失敗
$ gcloud auth configure-docker
$ 下載新的服務帳戶金鑰

# 錯誤: Cloud Run 容器啟動失敗
$ docker run -p 8080:8080 playform-api:test
$ 檢查 Dockerfile PORT 設置為 8080

# 錯誤: Firestore 權限拒絕
$ firebase rules:test
$ firebase deploy:firestore:rules --project playform-prod
```

---

## 📈 監控儀表板

### Firebase Console
```
https://console.firebase.google.com/project/playform-prod
```

### Google Cloud Console  
```
https://console.cloud.google.com/run?project=playform-api-prod
```

### GitHub Actions
```
https://github.com/your-org/playform/actions
```

---

## 🎯 典型部署流程

```
1. 開發功能
   ↓
2. git push origin main
   ↓
3. GitHub Actions 自動觸發
   ├─ ✅ 測試
   ├─ ✅ 構建
   ├─ ✅ 部署前端 → Firebase
   ├─ ✅ 部署後端 → Cloud Run
   └─ ✅ 安全掃描
   ↓
4. 驗證部署
   ├─ 訪問 https://playform-prod.web.app
   ├─ 測試 API 端點
   └─ 查看監控日誌
   ↓
5. ✅ 完成！
```

---

## 🚀 效能提示

```bash
# 本地開發 - 使用 uvicorn reload
uvicorn main:app --reload

# 生產環境 - 使用 gunicorn 多工作進程
gunicorn -w 4 -b 0.0.0.0:8080 main:app

# 緩存 npm 依賴
npm ci --prefer-offline --no-audit

# 緩存 pip 依賴
pip install --cache-dir ~/.cache/pip -r requirements.txt
```

---

**需要幫助？查看**：
- 📖 [完整部署指南](./DEPLOYMENT_GUIDE.md)
- ✅ [檢查清單](./CLOUD_DEPLOYMENT_CHECKLIST.md)
- 🔧 [Firestore 配置](./firebase.json)
- 🐳 [Docker 配置](./apps/core/backend/Dockerfile)
