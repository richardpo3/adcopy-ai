import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are a sharp, direct AI assistant.
Answer clearly and concisely. No fluff."""

def chat():
    history = [{"role": "system", "content": SYSTEM_PROMPT}]
    print("\nCLI Chatbot — type 'quit' to exit\n")

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit"):
            print("Done.")
            break

        history.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=1024,
            messages=history,
        )

        reply = response.choices[0].message.content
        history.append({"role": "assistant", "content": reply})

        print(f"\nAI: {reply}\n")

if __name__ == "__main__":
    chat()
