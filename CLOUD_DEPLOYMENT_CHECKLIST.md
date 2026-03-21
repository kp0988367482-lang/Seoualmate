# ☁️ 部署檢查清單 - Playform

## 📋 準備階段

### 1. 帳戶設置
- [ ] 擁有 Google Cloud 付費帳戶
- [ ] 擁有 Firebase 帳戶
- [ ] 已安裝 Google Cloud CLI (`gcloud`)
- [ ] 已安裝 Firebase CLI (`firebase`)
- [ ] 已安裝 Docker

### 2. 創建雲端項目
- [ ] Firebase 項目: **playform-prod**
- [ ] Google Cloud 項目: **playform-api-prod**
- [ ] 啟用服務:
  - [ ] Firebase Hosting
  - [ ] Firestore Database
  - [ ] Cloud Run
  - [ ] Container Registry

### 3. 認證和權限
- [ ] `firebase login` ✓
- [ ] `gcloud auth login` ✓
- [ ] `gcloud config set project playform-api-prod` ✓
- [ ] 創建服務帳戶和金鑰 ✓

---

## 🔐 GitHub Secrets 配置

### 在 GitHub 倉庫中設置以下 Secrets：

| Secret 名稱 | 來源 | 複製位置 |
|-----------|------|--------|
| `FIREBASE_TOKEN` | Firebase | `firebase login:ci` 輸出 |
| `FIREBASE_PROJECT_ID` | Firebase | `playform-prod` |
| `GCP_PROJECT_ID` | Google Cloud | `playform-api-prod` |
| `GCP_SA_KEY` | Google Cloud | 服務帳戶 JSON 金鑰 |
| `DATABASE_URL` | 自設 | PostgreSQL 連接字符串 |
| `OPENAI_API_KEY` | OpenAI | API 密鑰 |

**操作步驟：**
1. 進入倉庫 → Settings → Secrets and variables → Actions
2. 點擊 "New repository secret"
3. 輸入 Secret 名稱和值
4. 重複上列所有 Secrets

---

## 🚀 部署階段

### 第 1 步：本地測試

```powershell
# 1. 測試後端
cd apps/core/backend
uvicorn main:app --reload --port 8000

# 2. 測試前端
cd ../frontend
npm run dev

# 3. 測試 Docker 構建
docker build -t playform-api:test .
docker run -p 8080:8080 playform-api:test
```

- [ ] 後端 API 運行正常
- [ ] 前端頁面正常顯示
- [ ] Docker 容器成功啟動

### 第 2 步：部署 Firestore

```bash
# 部署 Firestore 規則
firebase deploy:firestore:rules --project playform-prod

# 部署 Firestore 索引
firebase deploy:firestore:indexes --project playform-prod
```

- [ ] Firestore 規則已部署
- [ ] Firestore 索引已建立
- [ ] 可在 Firebase Console 中驗證

### 第 3 步：推送到 GitHub

```bash
# 確保所有更改已提交
git add .
git commit -m "部署配置: Firebase + Cloud Run + GitHub Actions"
git push origin main
```

- [ ] 所有檔案已提交
- [ ] 推送成功

### 第 4 步：監控 GitHub Actions

1. 進入倉庫 → Actions
2. 查看 "自動化部署 - Firebase 和 Google Cloud" 工作流
3. 等待完成

**預期輸出：**
```
✅ Test: 通過
✅ Deploy Firebase: 成功
✅ Deploy Google Cloud Run: 成功
✅ Security Scan: 完成
```

---

## ✅ 部署驗證

### Firebase Hosting 驗證

```bash
# 前端已部署到：
firebase open hosting:site --project playform-prod

# 或直接訪問：
# https://playform-prod.web.app
```

- [ ] 前端頁面正常加載
- [ ] 所有資源已加載
- [ ] 沒有 404 錯誤

### Google Cloud Run 驗證

```bash
# 獲取服務 URL
gcloud run services describe playform-api --region us-central1

# 或直接查看：
# https://console.cloud.google.com/run?project=playform-api-prod
```

- [ ] API 服務已部署
- [ ] 可訪問 `/docs` Swagger 文檔
- [ ] 測試 API 端點返回正常

### Firestore 驗證

```bash
# 在 Firebase Console 中檢查：
# https://console.firebase.google.com/firestore/databases
```

- [ ] Firestore 資料庫已創建
- [ ] 測試集合可見
- [ ] 規則已應用

---

## 📊 監控設置

### 1. Firebase 監控

```bash
firebase functions:log --project playform-prod

firebase hosting:channel:list --project playform-prod
```

### 2. Google Cloud 監控

```bash
# 查看 Cloud Run 日誌
gcloud run logs read playform-api --region us-central1 --limit 100

# 查看指標
gcloud monitoring metrics-descriptors list
```

### 3. 設置告警

在 Google Cloud Console 中：
1. Navigation → Monitoring → Alerting Policies
2. 創建新告警
3. 條件範例：
   - Cloud Run 錯誤率 > 1%
   - 反應時間 > 1000ms
   - Firestore 讀取超額

---

## 🔄 持續更新流程

**每次更新只需：**

```bash
# 1. 開發並測試
git checkout -b feature/new-feature
# ... 開發代碼 ...

# 2. 提交
git add .
git commit -m "功能: 新功能描述"

# 3. 推送
git push origin feature/new-feature

# 4. 創建 Pull Request
# GitHub 上點擊 "Create Pull Request"

# 5. 自動測試和部署
# GitHub Actions 自動執行
# 部署到 Preview + Production
```

---

## 🛠️ 故障排除

### 問題 1: GitHub Actions 失敗

```
❌ Error: Firebase token invalid
```

**解決方案：**
```bash
# 重新生成 token
firebase login:ci

# 更新 GitHub Secret
# Settings → Secrets → Update FIREBASE_TOKEN
```

### 問題 2: Cloud Run 部署失敗

```
❌ Cloud Run service failed to start
```

**解決方案：**
```bash
# 檢查本地 Docker 構建
docker build -t playform-api:test apps/core/backend/
docker run -p 8080:8080 playform-api:test

# 檢查日誌
gcloud run logs read playform-api --region us-central1
```

### 問題 3: Firestore 權限錯誤

```
❌ Permission denied on document
```

**解決方案：**
```bash
# 測試規則
firebase rules:test

# 更新規則
# 編輯 firestore.rules 並重新部署
firebase deploy:firestore:rules
```

---

## 📈 性能優化

### 1. CDN 緩存

```bash
# Firebase Hosting 自動啟用 CDN
# 在 firebase.json 中配置：
{
  "hosting": {
    "headers": [{
      "source": "**/*.{js,css}",
      "headers": [{
        "key": "Cache-Control",
        "value": "max-age=31536000"
      }]
    }]
  }
}
```

### 2. Cloud Run 自動擴展

```bash
gcloud run deploy playform-api \
  --max-instances 100 \
  --memory 512Mi \
  --cpu 1 \
  --timeout 3600
```

### 3. Firestore 最佳實踐

```python
# ✅ 使用批量操作
batch = db.batch()
batch.set(doc1, data1)
batch.set(doc2, data2)
batch.commit()

# ✅ 添加索引
# 自動建議或在 firestore.indexes.json 中定義

# ❌ 避免
# - 大集合掃描
# - 深層子集合
# - 無界查詢
```

---

## 🎉 完成狀態

部署完成後，你的應用架構將是：

```
用戶 → CloudFlare CDN → Firebase Hosting (前端)
                    ↓
                 API → Google Cloud Run (後端)
                    ↓
                Firestore (資料庫)
```

**每次推送 main 分支後：**
1. GitHub Actions 自動測試
2. 構建 Docker 映像
3. 部署到生產環境
4. 自動化監控和告警

---

✅ **所有檢查完成！部署成功！** 🚀
