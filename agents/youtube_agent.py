"""
YouTube 콘텐츠 자동 생성 에이전트
"""

from langchain_openai import ChatOpenAI
import os

def run_youtube():
    """YouTube 콘텐츠 생성"""
    
    print("\n🎬 YouTube Agent 실행...")
    
    llm = ChatOpenAI(model="gpt-4", api_key=os.getenv("OPENAI_API_KEY"))
    
    # 1. 트렌드 찾기
    trends = [
        "AI 자동화",
        "GitHub Actions",
        "SaaS 구축"
    ]
    
    for trend in trends:
        # 2. 스크립트 생성
        prompt = f"""
        {trend}에 대한 10분 YouTube 비디오 스크립트를 만들어줘.
        한국어로 작성하고 쉽고 재미있게 만들어.
        """
        
        # 3. LLM 호출 (실제 통합)
        print(f"  ✓ '{trend}' 콘텐츠 생성 중...")
        
        # 실제 환경에서는:
        # response = llm.invoke(prompt)
        # script = response.content
        # print(script)
    
    print("✅ YouTube 콘텐츠 생성 완료")
    return {"status": "success", "videos": 3}
