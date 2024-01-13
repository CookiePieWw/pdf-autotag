import os
import json
import requests

class OpenAIClient:
    def __init__(self, use_proxy: bool=True, sse: bool=False):
        self.api_key = os.environ.get("OPENAI_API_KEY")
        if self.api_key is None:
            raise ValueError("No API key available, please set the OPENAI_API_KEY environment variable")

        self.baseurl = "https://api.openai.com/v1"
        self.url = f'{self.baseurl}/chat/completions'
        self.use_proxy = use_proxy
        if use_proxy:
            self.proxies = {
                "http": os.environ.get("OPENAI_HTTP_PROXY"),
                "https": os.environ.get("OPENAI_HTTP_PROXY"),
            }

        if self.proxies["http"] is None and self.proxies["https"] is None:
            raise ValueError("No proxy available, please set the OPENAI_HTTP_PROXY and OPENAI_HTTPS_PROXY environment variables")

        self.defaut_settings = {
            "temperature": 0,
            "top_p": 1,
            "n": 1,
            "stream": sse,
            "max_tokens": 250,
            "frequency_penalty": 0,
            "presence_penalty": 0,
        }

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    async def listModels(self):
        return [
            "gpt-3.5-turbo",
            "gpt-4",
            "gpt-4-vision-preview",
            "gpt-4-1106-preview",
        ]

    async def sendMessage(self, messages, model: str="gpt-4-1106-preview"):
        data = {
            "model": model,
            "messages": messages,
        }
        data.update(self.defaut_settings)

        if self.use_proxy:
            assert(self.proxies is not None)
            response = requests.post(self.url, json=data, headers=self.headers, proxies=self.proxies)
        else:
            response = requests.post(self.url, json=data, headers=self.headers)

        plain_text = json.loads(response.text)
        return plain_text['choices'][0]['message']['content']
