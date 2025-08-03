# ai_core.py

import openai
import langdetect
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

async def generate_workout(user_input: str, last_workout: str = "") -> str:
    # Определяем язык запроса
    try:
        lang = langdetect.detect(user_input)
    except Exception:
        lang = "en"

    # Признаки запроса на перевод
    user_input_lower = user_input.lower()
    wants_translation = any(phrase in user_input_lower for phrase in [
        "переведи", "на английском", "английский", "translate", "in english", "english version"
    ])

    # Если явно просит перевод и есть последняя тренировка — переведём её
    if wants_translation and last_workout:
        user_input = f"{user_input}\n\nВот последняя программа:\n{last_workout}"

    # Промпт на нужном языке
    if lang == "ru":
        system_prompt = (
            "Ты — виртуальный фитнес-тренер. "
            "Если пользователь просит составить тренировку, составь. "
            "Если пользователь просит перевести предыдущую тренировку — переведи. "
            "Если сообщение не связано с тренировками, скажи: "
            "«Я могу помочь только с тренировками 💪» — и ничего больше."
        )
    else:
        system_prompt = (
            "You are a virtual fitness coach. "
            "If the user asks for a workout, create one. "
            "If the user asks to translate the previous workout, do it. "
            "If the message is not related to training, say: "
            "“I can only help with training plans 💪” — and nothing else."
        )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]

    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=600,
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return f"⚠️ Ошибка при обращении к GPT: {str(e)}"
