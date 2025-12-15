import re
from google import genai
from google.genai import types
from .base import BaseTranslatorService

client = genai.Client()

class GoogleTranslator(BaseTranslatorService):

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

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=[prompt],
            config=types.GenerateContentConfig(temperature=0)
        )
        return response.text.strip()
