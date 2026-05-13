import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

PROMPTS = {
    "Direct": "Answer in one sentence. No fluff.",
    "Explain like I'm 12": "Explain everything simply, like you're talking to a curious 12-year-old. Use analogies.",
    "Expert": "You are a senior expert. Give a thorough, technical answer with nuance and caveats.",
}

def test(user_message):
    print(f"\n{'='*60}")
    print(f"Message: {user_message}")
    print(f"{'='*60}\n")

    for name, system_prompt in PROMPTS.items():
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=512,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
        )
        reply = response.choices[0].message.content
        print(f"[ {name} ]")
        print(reply)
        print()

def main():
    print("\nPrompt Tester — same message, 3 different system prompts")
    print("Type 'quit' to exit\n")

    while True:
        message = input("Your message: ").strip()
        if not message:
            continue
        if message.lower() in ("quit", "exit"):
            break
        test(message)

if __name__ == "__main__":
    main()
