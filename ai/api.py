import requests

from config import API_KEY


def get_gpt_response(response):
    return response["response"][0]["message"]["content"]


def get_claude_response(response):
    return response.get("response")[0]["choices"][0]["message"]["content"]


def get_deepseak_response(response):
    return response["response"][0]["choices"][0]["message"]["content"]


def api(text: str, model_name: str = "deepseek-v3", is_word: bool = True) -> str:
    prompt = f"""
    Переведи с молодёжно сленга слово (именно с молодёжного): {text}.
    Ответь сразу переводом слова без вступлений и постороннего. Максимальная длина ответа 45.
    Если вместо слова что-то непоянтное, то выведи: Такого слова нет.
    """ if is_word else """Переведи с молодёжно сленга фразу (именно с молодёжного): {text}.
    Ответь сразу переводом слова без вступлений и постороннего.
    """
    # задаем модель и промпт

    models = {
        "Claude 3.5 Haiku": {
            "messages": [
                {"role": "user", "content": [{"type": "text", "text": prompt}]}
            ],
            "model": "claude-3-5-haiku-20241022",
            "endpoint": "claude",
            "response_parser": get_claude_response,
        },
        "Claude 3.7 Sonnet": {
            "messages": [
                {"role": "user", "content": [{"type": "text", "text": prompt}]}
            ],
            "model": "claude-3-7-sonnet-20250219",
            "endpoint": "claude",
            "response_parser": get_claude_response,
        },
        "gpt-4o-mini": {
            "messages": [{"role": "user", "content": prompt}],
            "model": "gpt-4o-mini-2024-07-18",
            "endpoint": "gpt-4o-mini",
            "response_parser": get_gpt_response,
        },
        "deepseek-v3": {
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            "model": "deepseek-v3",
            "endpoint": "deepseek-v3",
            "response_parser": get_deepseak_response,
        },
    }

    data = {
        # "model": "claude-3-5-haiku-20241022",
        "stream": True,
        "is_sync": True,
        "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}]}],
    }
    data = {
        "model": models[model_name]["model"],
        "stream": False,
        "is_sync": True,
        "messages": models[model_name]["messages"],
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }

    url_endpoint = (
        f"https://api.gen-api.ru/api/v1/networks/{models[model_name]['endpoint']}"
    )
    response = requests.post(url_endpoint, json=data, headers=headers).json()
    return models[model_name]["response_parser"](response)
