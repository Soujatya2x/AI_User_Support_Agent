from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

class ResponseGenerator:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))


    def generate_response(self, persona, retrieved_chunks, conversation_history, user_message):
        prompt = f"""
        You are an AI assistant.
        Persona:
            {persona}
        Conversation so far:
            {conversation_history}
        Knowledge Base Context:
            {retrieved_chunks}
        User message:
            {user_message}
        Respond appropriately.
        """
    
        response = self.client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
    
        return response.choices[0].message.content