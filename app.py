import os
import streamlit as st

from ingest import ingest_pdf
from rag import ask_question

st.set_page_config(
    page_title="PDF Chatbot",
    page_icon="📄",
    layout="wide"
)

st.markdown("""
<style>
.main-title{
    font-size:2.5rem;
    font-weight:700;
    color:#1E3A8A;
}
.subtitle{
    color:#666;
    margin-bottom:20px;
}
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_ingested_file" not in st.session_state:
    st.session_state.last_ingested_file = None

@st.cache_resource(show_spinner=False)
def process_pdf(path):
    ingest_pdf(path)

with st.sidebar:
    st.title("📂 Control Panel")

    with st.form("upload_form"):
        uploaded_file = st.file_uploader(
            "Upload PDF",
            type="pdf"
        )
        upload_btn = st.form_submit_button("Process PDF")

    if upload_btn and uploaded_file:
        os.makedirs("data", exist_ok=True)
        file_path = os.path.join("data", uploaded_file.name)

        if st.session_state.last_ingested_file != uploaded_file.name:
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            with st.spinner("Reading PDF and creating embeddings..."):
                process_pdf(file_path)

            st.session_state.last_ingested_file = uploaded_file.name
            st.session_state.messages = []
            st.success("✅ PDF processed successfully.")
        else:
            st.info("This PDF has already been processed.")

    st.divider()

    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.markdown(
    '<div class="main-title">📄 PDF Chatbot</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Ask questions about your uploaded PDF.</div>',
    unsafe_allow_html=True
)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

question = st.chat_input("Ask a question...")

if question:
    if st.session_state.last_ingested_file is None:
        st.warning("Please upload a PDF first.")
        st.stop()

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                answer = ask_question(question)
            except Exception as e:
                answer = f"❌ Error: {e}"

        st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )