import streamlit as st
from langchain_core.messages import ChatMessage
from dotenv import load_dotenv

load_dotenv()
# streamlit run main.py

# 만약 메세지 라는 키가 없으면 생성
st.title("나는 따라쟁이")
if "messages" not in st.session_state:
# 대화 기록을 저장하긴 위한 용도로 생성
    st.session_state["messages"] = []

def print_messages():
    for chat_message in st.session_state["messages"]:
        st.chat_message(chat_message.role).write(chat_message.content)



def add_message(role, message):
    st.session_state["messages"].append(ChatMessage(role=role,content=message))

print_messages()

# python input이랑 동일, 채팅창 입력 받는 부분
user_input = st.chat_input("Say something")

if user_input:
    st.chat_message("user").write(user_input)
    st.chat_message("assistant").write(user_input)

    add_message("user",user_input)
    add_message("assistant",user_input)


