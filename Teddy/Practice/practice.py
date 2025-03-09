import streamlit as st
from langchain_core.messages import ChatMessage
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import load_prompt
from langchain import hub

load_dotenv()
# streamlit run main.py

# 만약 메세지 라는 키가 없으면 생성
st.title("나만의 GPT")

if "messages" not in st.session_state:
# 대화 기록을 저장하긴 위한 용도로 생성
    st.session_state["messages"] = []

with st.sidebar:
    clear_btn = st.button(("대화 초기화"))

    option = st.selectbox(
        "프롬프트를 선택해주세요", ("기본모드", "SNS게시글", "요약"), index=0
    )

def print_messages():
    for chat_message in st.session_state["messages"]:
        st.chat_message(chat_message.role).write(chat_message.content)

# 체인을 생성
def creat_chain(prompt_type):
    # prompt | llm | stroutputParser
    if prompt_type == "기본모드":
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system","당신은 친절한 AI 어시스턴스 입니다."),
                ("user","#Question:\n{question}"),
            ]
        )
    elif prompt_type == "SNS게시글":
        prompt = load_prompt("sns.yaml",encoding="utf-8")
    elif prompt_type == "요약":
        prompt = hub.pull("teddynote/chain-of-density-korean")

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser

    return chain

def add_message(role, message):
    st.session_state["messages"].append(ChatMessage(role=role,content=message))

if clear_btn:
        st.session_state['messages'] = []

# 이전 대화 기록 출력
print_messages()

# python input이랑 동일, 채팅창 입력 받는 부분
user_input = st.chat_input("Say something")

if user_input:
    # 사용자의 입력
    st.chat_message("user").write(user_input)
    # chain 을 생성
    chain = creat_chain(option)
    # ai_answer = chain.invoke({"question" : user_input})
    response = chain.stream({"question" : user_input})
    with st.chat_message("assistant"):
        # 빈공간을 만들어줌
        container = st.empty()
        ai_answer = ""
        for token in response:
            ai_answer += token
            container.markdown(ai_answer)
    # st.chat_message("assistant").write(ai_answer)

    add_message("user",user_input)
    add_message("assistant",ai_answer)


### 나중에 chain-of-density 사용, 요약에서 좋은 성능을 보임