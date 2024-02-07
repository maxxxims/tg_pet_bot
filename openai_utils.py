import openai
import logging
import asyncio
from config import load_openai_token

openai.api_key = load_openai_token()


async def generate_text(prompt) -> dict:
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        print(f"total_tokens = {response['usage']['total_tokens']}" )
        print(f"response = {response['choices'][0]['message']['content']}" )
        return response['choices'][0]['message']['content'], response['usage']['total_tokens']
    except Exception as e:
        print(e)
        logging.error(e)


async def generate_description(user_prompt):
    TEXT = "Преврати это описание в более грамотное, лаконичное, красивое, без наигранности, чтобы описание бездомного животного было привлекательно для объявления:"
    prompt = TEXT + '\n' + user_prompt
    answer, tokens = await generate_text(prompt)
    return answer


if __name__ == "__main__":
    description = "цвет: бурый, глаза красивые, послушный"
    loop = asyncio.get_event_loop()
    loop.run_until_complete(generate_description(description))