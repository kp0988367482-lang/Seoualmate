"""
마스터 실행 스크립트 - 최상위 엔트리포인트
사용자가 원하는 작업을 선택하여 실행
"""

import sys
import os
import subprocess
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


def print_menu():
    """메인 메뉴 출력"""
    print("\n" + "="*60)
    print("🚀 Playform AI Automation - 마스터 제어판")
    print("="*60)
    print("\n[0] 배포 체크리스트 실행")
    print("[1] GitHub 저장소 설정")
    print("[2] 데모 모드 (YouTube + SaaS + Marketing)")
    print("[3] 프로덕션 모드 (실제 API 호출)")
    print("[4] 개별 에이전트 실행")
    print("    [4-1] YouTube Agent만")
    print("    [4-2] SaaS Agent만")
    print("    [4-3] Marketing Agent만")
    print("[5] 전체 테스트 (pytest)")
    print("[6] 설정 확인")
    print("[7] 도움말")
    print("[Q] 종료")
    print("-"*60)


def run_checklist():
    """배포 체크리스트 실행"""
    print("\n📋 배포 체크리스트 실행 중...\n")
    subprocess.run([sys.executable, "deployment_checklist.py"])


def setup_github():
    """GitHub 저장소 설정"""
    print("\n🔗 GitHub 저장소 설정 중...\n")
    subprocess.run([sys.executable, "setup_github.py"])


def run_demo():
    """데모 모드 실행"""
    print("\n🎬 데모 모드 (YouTube + SaaS + Marketing) 실행 중...\n")
    subprocess.run([sys.executable, "main_antigravity.py", "--demo"])


def run_production():
    """프로덕션 모드 실행"""
    print("\n⚙️  프로덕션 모드 (실제 API 호출) 실행 중...\n")
    
    # OpenAI API Key 확인
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ 오류: OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.")
        print("💡 팁: .env 파일에 OPENAI_API_KEY를 추가하세요")
        return
    
    subprocess.run([sys.executable, "main_antigravity.py"])


def run_agent(agent_name):
    """개별 에이전트 실행"""
    agents = {
        "youtube": ("agents.youtube_agent", "YouTube Agent"),
        "saas": ("agents.saas_agent", "SaaS Agent"),
        "marketing": ("agents.marketing_agent", "Marketing Agent")
    }
    
    if agent_name in agents:
        module, description = agents[agent_name]
        print(f"\n🎯 {description} 실행 중...\n")
        
        try:
            # Python에서 동적으로 모듈 import 및 실행
            exec(f"from {module} import run_{agent_name}")
            exec(f"run_{agent_name}()")
        except Exception as e:
            print(f"❌ 오류: {e}")
    else:
        print(f"❌ 알 수 없는 에이전트: {agent_name}")


def run_tests():
    """전체 테스트 실행"""
    print("\n🧪 전체 테스트 (pytest) 실행 중...\n")
    
    # pytest 설치 확인
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "test_agents.py", "-v"],
        cwd=Path(__file__).parent
    )
    
    if result.returncode != 0:
        print("\n💡 pytest 설치가 필요합니다:")
        print("   pip install pytest pytest-asyncio")


def show_config():
    """설정 확인"""
    print("\n⚙️  현재 설정:")
    print("-"*60)
    
    # .env 파일 확인
    if Path(".env").exists():
        print("✅ .env 파일 존재")
        with open(".env") as f:
            for line in f:
                if not line.startswith("#") and "=" in line:
                    key, value = line.strip().split("=", 1)
                    masked_value = value[:10] + "***" if len(value) > 10 else value
                    print(f"   {key}={masked_value}")
    else:
        print("❌ .env 파일 없음")
    
    print("\n✅ 특정 Python 패키지:")
    packages = ["langchain", "openai", "fastapi", "pytest"]
    for package in packages:
        try:
            __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} (pip install {package})")
    
    print("\n📁 프로젝트 구조:")
    structure = [
        "main_antigravity.py",
        "agents/",
        ".github/workflows/deploy.yml",
        ".firebaserc",
        "firebase.json"
    ]
    
    for item in structure:
        exists = "✅" if Path(item).exists() else "❌"
        print(f"   {exists} {item}")


def show_help():
    """도움말 표시"""
    help_text = """
📖 Playform AI Automation 도움말
="*60)

🚀 빠른 시작:
1. python master.py → [2] 데모 모드 실행
2. python master.py → [0] 배포 체크리스트 확인
3. python master.py → [1] GitHub 저장소 설정

📚 각 모드 설명:

[0] 배포 체크리스트
   - 모든 설정 파일 확인
   - 환경 변수 검증
   - Python 패키지 설치 상태 확인
   - 배포 준비도 평가

[1] GitHub 저장소 설정
   - Git 저장소 초기화
   - GitHub로 푸시
   - 자동 배포 설정
   - GitHub Secrets 구성

[2] 데모 모드
   - API 호출 없음
   - 리소스 사용 최소
   - 시스템 테스트용
   권장: 처음 시작할 때

[3] 프로덕션 모드
   - 실제 API 호출
   - OpenAI GPT-4 사용
   - 실제 콘텐츠 생성
   준비: OPENAI_API_KEY 필수

[4] 개별 에이전트 실행
   - YouTube Agent: 콘텐츠 생성
   - SaaS Agent: 기능 개발
   - Marketing Agent: 마케팅 자동화

[5] 전체 테스트
   - pytest로 모든 에이전트 테스트
   - 설정 파일 검증
   - 통합 테스트

[6] 설정 확인
   - .env 파일 확인
   - 패키지 설치 상태
   - 프로젝트 구조

🔧 트러블슈팅:

Q: API 에러가 나요
A: OPENAI_API_KEY 확인 → .env 파일에 유효한 키 입력

Q: 패키지 설치 오류
A: pip install langchain langchain-openai python-dotenv

Q: GitHub Actions 실행 안 됨
A: [1]로 GitHub 저장소 설정 → Secrets 추가

Q: 느린 속도?
A: [2] 데모 모드는 느릴 수 있음 (정상)

📞 추가 정보:
- GETTING_STARTED.md - 초보자 가이드
- README.md - 프로젝트 개요
- SIMPLIFIED_ARCHITECTURE.md - 아키텍처 설명
"""
    
    print(help_text)


def main():
    """메인 루프"""
    while True:
        print_menu()
        choice = input("선택: ").strip().upper()
        
        if choice == "0":
            run_checklist()
        elif choice == "1":
            setup_github()
        elif choice == "2":
            run_demo()
        elif choice == "3":
            run_production()
        elif choice == "4-1":
            run_agent("youtube")
        elif choice == "4-2":
            run_agent("saas")
        elif choice == "4-3":
            run_agent("marketing")
        elif choice == "5":
            run_tests()
        elif choice == "6":
            show_config()
        elif choice == "7":
            show_help()
        elif choice == "Q":
            print("\n👋 종료합니다!")
            break
        else:
            print("\n❌ 올바른 선택이 아닙니다. 다시 시도해주세요.")
        
        input("\n[Enter 를 눌러 계속...]")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 중단되었습니다!")
        sys.exit(0)
