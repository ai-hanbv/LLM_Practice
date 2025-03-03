"""
오늘 배운 목록
1. MassagePlaceHolder
2. oneshot, Fewshot prompt
3. Example Selector (custom & basic)
4. langchain hub
5. streamlit basic

1~4까지 응용해서 간단한 프로젝트 진행
테디노트님의 강의에도 있듯이 회의록 프로그램을 만들어보고 싶어 회의록 프로그램으로 진행
ExampleSelecter도 써야해서 예제는 여러 개로 주겠다.
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain import hub

llm = ChatOpenAI(model = "gpt-4o-mini", temperature = 0.2)
prompt = hub.pull("rlm/rag-prompt")

chain = prompt | llm | StrOutputParser()


# MessagePlaceHolder는 지금 당장 입력이 필요하지 않거나 
print(chain.invoke({"question" : "파이썬에 대해 알려줘", "context" : MessagesPlaceholder("history")}))