import streamlit as st
import requests
import time
import uuid

# ================= CONFIG =================

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="MindMate AI",
    page_icon="🧠",
    layout="wide",
)

# ================= CUSTOM CSS =================

st.markdown("""
<style>

.stApp{
    background-color:#0E1117;
    color:white;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

section[data-testid="stSidebar"]{
    background-color:#0B0F14;
    border-right:1px solid #262730;
}

div[data-testid="stChatInput"]{
    background:#1A202C;
    border-radius:20px;
    border:1px solid #2D3748;
}

.main-title{
    font-size:2.5rem;
    font-weight:700;
    background:linear-gradient(90deg,#9F7AEA,#ED64A6);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

</style>
""", unsafe_allow_html=True)

# ================= SESSION =================

if "chats" not in st.session_state:
    st.session_state.chats = {}

if "current_chat" not in st.session_state:
    new_id = str(uuid.uuid4())
    st.session_state.chats[new_id] = []
    st.session_state.current_chat = new_id

# ================= SIDEBAR =================

with st.sidebar:

    st.markdown("## 🧠 MindMate AI")

    if st.button("➕ New Chat", use_container_width=True):
        new_id = str(uuid.uuid4())
        st.session_state.chats[new_id] = []
        st.session_state.current_chat = new_id
        st.rerun()

    st.markdown("---")

    for chat_id in st.session_state.chats.keys():

        title = f"Chat {list(st.session_state.chats.keys()).index(chat_id)+1}"

        if st.button(title, key=chat_id, use_container_width=True):
            st.session_state.current_chat = chat_id
            st.rerun()

# ================= MAIN CHAT =================

chat = st.session_state.chats[st.session_state.current_chat]

if not chat:
    st.markdown('<div class="main-title">MindMate AI</div>', unsafe_allow_html=True)
    st.markdown("### Your personal mental health companion")

# Show messages
for message in chat:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ================= RESPONSE =================

if chat and chat[-1]["role"] == "user":

    with st.chat_message("assistant"):

        placeholder = st.empty()
        full_response = ""

        try:
            with st.spinner("Thinking..."):

                response = requests.post(
                    f"{BASE_URL}/query",
                    json={"question": chat[-1]["content"]},
                )

            if response.status_code == 200:

                answer = response.json().get("answer", "No answer")

                for char in answer:
                    full_response += char
                    placeholder.markdown(full_response + "▌")
                    time.sleep(0.005)

                placeholder.markdown(full_response)

                chat.append({
                    "role":"assistant",
                    "content":full_response
                })

            else:
                error = response.text
                placeholder.error(error)

        except Exception as e:
            placeholder.error(f"Connection failed: {str(e)}")

# ================= INPUT =================

if prompt := st.chat_input("Message MindMate AI..."):
    chat.append({"role":"user","content":prompt})
    st.rerun()
