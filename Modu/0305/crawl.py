import asyncio
import json
from datetime import datetime
from pydantic import BaseModel, Field
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode,BrowserConfig
from crawl4ai.async_configs import LlmConfig
from crawl4ai.extraction_strategy import LLMExtractionStrategy
import os

class NaverNewsArticle(BaseModel):
    title : str = Field(description="기사 제목")
    published_data : str = Field(description="발행일")
    author : str = Field(description="기자 이름")
    content : str = Field(description="기자 본문")


async def extract_naver_news(naver_news_url:str):
    # 문서와 똑같이 작성하였지만 오류가 발생하였고 없는 모듈이라고 하였다. 라이브러리를 뒤져서 맞는 모듈을 찾아냈다.
    strategy = LLMExtractionStrategy(
    llmConfig=LlmConfig(
        provider="openai/gpt-4o-mini",
        api_token=os.getenv("OPENAI_API_KEY")
        ),
    schema=NaverNewsArticle.model_json_schema(),
    extraction_type="schema",
    instruction="""
    네이버 뉴스 기사에서 다음 정보를 추출하세요:
    - title : 기사 제목
    - published_data : 발행일시
    - author : 기자 이름
    - content : 기사 본문
    """
    )
    
    config = CrawlerRunConfig(
        exclude_external_links=True,
        extraction_strategy=strategy,
        cache_mode=CacheMode.BYPASS,
    )
    browser_cfg = BrowserConfig(headless=True)

    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        result = await crawler.arun(
            url=naver_news_url,
            config=config,
        )
        article = json.loads(result.extracted_content)
        return article
    

naver_url = "https://n.news.naver.com/mnews/article/001/0015245353?rc=N&ntype=RANKING"

article = asyncio.run(extract_naver_news(naver_url))
print(article)


#Result
"""
[INIT].... → Crawl4AI 0.5.0
[FETCH]... ↓ https://n.news.naver.com/mnews/article/001/0015245... | Status: True | Time: 0.82s
[SCRAPE].. ◆ https://n.news.naver.com/mnews/article/001/0015245... | Time: 0.271s
[EXTRACT]. ■ Completed for https://n.news.naver.com/mnews/article/001/0015245... | Time: 27.991495199999918s
[COMPLETE] ● https://n.news.naver.com/mnews/article/001/0015245... | Status: True | Total: 29.09s
[{'title': '탄핵 인용 예상 많아 “국회 탄핵소추 사유 변경 문제 있다” 의견도 2명은 전망 유보... 
“위헌·위법성 논란 여지”', 'published_data': '', 'author': '', 'content': '윤석열 대통령에 대한  
헌법재판소의 탄핵심판 선고가 코앞으로 다가온 가운데, 10명 인터뷰…탄핵 인용 예상 많아 “국회 탄핵소추 사유 변경 문제 있다” 
의견도 2명은 전망 유보... “위헌·위법성 논란 여지”', 'error': False}, 
{'title': "선관위 '채용비리' 대국민사과…특혜채용 10명 여전히 정상근무(종합)", 'published_data': '2025.03.04. 오후 7:22', 'author': '최평천 기자', 
'content': '중앙선거관리위원회가 4일 채용 비리 문제와 관련해 대국민 사과를 했지만, \'특혜 채용\' 혜택을 받은 것으로 확인된 당사자 10명은 여전히 정상 근무 중인 것으로 나타났다. 
선관위 관계자는 연합뉴스와 통화에서 "감사원 감사에서 적발 된 위법·부당 채용 관련자 10명이 정상적인 업무를 하고 있다"고 밝혔다. 선관위는 2023년 5월 고위직 간부 자녀 채용 비리가 불거지자 
경력직 채용 실태에 대한 자체 감사를 진행했고, 감사원 감사도 받 았다. 선관위는 자체 감사에서 특혜 채용 의혹이 확인된 박찬진 전 사무총장과 송봉섭 전 사무차장,  신우용 전 제주 상임위원 등 
고위직 간부 자녀 5명에 대해서만 2023년 7월 업무 배제 조치를 했다. 그러나 지난해 1월 총선을 앞두고 이들을 업무에 복귀시켰다. 선관위 관계자는 "감사원이 채용 비리와  관련해 징계를 요구한 
직원들은 채용 과정에 관여한 간부 또는 인사 담당자들이고, 채용된 당사자에  대해서는 징계를 요구하지 않았다"며 "징계 요구가 없었기 때문에 정상적으로 일을 하는 것"이라고 설명했다. 
이 관계자는 "국민의 눈높이를 고려해 채용된 당사자들에 대해서도 후속 조치를 검토하겠다" 고 덧붙였다. 선관위는 감사원에서 징계와 주의 처분을 요구한 27명에 대한 절차를 진행 중이다. 선관위는 채용 비리 문제를 둘러싸고 
비판 여론이 높아지자 이날 "일부 고위직 자녀 경력 채용의 문제와  복무기강 해이 등에 대해 국민 여러분에게 다시 한번 깊이 사과드린다"며 국회에서 통제 방안 마련을 위한 논의가 진행될 경우 적극 참여하겠다고 밝혔다. 
아울러 외부 인사가 주도하는 한시적 특별위원회 구성 등의 자체 개혁안도 적극적으로 검토할 방침이다. 선관위는 보도자료에서 "헌법재판소 결정에  따라 선관위가 행정부 소속인 감사원의 직무감찰 대상에서 제외되지만, 
국민의 대표인 국회에 의한 국정조사와 국정감사 등의 외부적 통제까지 배제되는 것은 아니다"라고 설명했다. 오는 17일 열리는 선 관위원 전체회의에서 자정·개혁 방안이 마련될 가능성도 나온다. 
선관위가 사실상 국회가 마련하는 통제 방안을 수용할 수 있다는 의사를 밝힘에 따라 국회 논의에 속도가 붙을 수 있을지 주목된다. 국민 의힘 권성동 원내대표는 국회에서 기자들과 만나 선관위의 대국민 사과에 대해 
"만시지탄이지만 국민 을 의식하고 본인들에 대한 비판을 의식하고 있다는 것을 보여준 것은 다행"이라고 평가했다. 이어 " 원래 기관이 자정 능력을 상실하면 외부에서 제3의 기관이 외과적 수술을 하는 것이 조직의 
건강성 회복을 위해 정말 필요하다"며 "그런 차원에서 국회가 특별감사관법을 제정해 문제점을 들여다보고, 개 선방안을 찾는 것이 선관위와 국민 모두에게 이익이 된다"고 말했다. 앞서 국민의힘은 선관위의 부패 를 개혁하겠다며 
5대 선결 과제 추진을 발표했다. 주제별로 ▲ 외부 감시·견제 강화를 위한 특별감사관 도입 ▲ 선관위 사무총장 대상 국회 인사청문회 도입 ▲ 법관의 선관위원장 겸임 금지 ▲ 시도선관위 대상 행정안전위원회 국정감사 도입 ▲ 
지방선관위 상임위원 임명 자격을 외부 인사로 확대하기 위한 선 관위법 시행규칙 개정 등이다. 더불어민주당 조승래 수석대변인은 서면 브리핑에서 "선관위가 신속하 고 엄정하게 채용 비리를 조사해 엄단하는 것은 물론이고 
앞으로 뼈를 깎는 노력으로 국민 신뢰를 회 복하기를 바란다"며 "국민의 실망을 깊이 숙고해 다시는 조직 내에 비리가 들어설 수 없도록 하기를  바란다"고 말했다. 조 수석대변인은 "감사원에 선관위 직무감사 권한이 없다는 
헌법재판소 결정을 존 중해 국회 차원에서 선관위를 감시·견제해 국민 신뢰를 회복할 수 있도록 실효성 있는 대책을 마련하 겠다"고 말했다.', 'error': False}]
"""