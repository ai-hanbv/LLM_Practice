import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS, InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.messages.chat import ChatMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import load_prompt
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv
import glob
import os


if not os.path.exists(".cache"):
    os.mkdir(".cache")
if not os.path.exists(".cache/embeddings"):
    os.mkdir(".cache/embeddings")
if not os.path.exists(".cache/files"):
    os.mkdir(".cache/files")

vectorstore = None


load_dotenv()

st.title("PDF 기반 QA")

if "messages" not in st.session_state:
# 대화 기록을 저장하긴 위한 용도로 생성
    st.session_state["messages"] = []
if "chain" not in st.session_state:
# 대화 기록을 저장하긴 위한 용도로 생성
    st.session_state["chain"] = None

with st.sidebar:
    select_prompt = "prompts/pdf-rag.yaml"
    clear_btn = st.button(("대화 초기화"))
    uploaded_file = st.file_uploader(("파일 업로드"),type=['pdf'])
    model_name = st.selectbox("모델",["gpt","llama","antropic"])

def add_message(role, message):
    st.session_state["messages"].append(ChatMessage(role=role,content=message))

def print_messages():
    for chat_message in st.session_state["messages"]:
        st.chat_message(chat_message.role).write(chat_message.content)

def creat_chain(prompt_filepath, retriever, model_name = "gpt-4o-mini"):
    prompt = load_prompt(prompt_filepath, encoding="utf-8")
    if model_name.startswith("gpt"):
        llm = ChatOpenAI(model=model_name, temperature=0)
    elif model_name.startswith("llama"):
        llm = OllamaLLM(model="llama3.2:latest")
        print("올라마")
    output_parser = StrOutputParser()
    chain = (
        {"context" : retriever, "question" : RunnablePassthrough()}
        | prompt
        | llm
        | output_parser
    )
    return chain

user_input = st.chat_input("Say something")


warning_msg = st.empty()

# 파일이 업로드 되었을 
@st.cache_resource(show_spinner="업로드한 파일을 처리 중 입니다.")
def embed_file(file):
    file_path = f"./.cache/files/{file.name}"
    loader = PyPDFLoader(file_path)
    document = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size = 1000,chunk_overlap=100)
    splited_document = splitter.split_documents(document)
    vectorstore = FAISS.from_documents(
        documents = splited_document,
        embedding = OpenAIEmbeddings(),
        )
    vectorstore.add_documents(splited_document)
    retriever = vectorstore.as_retriever(
        search_type = "mmr",
        search_kwargs = {"k" : 5}
    )
    return retriever
    


if uploaded_file:
    retriever = embed_file(uploaded_file)
    chain = creat_chain(select_prompt,retriever,model_name=model_name)
    st.session_state["chain"] = chain

if user_input:
    chain = st.session_state["chain"]
    if chain is not None:
        st.chat_message("user").write(user_input)
        # ai_answer = chain.invoke({"question" : user_input})
        response = chain.invoke(user_input)
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
    else:
        warning_msg.error("파일을 업로드 해주세요")