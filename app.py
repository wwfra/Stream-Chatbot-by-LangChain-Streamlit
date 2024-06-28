import os
import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

load_dotenv()

# Init the chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.set_page_config(page_title="Chat Bot O.o", page_icon="🚀")
st.title("I'm Chat Bot")

def query(user_input, chat_history):
    template = f"""
    You are a helpful AI assistent, your task is answer the user's question considering the history of conversation:
    
    history of conversation: {chat_history}
    
    user's question: {user_input}
    """
    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatOpenAI(
        api_key=os.getenv("SILI_API_KEY"),
        base_url="https://api.siliconflow.cn/v1",
        model="Qwen/Qwen2-7B-Instruct",
        stream_options={"include_usage": True}
    )

    chain = prompt | llm | StrOutputParser()
    return chain.stream({
        "chat_history": chat_history,
        "user_input": user_input
    })

for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.write(message.content)
    else:
        with st.chat_message("assistant"):
            st.write(message.content)

user_input = st.chat_input("Ask any question to me...")
if user_input is not None and user_input != (" " * len(user_input)):
    st.session_state.chat_history.append(HumanMessage(user_input))
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        ai_output = st.write_stream(query(user_input, st.session_state.chat_history))
    st.session_state.chat_history.append(AIMessage(ai_output))

    if len(st.session_state.chat_history) >= 10:
        st.session_state.chat_history = st.session_state.chat_history[-10:]
else:
    print("It's a Empty Input!")
