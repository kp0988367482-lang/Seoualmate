#!/usr/bin/env python3
"""
GitHub 저장소 자동 생성 및 초기화 스크립트
Playform AI Automation을 GitHub에 배포
"""

import subprocess
import os
import sys
from pathlib import Path


def run_command(cmd, description):
    """명령어 실행"""
    print(f"\n📍 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ 성공")
            if result.stdout:
                print(f"   {result.stdout.strip()[:100]}")
            return True
        else:
            print(f"❌ 실패")
            if result.stderr:
                print(f"   오류: {result.stderr.strip()[:100]}")
            return False
    except Exception as e:
        print(f"❌ 예외 발생: {e}")
        return False


def setup_github_repo():
    """GitHub 저장소 설정"""
    
    print("\n" + "="*60)
    print("🚀 Playform AI - GitHub 자동 배포 초기화")
    print("="*60)
    
    # 1️⃣  Git 설정
    print("\n1️⃣  Git 설정")
    run_command("git config --global user.email 'ai@playform.dev'", "Git 이메일 설정")
    run_command("git config --global user.name 'Playform AI'", "Git 사용자명 설정")
    
    # 2️⃣  .gitignore 생성
    print("\n2️⃣  .gitignore 설정")
    gitignore_content = """# Environment
.env
.env.local
.env.*.local

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST
.venv
venv/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Firebase
.firebaserc
firebase-debug.log
firebase-key.json

# Build
dist/
build/
*.log
.next/

# Node
node_modules/
npm-debug.log

# Logs
logs/
*.log
deployment_report_*.json
"""
    
    with open(".gitignore", "w") as f:
        f.write(gitignore_content)
    print("✅ .gitignore 생성")
    
    # 3️⃣  Git 초기화
    print("\n3️⃣  Git 저장소 초기화")
    
    if not Path(".git").exists():
        run_command("git init", "Git 저장소 초기화")
    
    # 4️⃣  파일 추가
    print("\n4️⃣  파일 추가")
    run_command("git add .", "모든 파일 스테이징")
    
    # 5️⃣  초기 커밋
    print("\n5️⃣  초기 커밋")
    run_command(
        'git commit -m "Initial commit: Playform AI Automation System with GitHub Actions"',
        "초기 커밋"
    )
    
    # 6️⃣  main 브랜치 설정
    print("\n6️⃣  Main 브랜치 설정")
    run_command("git branch -M main", "Main 브랜치로 변경")
    
    # 7️⃣  GitHub 저장소 연결 (사용자가 먼저 생성해야 함)
    print("\n7️⃣  GitHub 원격 저장소 연결")
    print("➤ GitHub Create 명령어:")
    print('   gh repo create playform-ai --public --source=. --remote=origin --push')
    print("")
    print("또는 기존 저장소가 있다면:")
    print("   git remote add origin https://github.com/{USERNAME}/playform-ai.git")
    print("   git push -u origin main")


def verify_secrets():
    """GitHub Secrets 검증"""
    
    print("\n" + "="*60)
    print("🔐 GitHub Secrets 설정 확인")
    print("="*60)
    
    required_secrets = {
        "OPENAI_API_KEY": "ChatGPT-4 API 키",
        "FIREBASE_TOKEN": "Firebase Admin SDK 키",
        "NOTION_API_KEY": "Notion API 키 (선택)",
        "YOUTUBE_API_KEY": "YouTube API 키 (선택)"
    }
    
    print("\n필요한 GitHub Secrets:")
    print("-" * 40)
    
    for secret_name, description in required_secrets.items():
        status = "✅ 필수" if "선택" not in description else "⚠️  선택사항"
        print(f"{status} {secret_name}: {description}")
    
    print("\nGitHub Secrets 설정 방법:")
    print("-" * 40)
    print("1. https://github.com/{USERNAME}/playform-ai/settings/secrets/actions")
    print("2. 'New repository secret' 클릭")
    print("3. Name: OPENAI_API_KEY")
    print("4. Value: sk-... (API 키)")
    print("5. 'Add secret' 클릭")
    print("")
    print("또는 GitHub CLI 사용:")
    print("   gh secret set OPENAI_API_KEY --body 'sk-...'")
    print("   gh secret set FIREBASE_TOKEN --body '@firebase-key.json'")
    

def show_deployment_flow():
    """배포 흐름 표시"""
    
    print("\n" + "="*60)
    print("🔄 자동 배포 흐름")
    print("="*60)
    
    flow = """
1. 로컬에서 코드 수정
   ↓
2. git push origin main
   ↓
3. GitHub Actions 트리거
   └─ .github/workflows/deploy.yml 실행
   └─ Test → Deploy Firebase → Deploy Cloud Run
   └─ Security Scan → Notify
   ↓
4. Firebase Hosting에 프론트엔드 배포
   └─ https://playform-prod.web.app
   ↓
5. Google Cloud Run에 백엔드 배포
   └─ https://playform-prod.run.app
   ↓
6. 매일 6시간마다 AI Agent 자동 실행
   ├─ 🎬 YouTube: 콘텐츠 생성
   ├─ ⚙️  SaaS: 기능 개발
   └─ 📢 Marketing: 마케팅 자동화
"""
    
    print(flow)


def main():
    print("🎯 Playform AI 배포 초기화 시작\n")
    
    # 1. GitHub 저장소 설정
    choice = input("GitHub 저장소를 초기화하시겠습니까? (y/n): ").lower()
    if choice == "y":
        setup_github_repo()
    
    # 2. Secrets 검증
    choice = input("\nGitHub Secrets 설정 방법을 보시겠습니까? (y/n): ").lower()
    if choice == "y":
        verify_secrets()
    
    # 3. 배포 흐름 표시
    choice = input("\n자동 배포 흐름을 보시겠습니까? (y/n): ").lower()
    if choice == "y":
        show_deployment_flow()
    
    print("\n" + "="*60)
    print("✅ 초기화 완료!")
    print("="*60)
    print("\n다음 단계:")
    print("1. GitHub 저장소 생성 및 설정")
    print("2. GitHub Secrets 추가")
    print("3. 로컬에서 테스트: python main_antigravity.py --demo")
    print("4. git push로 GPU Actions 트리거")
    print("")
    print("📖 더 자세한 정보: GETTING_STARTED.md")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ 초기화 중단됨")
        sys.exit(1)
