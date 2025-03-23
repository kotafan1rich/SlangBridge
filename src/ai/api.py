import requests

from config import API_KEY


class Api:
    @staticmethod
    def get_gpt_response(response):
        return response["response"][0]["message"]["content"]

    @staticmethod
    def get_claude_response(response):
        return response.get("response")[0]["choices"][0]["message"]["content"]

    @staticmethod
    def get_deepseak_response(response):
        return response["response"][0]["choices"][0]["message"]["content"]

    def tarnslate(
        self, text: str, model_name: str = "Claude 3.5 Haiku", is_word: bool = True
    ) -> str:
        prompt = (
            f"""
        Переведи с молодёжно сленга слово: {text}.
        Ответь сразу переводом слова (одим словом или двумя) без вступлений и
        добавления фраз от себя. Например: я - кринж, ты - неловсть, стыд
        Если вместо слова что-то непоянтное, то выведи: Такого слова нет.
        """
            if is_word
            else f""" Представь, что ты переводчик для двух людей со сленга,
            которые не понимают друг друга из-за не понятных слов. Я тебе скажу фразу,
            а ты должен перевести со сленга и передать её другому человеку, как будто
            мы разговариваем в живую, а ты переводишь в реальном времени слово в слово
        Переведи с молодёжно сленга фразу (именно с молодёжного): {text}.
        Ответь сразу переводом слова без вступлений и добавления фраз от себя.
        """
        )

        models = {
            "Claude 3.5 Haiku": {
                "messages": [
                    {"role": "user", "content": [{"type": "text", "text": prompt}]}
                ],
                "model": "claude-3-5-haiku-20241022",
                "endpoint": "claude",
                "response_parser": Api.get_claude_response,
            },
            "Claude 3.7 Sonnet": {
                "messages": [
                    {"role": "user", "content": [{"type": "text", "text": prompt}]}
                ],
                "model": "claude-3-7-sonnet-20250219",
                "endpoint": "claude",
                "response_parser": Api.get_claude_response,
            },
            "gpt-4o-mini": {
                "messages": [{"role": "user", "content": prompt}],
                "model": "gpt-4o-mini-2024-07-18",
                "endpoint": "gpt-4o-mini",
                "response_parser": Api.get_gpt_response,
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
                "response_parser": Api.get_deepseak_response,
            },
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

        try:
            url_endpoint = f"https://api.gen-api.ru/api/v1/networks/{models[model_name]['endpoint']}"
            response = requests.post(url_endpoint, json=data, headers=headers).json()
            return models[model_name]["response_parser"](response)
        except Exception:
            return "Неудолось получить результат. Попробуйте позже."
