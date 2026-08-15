import os
import asyncio

from dotenv import load_dotenv
from openai import AsyncOpenAI


load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY is not set")


client = AsyncOpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
)


async def main():
    response = await client.chat.completions.create(
        model=os.getenv(
            "GROQ_MODEL",
            "llama-3.3-70b-versatile",
        ),
        messages=[
            {
                "role": "user",
                "content": "Say hello",
            }
        ],
    )

    print("GROQ TEST SUCCESS")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    asyncio.run(main())