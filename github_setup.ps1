# 🚀 GitHub 연결 & 첫 Push 스크립트
# 사용법: .\github_setup.ps1 -Username "your-github-username" -RepoName "playform"

param(
    [Parameter(Mandatory = $true)]
    [string]$Username,

    [Parameter(Mandatory = $false)]
    [string]$RepoName = "playform"
)

$RepoUrl = "https://github.com/$Username/$RepoName.git"

Write-Host "🔥 Playform GitHub 연결 시작..." -ForegroundColor Cyan
Write-Host "📍 저장소: $RepoUrl" -ForegroundColor Yellow

# ─── Git 사용자 정보 설정 ───────────────────────────────────────
Write-Host "`n[1/6] Git 사용자 정보 설정..." -ForegroundColor Green
git config user.name $Username
git config user.email "$Username@users.noreply.github.com"

# ─── Remote 추가 ───────────────────────────────────────────────
Write-Host "[2/6] GitHub Remote 연결..." -ForegroundColor Green
$currentRemote = git remote get-url origin 2>$null
if ($currentRemote) {
    Write-Host "  기존 Remote 발견: $currentRemote" -ForegroundColor Yellow
    git remote set-url origin $RepoUrl
    Write-Host "  ✅ Remote URL 업데이트 완료" -ForegroundColor Green
}
else {
    git remote add origin $RepoUrl
    Write-Host "  ✅ Remote 추가 완료" -ForegroundColor Green
}

# ─── .gitignore 확인 ───────────────────────────────────────────
Write-Host "[3/6] .gitignore 확인..." -ForegroundColor Green
if (-not (Test-Path ".gitignore")) {
    @"
node_modules/
.env
.env.local
*.pyc
__pycache__/
.venv/
*.db
dist/
build/
.DS_Store
*.log
mcp_server.log
playform.db
"@ | Out-File -FilePath ".gitignore" -Encoding utf8
    Write-Host "  ✅ .gitignore 생성 완료" -ForegroundColor Green
}
else {
    Write-Host "  ✅ .gitignore 이미 존재" -ForegroundColor Green
}

# ─── 첫 커밋 ───────────────────────────────────────────────────
Write-Host "[4/6] 파일 스테이징..." -ForegroundColor Green
git add .
git status --short

Write-Host "[5/6] 첫 커밋 생성..." -ForegroundColor Green
$commitMsg = "feat: Initial Playform monorepo setup

- apps/core: FastAPI backend + React frontend
- apps/admin: Admin dashboard
- apps/landing: Marketing landing page
- GitHub Actions: CI, Deploy, AI Review workflows
- Configured for Firebase + Vercel deployment"

git commit -m $commitMsg

# ─── Push ──────────────────────────────────────────────────────
Write-Host "[6/6] GitHub에 Push 중..." -ForegroundColor Green
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n🎉 성공! GitHub 저장소 확인: $RepoUrl" -ForegroundColor Cyan
    Write-Host "▶ https://github.com/$Username/$RepoName/actions — GitHub Actions 확인" -ForegroundColor Yellow
    Start-Process "https://github.com/$Username/$RepoName"
}
else {
    Write-Host "`n⚠️ Push 실패. GitHub에 '$RepoName' 저장소가 있는지 확인하세요:" -ForegroundColor Red
    Write-Host "  1. https://github.com/new 으로 이동" -ForegroundColor White
    Write-Host "  2. Repository name: $RepoName" -ForegroundColor White
    Write-Host "  3. Private/Public 선택 후 Create" -ForegroundColor White
    Write-Host "  4. 다시 이 스크립트 실행" -ForegroundColor White
}
