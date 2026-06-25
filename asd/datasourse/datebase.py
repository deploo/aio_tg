from llama_cpp import Llama
import asyncio
import re
import random

llm = Llama(
    model_path="models/qwen2.5-7b-instruct-q4_k_m.gguf",
    n_ctx=4096,
    n_threads=8,
    n_gpu_layers=35
)

DEFAULT_WORDS = [
    {"word": "apple", "trans": "яблоко", "example": "I eat an apple"},
    {"word": "cat", "trans": "кот", "example": "My cat sleeps"},
    {"word": "dog", "trans": "собака", "example": "The dog runs"},
    {"word": "house", "trans": "дом", "example": "Big house"},
    {"word": "car", "trans": "машина", "example": "Red car"},
    {"word": "book", "trans": "книга", "example": "I read a book"},
    {"word": "tree", "trans": "дерево", "example": "The tree is big"},
    {"word": "sun", "trans": "солнце", "example": "The sun shines"},
    {"word": "moon", "trans": "луна", "example": "The moon is bright"},
    {"word": "star", "trans": "звезда", "example": "The star twinkles"}
]


def get_default_word() -> dict:
    return random.choice(DEFAULT_WORDS)


async def generate_new_word() -> dict:
    try:
        messages = [
            {
                "role": "system",
                "content": "Ты - генератор слов для изучения английского. Придумай ОДНО слово, его перевод на русский и пример использования. Отвечай строго в формате: слово | перевод | пример"
            },
            {
                "role": "user",
                "content": "Придумай новое слово для изучения"
            }
        ]

        response = await asyncio.to_thread(
            llm.create_chat_completion,
            messages=messages,
            max_tokens=200,
            temperature=0.8,
            stop=["<|im_end|>"]
        )

        result = response['choices'][0]['message']['content'].strip()

        parts = result.split('|')

        if len(parts) >= 3:
            return {
                "word": parts[0].strip(),
                "trans": parts[1].strip(),
                "example": parts[2].strip()
            }
        else:
            word_match = re.search(r'(\w+)\s*[|—-]\s*([а-яА-ЯёЁ\s]+)\s*[|—-]\s*(.+?)(?:\n|$)', result)
            if word_match:
                return {
                    "word": word_match.group(1).strip(),
                    "trans": word_match.group(2).strip(),
                    "example": word_match.group(3).strip()
                }

            return get_default_word()

    except Exception as e:
        return get_default_word()


async def check_llama(text: str) -> str:
    try:
        messages = [
            {
                "role": "system",
                "content": "Ты - эксперт по английскому языку. Проверяй текст на ошибки. Отвечай кратко: сначала укажи ошибки, потом дай исправленный вариант."
            },
            {
                "role": "user",
                "content": f'Проверь этот текст на английском: "{text}"'
            }
        ]

        response = await asyncio.to_thread(
            llm.create_chat_completion,
            messages=messages,
            max_tokens=512,
            temperature=0.3,
            stop=["<|im_end|>"]
        )

        return response['choices'][0]['message']['content']

    except Exception as e:
        return f"Ошибка при обращении к модели: {str(e)}"