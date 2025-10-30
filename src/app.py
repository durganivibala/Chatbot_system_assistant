import streamlit as st
from rag_engine import generate_response
from memory_manager import ChatMemory

st.set_page_config(page_title="Chatbot", page_icon="🤖")
st.title("🤖 Assistant")

if "memory" not in st.session_state:
    st.session_state.memory = ChatMemory()

if st.button("🧹 Clear Chat Memory"):
    st.session_state.memory.clear()
    st.success("Memory cleared!")

user_query = st.chat_input("Ask something about the PME System...")

if user_query:
    chat_history = st.session_state.memory.get_formatted()
    answer = generate_response(user_query, chat_history)
    st.session_state.memory.add(user_query, answer)

    st.chat_message("user").write(user_query)
    st.chat_message("assistant").write(answer)
