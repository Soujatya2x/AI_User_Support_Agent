from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

class PersonDetector:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def detect(self, message):
        prompt = f"""
        Classify persona:
        - Technical Expert
        - Frustrated User
        - Business Executive

        Message: {message}

        Return JSON:
        {{
          "persona": "...",
          "confidence": 0-1
        }}
        """

        response = self.client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content