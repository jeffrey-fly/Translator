import re
from google import genai
from google.genai import types

from .base import BaseTranslatorService

class GoogleTranslator(BaseTranslatorService):
    def __init__(self, api_key = None):
        self._client = None
        self._api_key = api_key
        self.model_name = "gemini-2.5-flash-lite"

    @property
    def client(self) -> genai.Client:
        """
        每次访问 self.client 时，都会检查 _client 是否已实例化。
        """
        if self._client is None:
            if not self._api_key:
                raise ValueError(
                    "【配置错误】Google API Key 尚未设置。 "
                    "请在初始化时传入或调用 .set_api_key() 方法。"
                )

            # 只有在有 Key 且 client 为空时才创建实例
            print(f"正在使用 Key [***{self._api_key[-4:]}] 初始化 Google GenAI Client...")
            self._client = genai.Client(api_key=self._api_key)

        return self._client

    def set_api_key(self, api_key: str):
        """
        动态更新 API Key。
        更新后会将旧的 client 置空，下次请求时会自动重连。
        """
        if api_key and api_key != self._api_key:
            self._api_key = api_key
            self._client = None

    @staticmethod
    def _is_single_word(text: str) -> bool:
        text = text.strip()
        if not text:
            return False
        # 英文单词
        if re.fullmatch(r"[A-Za-z0-9\-']{1,30}", text):
            return True
        # 中文、日文、韩文短词
        if len(text) <= 3 and re.fullmatch(r"[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]+", text):
            return True
        return False

    def translate(self, text: str, target_language: str = "zh", source_language: str = "auto") -> str:
        text = text.strip()
        if self._is_single_word(text):
            prompt = (
                f"Translate the {source_language} word '{text}' into {target_language}.\n"
                "For each possible meaning, categorize by part of speech (e.g., n, vt, vi, adj),\n"
                "provide all meanings in Chinese for that part of speech, and give at most 1 example sentence per part of speech.\n"
                "Each example sentence should show the original sentence, a slash '/', then the Chinese translation.\n"
                "Output format:\n"
                "part_of_speech: meaning1; meaning2; ...\n"
                "Example: English sentence / Chinese translation\n"
                "Do not include any explanations in English."
            )
        else:
            prompt = f"Translate the following {source_language} text into {target_language}:\n{text}\nDo not add any extra explanations or examples."

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=[prompt],
            config=types.GenerateContentConfig(temperature=0)
        )
        return response.text.strip()
