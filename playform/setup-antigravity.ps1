# 🚀 Playform + Antigravity + GitHub 自動化主命令
# 一條命令啟動整個 AI 自動化系統

Write-Host "=== Playform AI Automation Setup ===" -ForegroundColor Cyan

# 1️⃣ Git 初始化
Write-Host "`n[1/8] 初始化 Git..." -ForegroundColor Yellow
git config --global user.name "playform-dev"
git config --global user.email "dev@playform.ai"
gh auth login 2>$null
git init
git add .
git commit -m "chore: Playform AI automation initial setup" 2>$null

# 2️⃣ GitHub 設置
Write-Host "[2/8] 設置 GitHub..." -ForegroundColor Yellow
$repoName = "playform"
$ownerName = Read-Host "Enter your GitHub username"
git remote remove origin 2>$null
git remote add origin "https://github.com/$ownerName/$repoName.git"

# 3️⃣ 安裝 Antigravity + AI 工具
Write-Host "[3/8] 安裝 Antigravity + LangChain..." -ForegroundColor Yellow
python -m pip install --quiet antigravity langchain chromadb openai firebase-admin pydantic

# 4️⃣ 創建 Agent 結構
Write-Host "[4/8] 創建 AI Agent 結構..." -ForegroundColor Yellow
$agentDirs = @(
    "agents",
    "agents/youtube",
    "agents/saas",
    "agents/firebase",
    "workflows",
    "scripts"
)

foreach ($dir in $agentDirs) {
    New-Item -Path $dir -ItemType Directory -Force | Out-Null
}

# 5️⃣ 創建主 Agent 文件
Write-Host "[5/8] 創建 AI Agent 文件..." -ForegroundColor Yellow

# main.py
$mainPy = @'
import os
import sys
from pathlib import Path

# Antigravity + LangChain Setup
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from agents.youtube.auto_content import run_youtube_agent
from agents.saas.auto_feature import run_saas_agent
from agents.firebase.auto_deploy import run_firebase_agent

# Initialize OpenAI
llm = ChatOpenAI(
    model="gpt-4",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.7
)

def run_all_agents():
    """Run all AI automation agents"""
    print("🚀 Starting Playform AI Automation...")
    
    try:
        print("\n📺 Running YouTube Agent...")
        run_youtube_agent(llm)
        
        print("\n🛠️ Running SaaS Feature Agent...")
        run_saas_agent(llm)
        
        print("\n🔥 Running Firebase Deploy Agent...")
        run_firebase_agent(llm)
        
        print("\n✅ All agents completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_all_agents()
'@

Set-Content -Path "main.py" -Value $mainPy

# 6️⃣ 創建 GitHub Actions
Write-Host "[6/8] 設置 GitHub Actions..." -ForegroundColor Yellow

$githubDir = ".github\workflows"
New-Item -Path $githubDir -ItemType Directory -Force | Out-Null

$workflowYml = @'
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
          pip install -r apps/core/backend/requirements.txt
      
      - name: Run AI Agents
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          FIREBASE_TOKEN: ${{ secrets.FIREBASE_TOKEN }}
          NOTION_API_KEY: ${{ secrets.NOTION_API_KEY }}
        run: |
          python main.py
      
      - name: Auto Commit Changes
        if: success()
        run: |
          git config --global user.name "playform-ai"
          git config --global user.email "ai@playform.dev"
          git add .
          git commit -m "chore: AI automation update" || true
          git push origin main
'@

Set-Content -Path "$githubDir\ai-automation.yml" -Value $workflowYml

# 7️⃣ 創建環境文件
Write-Host "[7/8] 設置環境文件..." -ForegroundColor Yellow

$envExample = @'
# AI 自動化配置
OPENAI_API_KEY=sk-...
FIREBASE_TOKEN=...
NOTION_API_KEY=ntn_...

# Playform API
PLAYFORM_API=http://127.0.0.1:8000

# YouTube 自動化
YOUTUBE_API_KEY=...
YOUTUBE_CHANNEL_ID=...

# 自動化設置
AUTO_DEPLOY=true
AUTO_COMMIT=true
AUTO_NOTIFY=true
'@

Set-Content -Path ".env.example" -Value $envExample

# 8️⃣ 最終設置
Write-Host "[8/8] 完成最後設置..." -ForegroundColor Yellow

git add .
git commit -m "feat: Add Antigravity AI automation" 2>$null
git push -u origin main 2>$null

Write-Host "`n✅ Setup Complete!" -ForegroundColor Green
Write-Host "`n📋 下一步:" -ForegroundColor Cyan
Write-Host "1. 設置 GitHub Secrets:
   - OPENAI_API_KEY
   - FIREBASE_TOKEN
   - NOTION_API_KEY" -ForegroundColor White

Write-Host "`n2. 運行本地測試:" -ForegroundColor White
Write-Host "   python main.py" -ForegroundColor Green

Write-Host "`n3. 推送到 GitHub:" -ForegroundColor White
Write-Host "   git push origin main" -ForegroundColor Green

Write-Host "`n4. 查看自動化:" -ForegroundColor White
Write-Host "   https://github.com/$ownerName/$repoName/actions" -ForegroundColor Green
