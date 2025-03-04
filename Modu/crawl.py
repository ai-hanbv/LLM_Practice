import asyncio
import json
from datetime import datetime
from pydantic import BaseModel, Field
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode,BrowserConfig
from crawl4ai.extraction_strategy import LLMExtractionStrategy
import os

class NaverNewsArticle(BaseModel):
    title : str = Field(description="기사 제목")
    published_data : str = Field(description="발행일")
    author : str = Field(description="기자 이름")
    content : str = Field(description="기자 본문")


async def extract_naver_news(naver_news_url:str):
    strategy = LLMExtractionStrategy(
    llmConfig="openai/gpt-4o-mini",
    api_token=os.getenv("OPENAI_API_KEY"),
    schema=NaverNewsArticle.schema(),
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