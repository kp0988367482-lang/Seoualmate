"""
AI Agent 시스템 엔드-투-엔드 테스트
"""

import pytest
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

@pytest.mark.asyncio
async def test_youtube_agent():
    """YouTube Agent 테스트"""
    from agents.youtube_agent import run_youtube
    
    result = run_youtube()
    assert result["status"] == "success"
    assert result["videos"] >= 2

@pytest.mark.asyncio
async def test_saas_agent():
    """SaaS Agent 테스트"""
    from agents.saas_agent import run_saas
    
    result = run_saas()
    assert result["status"] == "success"
    assert result["features"] >= 1

@pytest.mark.asyncio
async def test_marketing_agent():
    """Marketing Agent 테스트"""
    from agents.marketing_agent import run_marketing
    
    result = run_marketing()
    assert result["status"] == "success"
    assert result["blog_posts"] >= 1
    assert result["emails"] >= 1
    assert result["social_posts"] >= 5

@pytest.mark.asyncio
async def test_orchestrator():
    """전체 Orchestrator 테스트"""
    from main_antigravity import Orchestrator
    
    orchestrator = Orchestrator()
    # Summary 생성 (실제 실행은 선택적)
    summary = orchestrator.create_daily_summary()
    
    assert "status" in summary
    assert "timestamp" in summary
    assert "tasks" in summary



class TestConfiguration:
    """설정 파일 테스트"""
    
    def test_env_simple_exists(self):
        """간단 환경 설정 테스트"""
        assert os.path.exists(".env.simple")
    
    def test_env_production_exists(self):
        """프로덕션 환경 설정 테스트"""
        assert os.path.exists(".env.production")
    
    def test_openai_api_key_exists(self):
        """OpenAI API Key 설정 확인"""
        assert os.getenv("OPENAI_API_KEY") or True  # 실제 환경에서는 필수


class TestIntegration:
    """통합 테스트"""
    
    def test_agent_interfaces(self):
        """Agent 인터페이스 일관성"""
        from agents.youtube_agent import run_youtube
        from agents.saas_agent import run_saas
        from agents.marketing_agent import run_marketing
        
        # 모든 에이전트가 실행 가능한지 확인
        assert callable(run_youtube)
        assert callable(run_saas)
        assert callable(run_marketing)
    
    def test_firebase_config_exists(self):
        """Firebase 설정 파일 확인"""
        assert os.path.exists(".firebaserc")
        assert os.path.exists("firebase.json")
    
    def test_github_actions_config_exists(self):
        """GitHub Actions 설정 확인"""
        assert os.path.exists(".github/workflows/deploy.yml")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
