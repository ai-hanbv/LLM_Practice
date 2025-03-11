# AI/LLM 강의를 들으면서 응용해보기

#### 2025.03.04

1. crawl4ai (웹크롤링 라이브러리)

```
peotry add crawl4ai
crawl4ai-setup
# 만약 문제가 있을 시
crawl4ai-doctor
```

```python
# Docs Code
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, LlmConfig
# 오류 발생, 없는 코드
# 수정
from crawl4ai.async_configs import LlmConfig
# 오류 해결 및 정상 실행
```

해당코드는 craw4ai의 문서를 참고하여 작성하였으나 동작이 되지 않아 개선한 코드이다.
버전 0.5.0 기준으로 사용하였으나 계속 업데이트 되는 중이라 변경 가능성이 매우 높다.
오픈소스로 기여하고 싶었으나 개발자는 원하는 방향이 아닌 것으로 예상된다.

#### 2025.03.06

##### Text2SQL

[Text2SQL 참고 링크]("https://www.sktenterprise.com/bizInsight/blogDetail/skt/8161“)

- LLM을 이용하여 텍스트를 SQL 쿼리문으로 바꿔주는 방법이다. 현업에 있는 사람들은 데이터가 필요할 경우 데이터 전문가에게 부탁하거나 혹은 하드코딩 되어 있는 쿼리문을 버튼 등의 방식으로 이용하여 데이터를 받아오는 방식으로 이용하고 있다. 또한 현업 및 데이터 전문가들 사이에서는 용어가 달라 소통의 어려움이 존재한다. 그러나 Text2SQL 방식을 이용하게 된다면
현업자는 필요할 때 원하는 데이터를 받아올 수 있고 데이터 전문가는 더욱 효율적은 방식으로 SQL 저장, 호출, 관리하며 작업의 효율성 또한 높일 수 있다.

##### Spider dataset을 이용한 정확도 평가 지표(Accuracy metric)

1. EX(Excusion accuracy)
- EX 방식은 LLM이 생성한 쿼리와 정답인 쿼리를 비교하여 정확도를 측정하는 방식이다.
2. EM(Exact-set Match accuray)
- EM 방식은 모든 모델이 생성한 쿼리와 정답의 구문까지 비교해서 정확도를 측정하는 방식이다.

##### 대표적인 쿼리 추출 방식
1. Inference only Approach
- zero-shot, Few-shot 등 LLM이 프롬프트를 통해 추론하는 방식을 의미한다.
2. Fine-Tuning Apporach
- 파인튜닝은 모델을 원하는 방향으로 학습시킬 수 있는 방법 중 하나로 질문 쿼리, 정답 쿼리를 전달 후 학습시키는 방식이다.

#### 2025.03.06 ~

##### 알게된 함수
1. pd.to_numeric()

```python
import pandas as pd
data = ['1','2', 'A']

data = [pd.to_numeric(x) for x in data]

#1번째 실행
'1' -> 1
#2번쨰 실행
'2' -> 2
#3번째 실행 - 에러 발생
'A' -> error
# int, float로 변환 가능한 변수만 처리 해준다.
```
2. Typing 라이브러리, Langgraph, SQL QA Chain
3. 고유명사 DB