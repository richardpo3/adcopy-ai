import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are a summarisation assistant.
When given any text, respond with exactly 3 bullet points.
Each bullet must be one clear sentence. No intro, no outro."""

def summarise(text):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=256,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text},
        ],
    )
    return response.choices[0].message.content

def main():
    print("\nText Summariser — paste your text, press Enter twice to summarise\n")

    while True:
        lines = []
        while True:
            line = input()
            if line == "":
                break
            if line.lower() == "quit":
                return
            lines.append(line)

        text = "\n".join(lines).strip()
        if not text:
            continue

        print("\nSummary:")
        print(summarise(text))
        print()

if __name__ == "__main__":
    main()
