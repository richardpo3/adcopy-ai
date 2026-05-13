import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are an expert Facebook and Instagram ad copywriter.
When given a product, target audience, and key benefit — write exactly 5 ad copy variations.

Each variation must use a different angle:
1. Curiosity hook
2. Problem → Solution
3. Social proof / results
4. Urgency / scarcity
5. Direct benefit

Format each one like:
[Angle Name]
Headline: ...
Body: ...

Keep headlines under 10 words. Keep body under 30 words. Be punchy, not corporate."""

def generate_ads(product, audience, benefit):
    prompt = f"""
Product: {product}
Target audience: {audience}
Key benefit: {benefit}

Write 5 ad copy variations.
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1024,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content

def main():
    print("\nAI Ad Copy Generator")
    print("====================\n")

    product = input("Product name: ").strip()
    audience = input("Target audience (e.g. 'Shopify store owners', 'busy moms'): ").strip()
    benefit = input("Key benefit (e.g. 'saves 2 hours a day', 'doubles conversions'): ").strip()

    print("\nGenerating your ads...\n")
    result = generate_ads(product, audience, benefit)
    print(result)
    print()

if __name__ == "__main__":
    main()
