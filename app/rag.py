### RAG 

from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer
import faiss
import numpy as np
import chardet
import os
from PyPDF2 import PdfReader
import re



# tokenizer for chunking
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

# Chunking function
def chunk_text_by_tokens(text, chunk_size=200, overlap=50, tokenizer=None):
    tokens = tokenizer.encode(text) if tokenizer else text.split()  # simple fallback
    chunks = []
    start = 0
    while start < len(tokens):
        end = min(start + chunk_size, len(tokens))
        chunk_tokens = tokens[start:end] if tokenizer else tokens[start:end]
        chunk_text = tokenizer.decode(chunk_tokens) if tokenizer else " ".join(chunk_tokens)
        chunks.append(chunk_text)
        start += chunk_size - overlap
    return chunks

# PDF loader
def load_pdf_text(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

def clean_text(text):
    text = re.sub(r'Page \d+ of \d+', '', text)  # remove page numbers
    text = re.sub(r'\n+', '\n', text)  # normalize newlines
    return text.strip()

# Load KB documents (from folder)
def load_kb_documents(folder_path="data/kb_docs"):
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    full_path = os.path.join(project_root, folder_path)
    docs = []
    for file_name in os.listdir(full_path):
        file_path = os.path.join(full_path, file_name)
        if file_name.lower().endswith(".pdf"):
            text = load_pdf_text(file_path)
            text = clean_text(text)
            docs.append(text)
        elif file_name.lower().endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                docs.append(clean_text(f.read()))
    return docs

class VectorStore:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.vector_dim = self.model.get_sentence_embedding_dimension()
        self.index = faiss.IndexFlatL2(self.vector_dim)
        self.chunks = []  # store actual text chunks for retrieval

    def add_documents(self, docs):
        for doc in docs:
            doc_chunks = chunk_text_by_tokens(doc, chunk_size=200, overlap=50)
            self.chunks.extend(doc_chunks)
        embeddings = self.model.encode(self.chunks, convert_to_numpy=True)
        self.index.add(embeddings)

    def search(self, query, k=3):
        query_vec = self.model.encode([query], convert_to_numpy=True)
        distances, indices = self.index.search(query_vec, k)
        results = [self.chunks[i] for i in indices[0] if i < len(self.chunks)]
        return results
    
"""def load_pdf_text(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text
    
def load_kb_documents(folder_path="data/kb_docs"):
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    full_path = os.path.join(project_root, folder_path)
    docs = []

    for file in os.listdir(full_path):
        file_path = os.path.join(full_path, file)
        with open(file_path, "rb") as f:
            raw = f.read()
            result = chardet.detect(raw)
            encoding = result['encoding'] or 'utf-8'
            text = raw.decode(encoding, errors='ignore')
            docs.append(text)
    return docs"""
