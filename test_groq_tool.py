import os
import asyncio

from dotenv import load_dotenv
from openai import AsyncOpenAI


load_dotenv()

client = AsyncOpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)


async def main():

    tools = [
        {
            "type": "function",
            "function": {
                "name": "transfer_to_marketing_planner",
                "description": "Transfer the request to the Marketing Planner.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                    "additionalProperties": False,
                },
            },
        }
    ]

    response = await client.chat.completions.create(
        model=os.getenv(
            "GROQ_MODEL",
            "llama-3.3-70b-versatile",
        ),
        messages=[
            {
                "role": "user",
                "content": "Please use the marketing planner.",
            }
        ],
        tools=tools,
    )

    print("GROQ HANDOFF TOOL TEST: SUCCESS")
    print(response)


if __name__ == "__main__":
    asyncio.run(main())