# 🚀 Getting Started - Playform AI Automation

**5분 안에 AI 자동화 시스템 시작하기**

---

## 📋 사전 요구사항

- ✅ Python 3.11 이상
- ✅ Node.js 18+
- ✅ OpenAI API Key (ChatGPT-4)
- ✅ GitHub 계정 (자동 배포용)

---

## 🎯 Step 1: 환경 설정

### 1.1 Python 가상환경 생성

```powershell
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 1.2 필수 패키지 설치

```powershell
pip install langchain langchain-openai python-dotenv pytest-asyncio
```

### 1.3 .env 파일 선택

```powershell
# 빠른 시작 (추천)
cp .env.simple .env

# 또는 전체 기능
cp .env.complete .env

# 또는 프로덕션 배포
cp .env.production .env
```

### 1.4 API Key 설정

**.env 파일 편집:**

```env
OPENAI_API_KEY=sk-your-api-key-here
PLAYFORM_API=http://localhost:8000
FIREBASE_PROJECT_ID=playform-prod
```

---

## 🤖 Step 2: AI Agent 시스템 테스트

### 2.1 데모 모드 실행 (API 호출 없음)

```powershell
python main_antigravity.py --demo
```

**예상 출력:**

```
🎬 YouTube Agent 실행...
  ✓ 'AI 자동화' 콘텐츠 생성 중...
  ✓ 'GitHub Actions' 콘텐츠 생성 중...
  ✓ 'SaaS 구축' 콘텐츠 생성 중...
✅ YouTube 콘텐츠 생성 완료

⚙️  SaaS Agent 실행...
  ✓ 기능 설계 중...
  ✓ 코드 생성 및 저장 완료
  ✓ 자동 테스트 실행 중...
  ✓ GitHub에 커밋 중...
✅ SaaS 기능 개발 완료

📢 Marketing Agent 실행...
  ✓ 블로그 포스트 생성 중...
  ✓ 이메일 시퀀스 생성 중...
  ✓ 소셜 미디어 콘텐츠 생성 중...
✅ 마케팅 자동화 완료

📊 일일 성과 요약:
Timestamp: 2024-01-15 09:30:00
Status: ✅ 완료
Tasks:
- 🎬 YouTube: 3개 스크립트 생성
- ⚙️  SaaS: 1개 기능 배포
- 📢 Marketing: 20개 콘텐츠 생성
```

### 2.2 프로덕션 모드 실행 (실제 API 호출)

```powershell
python main_antigravity.py
```

### 2.3 개별 Agent 테스트

```powershell
# Python 콘솔
python

# YouTube Agent
>>> from agents.youtube_agent import run_youtube
>>> run_youtube()

# SaaS Agent
>>> from agents.saas_agent import run_saas
>>> run_saas()

# Marketing Agent
>>> from agents.marketing_agent import run_marketing
>>> run_marketing()
```

---

## ✅ Step 3: 전체 테스트 실행

```powershell
# Pytest 설치
pip install pytest pytest-asyncio

# 전체 에이전트 테스트
pytest test_agents.py -v

# 특정 Agent만 테스트
pytest test_agents.py::test_youtube_agent -v
```

**성공 메시지:**

```
test_agents.py::test_youtube_agent PASSED              [ 33%]
test_agents.py::test_saas_agent PASSED                 [ 66%]
test_agents.py::test_marketing_agent PASSED            [100%]

======================== 3 passed in 0.45s =========================
```

---

## 🔗 Step 4: GitHub 자동 배포 설정

### 4.1 GitHub Repository 생성

```powershell
# GitHub CLI 설치 필요 (https://cli.github.com)
gh repo create playform-ai --public
```

### 4.2 파일 추가 및 커밋

```powershell
git init
git add .
git commit -m "Initial: Playform AI Automation System"
git branch -M main
git remote add origin https://github.com/{YOUR_USERNAME}/playform-ai.git
git push -u origin main
```

### 4.3 GitHub Secrets 설정

**GitHub Repo Settings → Secrets and Variables → Actions**

**추가할 Secrets:**

| Name | Value |
|------|-------|
| OPENAI_API_KEY | sk-... (ChatGPT-4 API Key) |
| FIREBASE_TOKEN | firebase-admin-sdk.json 내용 |
| NOTION_API_KEY | ntn_... (선택사항) |
| YOUTUBE_API_KEY | AIza... (선택사항) |

**설정 방법:**

```powershell
# GitHub CLI로 설정 (선택사항)
gh secret set OPENAI_API_KEY --body "sk-..."
gh secret set FIREBASE_TOKEN --body "@firebase-key.json"
```

### 4.4 자동 실행 확인

**GitHub Actions 모니터링:**

- 📍 Repository → Actions 탭
- ✅ Workflow 상태 확인
- 📊 6시간마다 자동 실행 (`.github/workflows/deploy.yml`)

**수동 실행:**

```powershell
gh workflow run deploy.yml
```

---

## 🎯 Step 5: 로컬 개발 환경 설정 (선택사항)

### 5.1 백엔드 시작

```powershell
cd backend
python -m venv .venv
.\venv\Scripts\activate
pip install -r requirements.txt
python -c "from db import init_db; init_db()"
uvicorn main:app --reload --port 8000
```

### 5.2 프론트엔드 시작

```powershell
cd frontend
npm install
npm run dev
```

### 5.3 MCP Server 시작 (VS Code 통합)

```powershell
python mcp_server.py
```

**MCP Inspector 설정:**
- Transport: STDIO
- Server Script Path: `/full/path/to/mcp_server.py`

---

## 🔍 Step 6: 모니터링 및 디버깅

### 6.1 로그 확인

```powershell
# GitHub Actions 로그
gh run list --repo {owner}/{repo}
gh run view {run-id} --log

# 로컬 실행 로그
tail -f main_antigravity.log  # macOS/Linux
Get-Content main_antigravity.log -Tail 20 -Wait  # Windows
```

### 6.2 성능 문제 해결

| 문제 | 해결책 |
|------|--------|
| OpenAI API 에러 | OPENAI_API_KEY 확인 |
| Firebase 연결 실패 | FIREBASE_TOKEN, FIREBASE_PROJECT_ID 확인 |
| GitHub 배포 실패 | GitHub Secrets 확인 |
| 느린 실행 속도 | --demo 모드에서만 느림 (정상) |

### 6.3 콘솔 출력 커스터마이징

**main_antigravity.py 수정:**

```python
# 상세 로그 활성화
import logging
logging.basicConfig(level=logging.DEBUG)

# 또는 특정 agent만 실행
orchestrator = Orchestrator()
await orchestrator.youtube_agent.run()
```

---

## 📚 추가 리소스

- 📖 [SIMPLIFIED_ARCHITECTURE.md](SIMPLIFIED_ARCHITECTURE.md) - 아키텍처 설명
- 📖 [QUICK_CHOICE_GUIDE.md](QUICK_CHOICE_GUIDE.md) - 버전 선택 가이드
- 📖 [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - 클라우드 배포
- 🎯 [START_HERE.md](START_HERE.md) - 90일 로드맵

---

## 💡 다음 단계

1. ✅ 로컬에서 `main_antigravity.py --demo` 실행
2. ✅ GitHub repo 생성 및 Secrets 설정
3. ✅ `git push` 후 GitHub Actions 자동 실행 확인
4. ✅ 6시간 후 첫 자동 실행 결과 확인
5. ✅ Agent 성과 모니터링 및 최적화

---

## ❓ FAQ

**Q: API Key가 없으면?**
A: `--demo` 모드에서 API 호출 없이 테스트 가능합니다.

**Q: GitHub 초보자인데?**
A: QUICK_CHOICE_GUIDE.md의 초보자 섹션 참고

**Q: 에러 발생하면?**
A: 콘솔 출력을 읽고 .env 파일의 API Key 확인

**Q: 6시간마다 언제 실행되나?**
A: UTC 기준 0:00, 6:00, 12:00, 18:00 (한국시 +9시간)

---

**Let's automate your SaaS! 🚀**
