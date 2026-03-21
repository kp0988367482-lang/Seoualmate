#!/usr/bin/env python3
"""
🎯 AI Agent 시스템 배포 체크리스트
GitHub + Antigravity 통합 검증
"""

import os
import json
import subprocess
from pathlib import Path
from datetime import datetime

class DeploymentChecklist:
    def __init__(self):
        self.checks = []
        self.timestamp = datetime.now().isoformat()
    
    def check_file_exists(self, filepath, description):
        """파일 존재 여부 확인"""
        exists = Path(filepath).exists()
        status = "✅" if exists else "❌"
        print(f"{status} {description}")
        self.checks.append({
            "description": description,
            "status": "pass" if exists else "fail",
            "type": "file"
        })
        return exists
    
    def check_env_var(self, var_name, description):
        """환경 변수 확인"""
        exists = var_name in os.environ
        status = "✅" if exists else "❌"
        value = "***" if exists and len(os.getenv(var_name, "")) > 5 else os.getenv(var_name, "")
        print(f"{status} {description}: {value}")
        self.checks.append({
            "description": description,
            "status": "pass" if exists else "fail",
            "type": "env"
        })
        return exists
    
    def check_python_package(self, package, description):
        """Python 패키지 확인"""
        try:
            __import__(package)
            print(f"✅ {description}")
            self.checks.append({
                "description": description,
                "status": "pass",
                "type": "package"
            })
            return True
        except ImportError:
            print(f"❌ {description}")
            self.checks.append({
                "description": description,
                "status": "fail",
                "type": "package"
            })
            return False
    
    def run_full_check(self):
        """전체 체크 실행"""
        print("\n" + "="*60)
        print("🎯 Playform AI Agent 배포 체크리스트")
        print("="*60 + "\n")
        
        # 1️⃣  파일 구조 확인
        print("\n📁 1단계: 파일 구조 확인")
        print("-" * 40)
        self.check_file_exists(".env", "환경 설정 파일")
        self.check_file_exists("main_antigravity.py", "마스터 오케스트레이터")
        self.check_file_exists("agents/youtube_agent.py", "YouTube Agent")
        self.check_file_exists("agents/saas_agent.py", "SaaS Agent")
        self.check_file_exists("agents/marketing_agent.py", "Marketing Agent")
        self.check_file_exists(".github/workflows/deploy.yml", "GitHub Actions 워크플로우")
        self.check_file_exists(".firebaserc", "Firebase 설정")
        self.check_file_exists("firebase.json", "Firebase JSON 설정")
        self.check_file_exists("firestore.rules", "Firestore 보안 규칙")
        
        # 2️⃣  환경 변수 확인
        print("\n🔑 2단계: 환경 변수 확인")
        print("-" * 40)
        self.check_env_var("OPENAI_API_KEY", "OpenAI API Key")
        self.check_env_var("FIREBASE_PROJECT_ID", "Firebase Project ID")
        self.check_env_var("PLAYFORM_API", "Playform API 주소")
        
        # 3️⃣  Python 패키지 확인
        print("\n📦 3단계: Python 패키지 확인")
        print("-" * 40)
        self.check_python_package("langchain", "LangChain")
        self.check_python_package("langchain_openai", "LangChain OpenAI")
        self.check_python_package("dotenv", "Python-dotenv")
        self.check_python_package("pytest", "Pytest")
        self.check_python_package("fastapi", "FastAPI")
        
        # 4️⃣  GitHub 연동 확인
        print("\n🔗 4단계: GitHub 연동 확인")
        print("-" * 40)
        try:
            result = subprocess.run(
                ["git", "remote", "-v"],
                capture_output=True,
                text=True
            )
            if "origin" in result.stdout:
                print("✅ GitHub Repository 연결됨")
                print(f"   {result.stdout.split()[1]}")
                self.checks.append({"description": "GitHub 연동", "status": "pass", "type": "git"})
            else:
                print("❌ GitHub Repository 미연결")
                self.checks.append({"description": "GitHub 연동", "status": "fail", "type": "git"})
        except Exception as e:
            print(f"⚠️  Git 확인 불가: {e}")
        
        # 5️⃣  Firebase 연동 확인
        print("\n🔥 5단계: Firebase 연동 확인")
        print("-" * 40)
        firebase_rc = Path(".firebaserc")
        if firebase_rc.exists():
            with open(firebase_rc) as f:
                config = json.load(f)
                project = config.get("projects", {}).get("default")
                print(f"✅ Firebase 프로젝트: {project}")
                self.checks.append({
                    "description": f"Firebase 프로젝트 설정: {project}",
                    "status": "pass",
                    "type": "firebase"
                })
        else:
            print("❌ Firebase 설정 파일 없음")
            self.checks.append({
                "description": "Firebase 설정",
                "status": "fail",
                "type": "firebase"
            })
        
        # 📊 최종 요약
        print("\n" + "="*60)
        print("📊 체크리스트 결과 요약")
        print("="*60)
        
        passed = sum(1 for c in self.checks if c["status"] == "pass")
        failed = sum(1 for c in self.checks if c["status"] == "fail")
        total = len(self.checks)
        
        print(f"\n✅ 성공: {passed}/{total}")
        print(f"❌ 실패: {failed}/{total}")
        print(f"📈 성공률: {passed*100//total}%\n")
        
        if failed == 0:
            print("🎉 모든 확인 완료! 배포 준비 완료!\n")
            self.print_next_steps()
        else:
            print("⚠️  몇 가지 문제가 있습니다. 위의 ❌ 항목을 확인해주세요.\n")
            self.print_fix_steps()
        
        self.save_report()
        return failed == 0
    
    def print_next_steps(self):
        """다음 단계 출력"""
        print("🚀 다음 단계:")
        print("-" * 40)
        print("1. python main_antigravity.py --demo")
        print("   (데모 모드에서 모든 에이전트 실행)")
        print("")
        print("2. git push origin main")
        print("   (변경사항을 GitHub에 푸시)")
        print("")
        print("3. GitHub Actions 모니터링")
        print("   (https://github.com/{username}/playform-ai/actions)")
        print("")
        print("4. 6시간마다 자동 실행 확인")
        print("   (일일 성과 리포트 받기)")
    
    def print_fix_steps(self):
        """수정 단계 출력"""
        print("🔧 수정 단계:")
        print("-" * 40)
        
        failed_checks = [c for c in self.checks if c["status"] == "fail"]
        
        for check in failed_checks:
            if check["type"] == "file":
                print(f"파일 생성 필요: {check['description']}")
            elif check["type"] == "env":
                print(f"환경 변수 설정 필요: {check['description']}")
            elif check["type"] == "package":
                print(f"패키지 설치 필요: pip install {check['description'].lower()}")
            elif check["type"] == "git":
                print(f"GitHub 연동: gh repo create 또는 git remote add origin")
            elif check["type"] == "firebase":
                print(f"Firebase 설정: https://console.firebase.google.com")
    
    def save_report(self):
        """체크리스트 리포트 저장"""
        report = {
            "timestamp": self.timestamp,
            "total_checks": len(self.checks),
            "passed": sum(1 for c in self.checks if c["status"] == "pass"),
            "failed": sum(1 for c in self.checks if c["status"] == "fail"),
            "checks": self.checks
        }
        
        report_file = f"deployment_report_{self.timestamp.split('T')[0]}.json"
        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)
        
        print(f"📝 리포트 저장: {report_file}")


if __name__ == "__main__":
    checklist = DeploymentChecklist()
    success = checklist.run_full_check()
    exit(0 if success else 1)
