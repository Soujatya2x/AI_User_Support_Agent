from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from persona import PersonDetector
from sentiment import SentimentAnalyzer
from rag import VectorStore, load_kb_documents
from generator import ResponseGenerator
from escalation import should_escalate
from fastapi.middleware.cors import CORSMiddleware


app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global objects
vector_store = VectorStore()
persona_detector = PersonDetector()
sentiment_analyzer = SentimentAnalyzer()
generator = ResponseGenerator()

@app.on_event("startup")
def startup_event():
    global vector_store
    vector_store = VectorStore()
    docs = load_kb_documents()  
    vector_store.add_documents(docs)
    print(f"Loaded {len(docs)} documents into vector store.")

class UserMessage(BaseModel):
    message:str
    history: Optional[List[Dict]] = Field(default_factory=list)
    
@app.post("/chat")
def chat(user_input: UserMessage):
    history = user_input.history or []
    conversation_context = ""

    for msg in history[-6:]:  # limiting memory
        conversation_context += f"{msg['role']}: {msg['content']}\n"
    message = user_input.message
    query = message

    # Retrieve top-k chunks from vector store
    results = vector_store.search(query, k=3)
    
   
    """for i, r in enumerate(results):
        print(f"Chunk {i}:\n{r}\n{'-'*40}")"""

    
    persona = persona_detector.detect(message)
    sentiment = sentiment_analyzer.analyze(message)

    # Combine retrieved chunks into single string for context
    retrieved_chunks_text = "\n\n".join(results)  

    
    response = generator.generate_response(
    persona=persona,
    retrieved_chunks=retrieved_chunks_text,
    conversation_history=conversation_context,
    user_message=message
    )
    
    
    escalate = should_escalate(sentiment, 0.8)

    return {
        "persona": persona,
        "sentiment": sentiment,
        "response": response,
        "escalate": escalate
    }