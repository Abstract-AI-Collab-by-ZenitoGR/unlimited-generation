import asyncio
import os
from groq import AsyncGroq

async def groq_streaming(messages):
    print(messages)
    
    groq_api_key = os.getenv("GROQ_API_KEY")
    client = AsyncGroq(api_key=groq_api_key)

    stream = await client.chat.completions.create(
        messages=messages,
        model="llama3-8b-8192",
        temperature=0.5,
        max_tokens=8000,
        top_p=1,
        stream=True,
    )

    async for chunk in stream:
        yield chunk.choices[0].delta.content

async def groq_response(messages, max_tokens=8192):
    print("messages length:",len(messages))
    
    groq_api_key = os.getenv("GROQ_API_KEY")
    client = AsyncGroq(api_key=groq_api_key)

    chat_completion = await client.chat.completions.create(
        messages=messages,
        model="mixtral-8x7b-32768",
        temperature=0.9,
        max_tokens=max_tokens,
        top_p=1,
        stream=False,
    )
    print(chat_completion.usage.prompt_tokens)
    print(chat_completion.usage.completion_tokens)
    return chat_completion.choices[0].message.content, chat_completion.usage.completion_tokens, max_tokens