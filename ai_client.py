import os
import time
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class AIClient:
    def __init__(self, model="llama-3.3-70b-versatile", max_retries=3):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = model
        self.max_retries = max_retries

    def ask(self, prompt, system_prompt=None, max_tokens=1024):
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        for attempt in range(self.max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    max_tokens=max_tokens,
                    messages=messages,
                )
                return response.choices[0].message.content
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(2)
        return "Error: all retries failed."


if __name__ == "__main__":
    ai = AIClient()
    print("Testing API wrapper...\n")
    reply = ai.ask("What is one thing a beginner builder should do every day?")
    print(reply)
