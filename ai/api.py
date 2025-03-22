import requests

from config import API_KEY


def api(text: str, model_name: str = "Claude 3.5 Haiku") -> str:
    prompt = f"""
    Переведи с молодёжно сленга фразу (именно с молодёжного): {text}.
    Ответь сразу переводом слова без вступлений и постороннего. Максимальная длина 45.
    Если такого слова не существует, то выведи: Такого слова нет.
    """
    # задаем модель и промпт

    models = {
        "Claude 3.5 Haiku": {
            "messages": [
                {"role": "user", "content": [{"type": "text", "text": prompt}]}
            ],
            "model": "claude-3-5-haiku-20241022",
        },
        "Claude 3.7 Sonnet": {
            "messages": [
                {"role": "user", "content": [{"type": "text", "text": prompt}]}
            ],
            "model": "claude-3-7-sonnet-20250219",
        },
        "gpt-3.5": {
            "messages": {"role": "user", "content": prompt},
            "model": "gpt-3.5-turbo-1106",
        },
        "gpt-4o-mini": {
            "messages": {"role": "user", "content": prompt},
            "model": "gpt-4o-mini-2024-07-18",
        },
        "deepseek-r1": {
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            "model": "deepseek-r1",
        },
        "deepseek-v3": {
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            "model": "deepseek-v3",
        },
    }

    data = {
        # "model": "claude-3-5-haiku-20241022",
        "stream": False,
        "is_sync": True,
        "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}]}],
    }
    data = {
        "model":  models[model_name]["model"],
        "stream": False,
        "is_sync": True,
        "messages": models[model_name]["messages"],
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }

    url_endpoint = "https://api.gen-api.ru/api/v1/networks/claude"
    response = requests.post(url_endpoint, json=data, headers=headers).json()
    return response.get("response")[0]["choices"][0]["message"]["content"]
