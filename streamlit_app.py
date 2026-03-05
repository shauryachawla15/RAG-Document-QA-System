import streamlit as st
import PyPDF2
import docx
import chromadb
import re
from sentence_transformers import SentenceTransformer


# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Document Chat RAG", layout="wide")
st.title("📄 Document Chatbot (RAG Powered)")
st.write("Upload a PDF or DOCX and ask questions about it.")


# ---------------- LOAD EMBEDDING MODEL ----------------
@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_model()


# ---------------- INIT CHROMA ----------------
@st.cache_resource
def init_chroma():
    client = chromadb.Client()
    try:
        client.delete_collection("doc_chat")
    except:
        pass
    return client.create_collection("doc_chat")

collection = init_chroma()


# ---------------- TEXT CLEANING ----------------
def clean_text(text):
    text = re.sub(r'\n+', ' ', text)          # remove extra line breaks
    text = re.sub(r'\s+', ' ', text)          # normalize spaces
    return text.strip()


# ---------------- TEXT EXTRACTION ----------------
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + " "
    return text


def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + " "
    return text


# ---------------- SMART CHUNKING ----------------
def chunk_text(text, chunk_size=400):
    sentences = text.split(". ")
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) < chunk_size:
            current_chunk += sentence + ". "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader("Upload PDF or DOCX", type=["pdf", "docx"])

if uploaded_file:

    # Extract text
    if uploaded_file.type == "application/pdf":
        document_text = extract_text_from_pdf(uploaded_file)
    else:
        document_text = extract_text_from_docx(uploaded_file)

    document_text = clean_text(document_text)

    if len(document_text) < 50:
        st.error("Could not extract meaningful text from document.")
        st.stop()

    st.success("Document processed successfully!")

    # Chunking
    chunks = chunk_text(document_text)

    # Remove old embeddings
    existing = collection.get()
    if existing["ids"]:
        collection.delete(ids=existing["ids"])

    # Store embeddings
    embeddings = model.encode(chunks)

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=[f"id_{i}" for i in range(len(chunks))]
    )

    st.session_state["document_ready"] = True


# ---------------- CHAT STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []


# ---------------- CHAT INTERFACE ----------------
if st.session_state.get("document_ready"):

    st.subheader("💬 Chat with your document")

    # Show chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    if prompt := st.chat_input("Ask a question about the document..."):

        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        # Embed question
        query_embedding = model.encode([prompt])

        results = collection.query(
            query_embeddings=query_embedding,
            n_results=2,
            include=["documents", "distances"]
        )

        retrieved_chunks = []

        # Similarity threshold filtering
        for doc, distance in zip(results["documents"][0], results["distances"][0]):
            if distance < 1.0:   # lower = more similar
                retrieved_chunks.append(doc)

        if not retrieved_chunks:
            response = "I could not find relevant information in the document."
        else:
            context = " ".join(retrieved_chunks)

            response = f"""
###  Answer:

{context}
"""

        st.session_state.messages.append({"role": "assistant", "content": response})

        with st.chat_message("assistant"):
            st.markdown(response)

else:
    st.info("Upload a document to start chatting.")