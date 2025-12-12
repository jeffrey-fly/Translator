
# services/translation/openai_service.py
from openai import OpenAI

class OpenAITranslationService(BaseTranslationService):
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def translate(self, text, target_lang="en"):
        prompt = f"Translate to {target_lang}: {text}"
        rsp = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return rsp.choices[0].message.content
