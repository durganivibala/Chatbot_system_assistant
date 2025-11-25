import streamlit as st
from rag_engine import generate_response
from memory_manager import ChatMemory

st.set_page_config(page_title="Product Support Chatbot", page_icon="🤖")
st.title("🤖 ChatlocalAI [Offline chatbot]")


if "memory" not in st.session_state:
    st.session_state.memory = ChatMemory()


if st.button("🧹 Clear Chat Memory"):
    st.session_state.memory.clear()
    st.success("Memory cleared!")



chat_records = list(st.session_state.memory.history)  # deque → list

for turn in chat_records:
    st.chat_message("user").write(turn["user"])
    st.chat_message("assistant").write(turn["bot"])


user_query = st.chat_input("Ask something about the PME System...")

if user_query:
    # Immediately show user's message
    st.chat_message("user").write(user_query)

    with st.spinner("Generating response..."):
        # Retrieve relevant past memory for context
        relevant_history = st.session_state.memory.get_relevant(
            user_query, top_k=3, threshold=0.55
        )
        chat_history = st.session_state.memory.format_for_prompt(relevant_history)

        # RAG response generation
        answer = generate_response(user_query, chat_history)

        # Store in memory (with embeddings)
        st.session_state.memory.add(user_query, answer)

    # Show assistant response
    st.chat_message("assistant").write(answer)
