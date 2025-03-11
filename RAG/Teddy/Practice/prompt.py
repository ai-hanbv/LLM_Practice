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


"""
오늘 배운 목록
1. MassagePlaceHolder
2. oneshot, Fewshot prompt
3. Example Selector (custom & basic)
4. langchain hub

1~4까지 응용해서 간단한 프로젝트 진행
테디노트님의 강의에도 있듯이 회의록 프로그램을 만들어보고 싶어 회의록 프로그램으로 진행
ExampleSelecter도 써야해서 예제는 여러 개로 주겠다.
"""

from langchain_core.prompts import FewShotPromptTemplate, MessagesPlaceholder, PromptTemplate, ChatPromptTemplate,FewShotChatMessagePromptTemplate
from langchain_core.example_selectors import (
    SemanticSimilarityExampleSelector,
    MaxMarginalRelevanceExampleSelector,
    BaseExampleSelector,
)
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma


from  dotenv  import load_dotenv

load_dotenv()

fewshot_example = [
    {
        "instruction" : "당신은 회의록 작성 전문가 입니다. 주어진 정보를 바탕으로 회의록을 작성해주세요",
        "input" :"""
            금일 회의 주제는 국책과제 신청 입니다. 주관 기간은 과학기술정보통신부로
            해당 과제명은 AI 서버 구축 이고 김박씨는 소장으로써 업무 지시 및 관련 소개서를 쓰고
            박민석씨는 AI 서버 구축에 대한 금액 및 자료를 수집, 김인식씨는 정보 수집 및 정리의 임무를 맡았다.
            """,
        "answer" : """
            1. 회의일자 : 2025/03/01
            2. 참석인원 : 김박, 박민석, 김인식
            3. 회의 주제
                - 주관 기간 : 과학기술정보통신부
                - 과제명 : AI 서버 구축
            4. 역활
                - 김박 : 업무 지시 및 소개서 작성
                - 박민석 : AI 서버 구축에 대한 금액 및 자료 수집
                - 김민석 : 정보 수집 및 정리 입무
            5. 일정
                - 3.1 ~ 3.5 서버 구축 정리 후 보고
                - 3.5 ~ 3.10 소개서 작성
        """
    },
    {
        "instruction" : "당신은 소설가 입니다. 주제를 듣고 단편 소설을 작성하세요",
        "input" : "용과 용사가 싸워서 용사가 세상을 구하는 소설을 만들어줘",
        "answer" : """
            10세기 말 혜성처럼 등장한 용사는 미민 이라는 동네에서 태어났습니다. 그는 평소 아이들과 다르게 영민하였으며 무예가 뛰어나
            신동이라고 불렸습니다. 아버지와 같이 나무를 배러가는 도중 용을 만났고 치열한 전투 끝에 무찔렀습니다. 그는 영웅이 되었고
            세상을 구했습니다.
        """
    },
    {
        "instruction" : "당신은 수학자 입니다. 주제를 듣고 수학문제를 풀어주세요",
        "input" : "cos60 + tan0 는 머야",
        "answer" : """
            cos 45 = 1/2,
            tan 0 = =0 이므로
            1/2 + 0 = 1/2
            즉 정답은 1/2 입니다.
        """
    }
]


example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{instruction}:\n{input}"),
        ("ai", "{answer}"),
    ]
)

embedding_model = OpenAIEmbeddings()
chroma = Chroma("example",embedding_model)
example_selector = MaxMarginalRelevanceExampleSelector.from_examples(
    fewshot_example,
    embeddings=embedding_model,
    vectorstore_cls=Chroma,
    k=1
)

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature = 0.2
)

# default 사용
few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_selector=example_selector,
    example_prompt=example_prompt,
)
final_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant.",
        ),
        few_shot_prompt,
        ("human", "{instruction}\n{input}"),
    ]
)
chain = final_prompt | llm

question = {
    "instruction": "회의록",
    "input": "2023년 12월 26일, ABC 기술 회사의 제품 개발 팀은 새로운 모바일 애플리케이션 프로젝트에 대한 주간 진행 상황 회의를 가졌다. 이 회의에는 프로젝트 매니저인 최현수, 주요 개발자인 황지연, UI/UX 디자이너인 김태영이 참석했다. 회의의 주요 목적은 프로젝트의 현재 진행 상황을 검토하고, 다가오는 마일스톤에 대한 계획을 수립하는 것이었다. 각 팀원은 자신의 작업 영역에 대한 업데이트를 제공했고, 팀은 다음 주까지의 목표를 설정했다."
}

print(chain.invoke(question).content)

