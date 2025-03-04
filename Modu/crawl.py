import asyncio
from crawl4ai import AsyncWebCrawler
import nest_asyncio

async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url = "https://n.news.naver.com/mnews/article/001/0015245353?rc=N&ntype=RANKING"
        )
        print(result)

if __name__=="__main__":
    asyncio.run(main())