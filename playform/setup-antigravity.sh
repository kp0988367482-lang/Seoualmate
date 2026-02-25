#!/bin/bash

# 🚀 Playform + Antigravity + GitHub 自動化主命令 (macOS/Linux)

echo "=== Playform AI Automation Setup ==="

# 1️⃣ Git 初始化
echo "[1/8] 初始化 Git..."
git config --global user.name "playform-dev"
git config --global user.email "dev@playform.ai"
git init
git add .
git commit -m "chore: Playform AI automation initial setup" 2>/dev/null || true

# 2️⃣ GitHub 設置
echo "[2/8] 設置 GitHub..."
read -p "Enter your GitHub username: " ownerName
git remote remove origin 2>/dev/null || true
git remote add origin "https://github.com/$ownerName/playform.git"

# 3️⃣ 安裝依賴
echo "[3/8] 安裝 Antigravity + LangChain..."
python3 -m pip install --quiet antigravity langchain chromadb openai firebase-admin pydantic

# 4️⃣ 創建 Agent 結構
echo "[4/8] 創建 AI Agent 結構..."
mkdir -p agents/youtube agents/saas agents/firebase workflows scripts

# 5️⃣ .github/workflows 目錄
echo "[5/8] 設置 GitHub Actions..."
mkdir -p .github/workflows

# 6️⃣ 複製工作流文件
cat > .github/workflows/ai-automation.yml << 'EOF'
name: Playform AI Automation

on:
  push:
    branches: [main, develop]
  schedule:
    - cron: "0 */12 * * *"

jobs:
  ai-automation:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install Dependencies
        run: |
          pip install antigravity langchain chromadb openai firebase-admin
      - name: Run AI Agents
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          FIREBASE_TOKEN: ${{ secrets.FIREBASE_TOKEN }}
        run: python main.py
EOF

# 7️⃣ 環境文件
echo "[6/8] 創建環境文件..."
cat > .env.example << 'EOF'
OPENAI_API_KEY=sk-...
FIREBASE_TOKEN=...
NOTION_API_KEY=ntn_...
PLAYFORM_API=http://127.0.0.1:8000
AUTO_DEPLOY=true
EOF

# 8️⃣ 最終提交
echo "[7/8] 完成設置..."
git add .
git commit -m "feat: Add Antigravity AI automation" 2>/dev/null || true

echo ""
echo "✅ Setup Complete!"
echo ""
echo "📋 下一步:"
echo "1. 設置 GitHub Secrets:"
echo "   - OPENAI_API_KEY"
echo "   - FIREBASE_TOKEN"
echo ""
echo "2. 運行本地測試:"
echo "   python3 main.py"
echo ""
echo "3. 推送到 GitHub:"
echo "   git push -u origin main"
echo ""
echo "🎉 Playform 自動化系統已準備就緒！"
